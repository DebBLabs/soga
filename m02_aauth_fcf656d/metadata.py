"""Truthful interim metadata for the incomplete Steps 1-3 foundation."""

from . import profile


def interim_person_server_metadata(issuer, jwks_uri):
    if not isinstance(issuer, str) or not issuer.startswith("https://"):
        raise ValueError("HTTPS issuer required")
    if not isinstance(jwks_uri, str) or not jwks_uri.startswith("https://"):
        raise ValueError("HTTPS jwks_uri required")
    return {
        "issuer": issuer.rstrip("/"),
        "jwks_uri": jwks_uri,
        "aauth_profile_commit": profile.AAUTH_COMMIT,
        "test_only": True,
        "conformance": "incomplete-steps-1-3-foundation",
    }


def assert_interim_metadata(metadata):
    prohibited = {"person_token_endpoint", "auth_token_endpoint"}
    if prohibited.intersection(metadata):
        raise ValueError("unimplemented endpoint advertised")
    if metadata.get("test_only") is not True:
        raise ValueError("metadata must remain test-only")
    return dict(metadata)

