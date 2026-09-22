#!/usr/bin/env python3
"""Bounded provider extension for public-key import and key generation."""

import hashlib
import json
from pathlib import Path
import sys


sys.dont_write_bytecode = True
PROVIDER_ROOT = Path(
    "/private/tmp/m02-aauth-fcf656d-phase1-install-20260921/site-packages"
)
EXPECTED_VERSION = "50.0.1"
PUBLIC_KEY = bytes.fromhex(
    "d75a980182b10ab7d54bfed3c964073a"
    "0ee172f3daa62325af021a68f707511a"
)
SIGNATURE = bytes.fromhex(
    "e5564300c360ac729086e2cc806e828a"
    "84877f1eb8e5d974d873e06522490155"
    "5fb8821590a33bacc61e39701cf9b46b"
    "d25bf5f0595bbe24655141438e7a100b"
)
MESSAGE = b""
WRONG_MESSAGE = b"wrong-message"
GENERATED_MESSAGE = b"bounded-provider-generation-check"
MODULE_PREFIXES = ("cryptography", "cffi", "_cffi_backend", "pycparser",
                   "typing_extensions")


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def exception_name(error):
    return type(error).__module__ + "." + type(error).__qualname__


def provider_module_paths():
    root = PROVIDER_ROOT.resolve()
    observed = {}
    for name, module in sorted(sys.modules.items()):
        if not name.startswith(MODULE_PREFIXES):
            continue
        origin = getattr(module, "__file__", None)
        if origin is None:
            observed[name] = "<no file origin: built-in or extension submodule>"
            continue
        resolved = Path(origin).resolve()
        require(root in resolved.parents, "provider module escaped pinned root: " + name)
        observed[name] = str(resolved)
    require(observed, "no provider modules observed")
    return observed


def rejection(operation):
    try:
        operation()
    except Exception as error:
        return exception_name(error)
    raise RuntimeError("negative case was accepted")


def main():
    require(len(sys.argv) == 1, "no command-line arguments permitted")
    require(PROVIDER_ROOT.is_dir() and not PROVIDER_ROOT.is_symlink(),
            "provider root absent or unsafe")
    script_dir = str(Path(__file__).resolve().parent)
    sys.path[:] = [entry for entry in sys.path if entry not in ("", script_dir)]
    sys.path.insert(0, str(PROVIDER_ROOT))

    import cryptography
    from cryptography.exceptions import InvalidSignature
    from cryptography.hazmat.primitives.asymmetric.ed25519 import (
        Ed25519PrivateKey, Ed25519PublicKey,
    )

    require(cryptography.__version__ == EXPECTED_VERSION, "provider version mismatch")

    imported = Ed25519PublicKey.from_public_bytes(PUBLIC_KEY)
    require(imported.public_bytes_raw() == PUBLIC_KEY, "public-key round trip mismatch")
    imported.verify(SIGNATURE, MESSAGE)
    wrong_message = rejection(lambda: imported.verify(SIGNATURE, WRONG_MESSAGE))
    altered = bytearray(SIGNATURE)
    altered[0] ^= 1
    altered_signature = rejection(lambda: imported.verify(bytes(altered), MESSAGE))
    require(wrong_message.endswith("InvalidSignature"), "wrong message exception mismatch")
    require(altered_signature.endswith("InvalidSignature"), "altered signature exception mismatch")
    short_key = rejection(lambda: Ed25519PublicKey.from_public_bytes(PUBLIC_KEY[:-1]))
    long_key = rejection(lambda: Ed25519PublicKey.from_public_bytes(PUBLIC_KEY + b"\x00"))

    generated_one = Ed25519PrivateKey.generate()
    generated_two = Ed25519PrivateKey.generate()
    public_one = generated_one.public_key().public_bytes_raw()
    public_two = generated_two.public_key().public_bytes_raw()
    require(len(public_one) == 32 and len(public_two) == 32,
            "generated public-key length mismatch")
    require(public_one != public_two, "generated public keys unexpectedly equal")
    signature_one = generated_one.sign(GENERATED_MESSAGE)
    signature_two = generated_two.sign(GENERATED_MESSAGE)
    generated_one.public_key().verify(signature_one, GENERATED_MESSAGE)
    generated_two.public_key().verify(signature_two, GENERATED_MESSAGE)
    generated_one_wrong = rejection(
        lambda: generated_one.public_key().verify(signature_one, WRONG_MESSAGE))
    generated_two_wrong = rejection(
        lambda: generated_two.public_key().verify(signature_two, WRONG_MESSAGE))
    require(generated_one_wrong.endswith("InvalidSignature"),
            "generated key one wrong-message exception mismatch")
    require(generated_two_wrong.endswith("InvalidSignature"),
            "generated key two wrong-message exception mismatch")

    result = {
        "result": "ED25519_PROVIDER_EXTENSION_VERIFIED",
        "provider_version": cryptography.__version__,
        "python_version": sys.version.split()[0],
        "vector": "RFC8032-7.1-TEST-1",
        "public_key_sha256": hashlib.sha256(PUBLIC_KEY).hexdigest(),
        "signature_sha256": hashlib.sha256(SIGNATURE).hexdigest(),
        "tests": {
            "public_key_round_trip": True,
            "signature_verifies": True,
            "wrong_message_rejected": True,
            "altered_signature_rejected": True,
            "invalid_public_key_lengths_rejected": {"31": short_key, "33": long_key},
            "generated_keys_distinct": True,
            "generated_public_key_lengths": [32, 32],
            "generated_signatures_verify": True,
            "generated_wrong_messages_rejected": True,
        },
        "loaded_provider_modules": provider_module_paths(),
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        failure = {"result": "FAILED", "error_type": exception_name(error),
                   "error": str(error)}
        print(json.dumps(failure, sort_keys=True, separators=(",", ":")))
        raise SystemExit(1)
