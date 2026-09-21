"""Pinned constants for the bounded AAuth fcf656d Steps 1-3 profile."""

AAUTH_COMMIT = "fcf656de1926535f5bd6fc0538147ead6646e727"
AAUTH_PROTOCOL_SHA256 = "295ba2a0edd99dd077c4c877b6276608000419fdf4bbef2327da0c6e4d950953"
JOSE_ALGORITHM = "Ed25519"
TOKEN_TYPES = frozenset({
    "aa-agent+jwt", "aa-person+jwt", "aa-resource+jwt", "aa-auth+jwt",
})
BASE_COMPONENTS = ("@method", "@authority", "@path", "signature-key")
BODY_COMPONENTS = ("content-digest", "content-type")
SIGNATURE_LABEL = "sig"
SIGNATURE_SCHEME = "jwt"
FRESHNESS_SECONDS = 60
FORWARD_SKEW_SECONDS = 60
MAX_FIELD_BYTES = 16_384
MAX_BODY_BYTES = 1_048_576
MAX_MEMBERS = 64
MAX_PARAMETERS = 16
MAX_STRING_BYTES = 8_192
MAX_BYTE_SEQUENCE_BYTES = 8_192
SIGNATURE_ERROR_CODES = frozenset({
    "unsupported_algorithm", "unsupported_scheme", "invalid_input",
    "required_input", "invalid_signature", "clock_skew",
})
