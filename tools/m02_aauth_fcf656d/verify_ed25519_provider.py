#!/usr/bin/env python3
"""Deterministic Ed25519 behavior checks for the pinned provider tree."""

import hashlib
import json
from pathlib import Path
import sys


sys.dont_write_bytecode = True

PROVIDER_ROOT = Path(
    "/private/tmp/m02-aauth-fcf656d-phase1-install-20260921/site-packages"
)
SCRIPT_DIRECTORY = str(Path(__file__).resolve().parent)
SECRET_SEED = bytes.fromhex(
    "9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60"
)
EXPECTED_PUBLIC_KEY = bytes.fromhex(
    "d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a"
)
EXPECTED_SIGNATURE = bytes.fromhex(
    "e5564300c360ac729086e2cc806e828a84877f1eb8e5d974d873e06522490155"
    "5fb8821590a33bacc61e39701cf9b46bd25bf5f0595bbe24655141438e7a100b"
)
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


def main():
    require(len(sys.argv) == 1, "no command-line arguments permitted")
    require(PROVIDER_ROOT.is_dir() and not PROVIDER_ROOT.is_symlink(),
            "provider root absent or unsafe")
    sys.path[:] = [entry for entry in sys.path if entry not in ("", SCRIPT_DIRECTORY)]
    sys.path.insert(0, str(PROVIDER_ROOT))

    import cryptography
    from cryptography.exceptions import InvalidSignature
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

    require(cryptography.__version__ == "50.0.1", "provider version mismatch")
    private_key = Ed25519PrivateKey.from_private_bytes(SECRET_SEED)
    public_key = private_key.public_key()
    public_bytes = public_key.public_bytes_raw()
    signature = private_key.sign(b"")
    require(public_bytes == EXPECTED_PUBLIC_KEY, "RFC public key mismatch")
    require(signature == EXPECTED_SIGNATURE, "RFC signature mismatch")
    public_key.verify(EXPECTED_SIGNATURE, b"")

    wrong_message_rejected = False
    try:
        public_key.verify(EXPECTED_SIGNATURE, b"x")
    except InvalidSignature:
        wrong_message_rejected = True
    require(wrong_message_rejected, "wrong message was accepted")

    altered = bytearray(EXPECTED_SIGNATURE)
    altered[0] ^= 0x01
    altered_signature_rejected = False
    try:
        public_key.verify(bytes(altered), b"")
    except InvalidSignature:
        altered_signature_rejected = True
    require(altered_signature_rejected, "altered signature was accepted")

    invalid_lengths = {}
    for length in (31, 33):
        try:
            Ed25519PrivateKey.from_private_bytes(b"\x00" * length)
        except Exception as error:
            invalid_lengths[str(length)] = exception_name(error)
        else:
            raise RuntimeError("invalid private-key length was accepted: " + str(length))

    result = {
        "result": "ED25519_PROVIDER_VERIFIED",
        "provider_version": cryptography.__version__,
        "python_version": sys.version.split()[0],
        "vector": "RFC8032-7.1-TEST-1",
        "tests": {
            "public_key_matches": True,
            "signature_matches": True,
            "signature_verifies": True,
            "wrong_message_rejected": wrong_message_rejected,
            "altered_signature_rejected": altered_signature_rejected,
            "invalid_private_key_lengths_rejected": invalid_lengths,
        },
        "expected_public_key_sha256": hashlib.sha256(EXPECTED_PUBLIC_KEY).hexdigest(),
        "expected_signature_sha256": hashlib.sha256(EXPECTED_SIGNATURE).hexdigest(),
        "loaded_provider_modules": provider_module_paths(),
    }
    sys.stdout.write(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        sys.stdout.write(json.dumps({
            "result": "FAILED",
            "error_type": exception_name(error),
            "error": str(error),
        }, indent=2, sort_keys=True) + "\n")
        raise SystemExit(1)
