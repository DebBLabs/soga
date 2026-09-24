"""Focused specification tests for the create-only AAuth fcf656d foundation."""

import base64
import hashlib
import json
from pathlib import Path
import unittest

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from m02_aauth_fcf656d import profile
from m02_aauth_fcf656d.http_signatures import (
    ReplayCache, Request, SignatureProfileError, content_digest, sign_request,
    parse_signature_error, signature_error_header, verify_content_digest,
    verify_request,
)
from m02_aauth_fcf656d.jose import (
    JoseError, public_jwk, public_jwks, sign_compact, verify_compact,
    validate_public_jwk,
)
from m02_aauth_fcf656d.metadata import (
    assert_interim_metadata, interim_person_server_metadata,
)
from m02_aauth_fcf656d.structured_fields import (
    InnerList, Item, StructuredFieldError, Token, parse_dictionary,
    parse_item, serialize_dictionary,
)


class Fixture(unittest.TestCase):
    def setUp(self):
        self.issuer_private = Ed25519PrivateKey.generate()
        self.agent_private = Ed25519PrivateKey.generate()
        self.issuer_jwk = public_jwk(self.issuer_private.public_key(), "issuer-1")
        self.agent_jwk = public_jwk(self.agent_private.public_key(), "agent-1")
        self.issuer_jwks = public_jwks([self.issuer_jwk])

    def assertion(self, typ="aa-agent+jwt"):
        return sign_compact(
            {"cnf": {"jwk": self.agent_jwk}, "exp": 2_000_000_000,
             "iss": "https://issuer.example", "jti": "test-jti"},
            typ, "issuer-1", self.issuer_private)


class ProfileTests(unittest.TestCase):
    def test_exact_pin_and_types(self):
        self.assertEqual(profile.AAUTH_COMMIT, "fcf656de1926535f5bd6fc0538147ead6646e727")
        self.assertEqual(profile.JOSE_ALGORITHM, "Ed25519")
        self.assertEqual(profile.TOKEN_TYPES, {
            "aa-agent+jwt", "aa-person+jwt", "aa-resource+jwt", "aa-auth+jwt",
        })


class StructuredFieldTests(unittest.TestCase):
    def test_dictionary_round_trip_preserves_order_and_types(self):
        value = (("sig", InnerList((Item("@method"), Item("@path")), (("created", 12),))),)
        encoded = serialize_dictionary(value)
        self.assertEqual(parse_dictionary(encoded), value)

    def test_token_is_not_quoted_string(self):
        encoded = serialize_dictionary((("sig", Item(Token("jwt"), (("jwt", "a.b.c"),))),))
        self.assertEqual(encoded, 'sig=jwt;jwt="a.b.c"')
        self.assertEqual(parse_dictionary(encoded)[0][1].value, Token("jwt"))

    def test_duplicate_dictionary_and_parameter_rejected(self):
        for value in ("a=1, a=2", "a=token;x=1;x=2"):
            with self.subTest(value=value), self.assertRaises(StructuredFieldError):
                parse_dictionary(value)

    def test_trailing_and_malformed_values_rejected(self):
        for value in ('"ok" trailing', ":not base64!:", "?2", "1000000000000000",
                      "١٢٣", "१२३"):
            with self.subTest(value=value), self.assertRaises(StructuredFieldError):
                parse_item(value)

    def test_oversized_field_rejected(self):
        with self.assertRaises(StructuredFieldError):
            parse_dictionary("a=" + '"' + "x" * profile.MAX_FIELD_BYTES + '"')


class JoseTests(Fixture):
    def test_sign_verify_each_exact_type(self):
        for typ in sorted(profile.TOKEN_TYPES):
            token = sign_compact({"purpose": typ}, typ, "issuer-1", self.issuer_private)
            self.assertEqual(verify_compact(token, typ, self.issuer_jwks), {"purpose": typ})

    def test_cross_type_confusion_rejected(self):
        token = self.assertion("aa-person+jwt")
        with self.assertRaisesRegex(JoseError, "wrong AAuth token type"):
            verify_compact(token, "aa-auth+jwt", self.issuer_jwks)

    def test_header_payload_and_signature_tampering_rejected(self):
        token = self.assertion()
        parts = token.split(".")
        cases = (
            "e30." + parts[1] + "." + parts[2],
            parts[0] + ".eyJjaGFuZ2VkIjp0cnVlfQ." + parts[2],
            parts[0] + "." + parts[1] + "." + ("A" if parts[2][0] != "A" else "B") + parts[2][1:],
        )
        for changed in cases:
            with self.subTest(token=changed), self.assertRaises(JoseError):
                verify_compact(changed, "aa-agent+jwt", self.issuer_jwks)

    def test_algorithm_and_key_policy(self):
        invalid = [
            {**self.issuer_jwk, "alg": "EdDSA"},
            {**self.issuer_jwk, "alg": "HS256"},
            {key: value for key, value in self.issuer_jwk.items() if key != "alg"},
            {**self.issuer_jwk, "kty": "EC"},
            {**self.issuer_jwk, "crv": "X25519"},
            {**self.issuer_jwk, "d": "private"},
        ]
        for jwk in invalid:
            with self.subTest(jwk=jwk), self.assertRaises(JoseError):
                public_jwks([jwk])

    def test_standard_base64_alphabet_is_rejected_for_jwk_x(self):
        standard = base64.b64encode(bytes([251, 255, 190, 62]) * 8).decode("ascii").rstrip("=")
        self.assertTrue("+" in standard or "/" in standard)
        with self.assertRaises(JoseError):
            validate_public_jwk({**self.issuer_jwk, "x": standard})

    def test_jwks_is_public_deterministic_and_kid_unique(self):
        other = public_jwk(Ed25519PrivateKey.generate().public_key(), "aaa")
        result = public_jwks([self.issuer_jwk, other])
        self.assertEqual([key["kid"] for key in result["keys"]], ["aaa", "issuer-1"])
        self.assertTrue(all("d" not in key for key in result["keys"]))
        with self.assertRaises(JoseError):
            public_jwks([self.issuer_jwk, self.issuer_jwk])

    def test_unknown_kid_and_unsupported_typ_rejected(self):
        token = self.assertion()
        with self.assertRaises(JoseError):
            verify_compact(token, "aa-agent+jwt", {"keys": []})
        with self.assertRaises(JoseError):
            sign_compact({}, "JWT", "issuer-1", self.issuer_private)


class HttpSignatureTests(Fixture):
    def base_request(self):
        return Request("POST", "ps.example", "/approve", {}, b"")

    def test_bound_request_verifies(self):
        signed = sign_request(self.base_request(), self.assertion(), self.agent_private, created=100)
        claims = verify_request(signed, self.issuer_jwks, "aa-agent+jwt", now=100)
        self.assertEqual(claims["jti"], "test-jti")

    def test_method_authority_path_and_key_are_bound(self):
        signed = sign_request(self.base_request(), self.assertion(), self.agent_private, created=100)
        variants = (
            Request("DELETE", signed.authority, signed.path, signed.headers, signed.body),
            Request(signed.method, "other.example", signed.path, signed.headers, signed.body),
            Request(signed.method, signed.authority, "/other", signed.headers, signed.body),
            Request(signed.method, signed.authority, signed.path,
                    {**signed.headers, "signature-key": signed.headers["signature-key"] + "x"}, signed.body),
        )
        for changed in variants:
            with self.subTest(changed=changed), self.assertRaises(SignatureProfileError):
                verify_request(changed, self.issuer_jwks, "aa-agent+jwt", now=100)

    def test_body_digest_and_content_type_are_bound(self):
        request = Request("POST", "ps.example", "/approve",
                          {"content-type": "application/json"}, b'{"ok":true}')
        signed = sign_request(request, self.assertion(), self.agent_private, created=100,
                              body_request=True)
        verify_request(signed, self.issuer_jwks, "aa-agent+jwt", now=100,
                       body_request=True)
        altered = Request(signed.method, signed.authority, signed.path, signed.headers, b'{"ok":false}')
        with self.assertRaisesRegex(SignatureProfileError, "digest"):
            verify_request(altered, self.issuer_jwks, "aa-agent+jwt", now=100,
                           body_request=True)
        altered_type = Request(signed.method, signed.authority, signed.path,
                               {**signed.headers, "content-type": "text/plain"}, signed.body)
        with self.assertRaises(SignatureProfileError):
            verify_request(altered_type, self.issuer_jwks, "aa-agent+jwt", now=100,
                           body_request=True)

    def test_digest_is_checked_before_body_interpretation(self):
        invalid_json = b"not-json"
        self.assertEqual(content_digest(invalid_json),
                         'sha-256=:' + base64.b64encode(hashlib.sha256(invalid_json).digest()).decode() + ':')
        with self.assertRaises(SignatureProfileError):
            verify_content_digest(content_digest(b"different"), invalid_json)

    def test_created_window_skew_and_replay(self):
        signed = sign_request(self.base_request(), self.assertion(), self.agent_private, created=100)
        with self.assertRaisesRegex(SignatureProfileError, "stale"):
            verify_request(signed, self.issuer_jwks, "aa-agent+jwt", now=161)
        boundary = sign_request(self.base_request(), self.assertion(), self.agent_private, created=160)
        verify_request(boundary, self.issuer_jwks, "aa-agent+jwt", now=100)
        future = sign_request(self.base_request(), self.assertion(), self.agent_private, created=161)
        with self.assertRaises(SignatureProfileError) as caught:
            verify_request(future, self.issuer_jwks, "aa-agent+jwt", now=100)
        self.assertEqual(caught.exception.code, "clock_skew")
        cache = ReplayCache()
        verify_request(signed, self.issuer_jwks, "aa-agent+jwt", now=100, replay_cache=cache)
        with self.assertRaisesRegex(SignatureProfileError, "replayed"):
            verify_request(signed, self.issuer_jwks, "aa-agent+jwt", now=100, replay_cache=cache)

    def test_missing_duplicate_and_unsupported_scheme(self):
        signed = sign_request(self.base_request(), self.assertion(), self.agent_private, created=100)
        missing = Request(signed.method, signed.authority, signed.path,
                          {key: value for key, value in signed.headers.items() if key != "signature"})
        with self.assertRaises(SignatureProfileError):
            verify_request(missing, self.issuer_jwks, "aa-agent+jwt", now=100)
        duplicate = Request(signed.method, signed.authority, signed.path,
                            {**signed.headers, "signature": signed.headers["signature"] + ", sig=:AA==:"})
        with self.assertRaises(SignatureProfileError):
            verify_request(duplicate, self.issuer_jwks, "aa-agent+jwt", now=100)
        unsupported = Request(signed.method, signed.authority, signed.path,
                              {**signed.headers, "signature-key": "sig=hwk;kty=\"OKP\""})
        with self.assertRaises(SignatureProfileError) as caught:
            verify_request(unsupported, self.issuer_jwks, "aa-agent+jwt", now=100)
        self.assertEqual(caught.exception.code, "unsupported_scheme")

    def test_label_is_correlated_across_signature_fields(self):
        signed = sign_request(self.base_request(), self.assertion(),
                              self.agent_private, created=100)
        mismatched = Request(
            signed.method, signed.authority, signed.path,
            {**signed.headers,
             "signature": signed.headers["signature"].replace("sig=", "other=", 1)},
            signed.body)
        with self.assertRaises(SignatureProfileError):
            verify_request(mismatched, self.issuer_jwks, "aa-agent+jwt", now=100)
        two_labels = Request(
            signed.method, signed.authority, signed.path,
            {**signed.headers,
             "signature-input": signed.headers["signature-input"]
             + ', other=("@method");created=100'},
            signed.body)
        with self.assertRaises(SignatureProfileError):
            verify_request(two_labels, self.issuer_jwks, "aa-agent+jwt", now=100)

    def test_signature_error_is_structured_and_uniform(self):
        error = SignatureProfileError("required_input", "details not emitted", ("content-type",))
        header = signature_error_header(error)
        self.assertIn("required_input", header)
        self.assertNotIn("details not emitted", header)
        self.assertEqual(parse_signature_error(header),
                         ("required_input", ("content-type",)))
        for code in sorted(profile.SIGNATURE_ERROR_CODES):
            self.assertIn(code, signature_error_header(SignatureProfileError(code, "secret")))


class MetadataAndRegressionTests(unittest.TestCase):
    def test_metadata_is_truthful_and_incomplete(self):
        metadata = interim_person_server_metadata(
            "https://ps.example/", "https://ps.example/jwks.json")
        self.assertEqual(metadata["issuer"], "https://ps.example")
        self.assertTrue(metadata["test_only"])
        self.assertNotIn("person_token_endpoint", metadata)
        self.assertNotIn("auth_token_endpoint", metadata)
        self.assertEqual(assert_interim_metadata(metadata), metadata)

    def test_metadata_rejects_false_endpoint_claim(self):
        with self.assertRaises(ValueError):
            assert_interim_metadata({"test_only": True, "person_token_endpoint": "/token"})

    def test_accepted_stage2_files_are_unchanged(self):
        root = Path(__file__).resolve().parents[1]
        expected = {
            "m02_person_server/__init__.py": "1590a304fe8181b6fe7c9e2819e61a5799afb31d827e9cdf596e5cfb97c084b5",
            "m02_person_server/__main__.py": "98adae8175c8c06aa65a186a5beff80ec3e37df05e3a7c9807c4053a92f517b3",
            "m02_person_server/crypto.py": "df1c28318ab44b2c23a957a5aecd23f4bcda2e6068f4616786aaa1916bfac6f9",
            "m02_person_server/http_server.py": "51d11c9a928ecc432efe8d86a342200b9d6666da78acfaa77042e0bfe922c74b",
            "m02_person_server/service.py": "0b7c0d503ef347c568fc6f6e5ece690d41b1fbc5885f2805b36819d261127043",
            "m02_person_server/store.py": "0c60b7f8e2539a7da7ccae7c301c5366b269974c15a29c4dc029e4bc647fc590",
            "m02_person_server/walkthrough.py": "0e69bcfc8edb9655020d4733af25de473e1a1488a333ae779a252ecfac34528d",
            "tests/test_m02_person_server.py": "68dabc624a1d045d73ce29a210da552f987ce49d39fe9e234965e5faf6289ec5",
        }
        for relative, digest in expected.items():
            with self.subTest(path=relative):
                self.assertEqual(hashlib.sha256((root / relative).read_bytes()).hexdigest(), digest)


if __name__ == "__main__":
    unittest.main()
