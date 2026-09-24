"""Bounded identifier validation for the transport-free AAuth exchange."""

import re


class IdentifierError(ValueError):
    pass


class OutOfProfileIdentifier(IdentifierError):
    pass


_LOCAL = re.compile(r"^[A-Za-z0-9._+-]{1,255}$")
_LABEL = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?$")


def validate_server_identifier(value):
    if not isinstance(value, str) or not value.startswith("https://"):
        raise IdentifierError("HTTPS server identifier required")
    remainder = value[8:]
    if not remainder or any(character in remainder for character in "/?#@:"):
        raise IdentifierError("server identifier must contain only scheme and host")
    labels = remainder.split(".")
    if len(remainder) > 253 or len(labels) < 2 or any(not _LABEL.fullmatch(label) for label in labels):
        raise IdentifierError("invalid server identifier domain")
    return value


def validate_agent_identifier(value, *, top_level_only=False):
    if not isinstance(value, str) or not value.startswith("aauth:"):
        raise IdentifierError("aauth agent identifier required")
    body = value[6:]
    if body.count("@") != 1:
        raise IdentifierError("agent identifier must contain one at-sign")
    local, domain = body.split("@")
    if not _LOCAL.fullmatch(local):
        raise IdentifierError("invalid agent local part")
    validate_server_identifier("https://" + domain)
    if top_level_only and "+" in local:
        raise OutOfProfileIdentifier("sub-agent identifiers are outside this profile")
    return value

