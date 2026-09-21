"""Bounded RFC 9651 subset used by the pinned AAuth request profile.

Duplicate rejection is an explicit stricter SOGA anti-smuggling rule, not an
RFC 9651 conformance claim.
"""

import base64
import binascii
from dataclasses import dataclass

from . import profile

DIGITS = "0123456789"


class StructuredFieldError(ValueError):
    pass


@dataclass(frozen=True)
class Item:
    value: object
    parameters: tuple = ()


@dataclass(frozen=True)
class InnerList:
    items: tuple
    parameters: tuple = ()


@dataclass(frozen=True)
class Token:
    value: str


def _fail(message):
    raise StructuredFieldError(message)


class _Parser:
    def __init__(self, value):
        if not isinstance(value, str):
            _fail("field must be text")
        if len(value.encode("utf-8")) > profile.MAX_FIELD_BYTES:
            _fail("field exceeds byte limit")
        self.value = value
        self.index = 0

    def done(self):
        return self.index == len(self.value)

    def peek(self):
        return self.value[self.index] if not self.done() else None

    def take(self):
        if self.done():
            _fail("unexpected end of field")
        result = self.value[self.index]
        self.index += 1
        return result

    def expect(self, expected):
        if self.take() != expected:
            _fail("unexpected character")

    def spaces(self):
        while self.peek() == " ":
            self.index += 1

    def key(self):
        start = self.index
        allowed = "abcdefghijklmnopqrstuvwxyz0123456789_.*-"
        while self.peek() is not None and self.peek() in allowed:
            self.index += 1
        key = self.value[start:self.index]
        if not key or key[0] not in "abcdefghijklmnopqrstuvwxyz*":
            _fail("invalid key")
        return key

    def token(self):
        start = self.index
        first = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz*"
        rest = first + "0123456789!#$%&'*+-.^_`|~:/"
        if self.peek() is None or self.peek() not in first:
            _fail("invalid token")
        self.index += 1
        while self.peek() is not None and self.peek() in rest:
            self.index += 1
        return Token(self.value[start:self.index])

    def bare(self):
        current = self.peek()
        if current == '"':
            self.take()
            output = []
            output_bytes = 0
            while self.peek() != '"':
                char = self.take()
                if char == "\\":
                    char = self.take()
                    if char not in ('"', "\\"):
                        _fail("invalid string escape")
                if ord(char) < 0x20 or ord(char) > 0x7E:
                    _fail("invalid string character")
                output.append(char)
                output_bytes += 1
                if output_bytes > profile.MAX_STRING_BYTES:
                    _fail("string exceeds limit")
            self.take()
            return "".join(output)
        if current == ":":
            self.take()
            start = self.index
            while self.peek() not in (":", None):
                self.index += 1
            encoded = self.value[start:self.index]
            self.expect(":")
            try:
                decoded = base64.b64decode(encoded, validate=True)
            except (binascii.Error, ValueError):
                _fail("invalid byte sequence")
            if len(decoded) > profile.MAX_BYTE_SEQUENCE_BYTES:
                _fail("byte sequence exceeds limit")
            return decoded
        if current == "?":
            self.take()
            value = self.take()
            if value not in "01":
                _fail("invalid boolean")
            return value == "1"
        if current == "-" or (current is not None and current in DIGITS):
            start = self.index
            if current == "-":
                self.index += 1
            digits = self.index
            while self.peek() is not None and self.peek() in DIGITS:
                self.index += 1
            if digits == self.index:
                _fail("invalid integer")
            value = int(self.value[start:self.index])
            if not -(10 ** 15 - 1) <= value <= 10 ** 15 - 1:
                _fail("integer out of range")
            return value
        return self.token()

    def parameters(self):
        output = []
        seen = set()
        while self.peek() == ";":
            self.take()
            key = self.key()
            if key in seen:
                _fail("duplicate parameter")
            seen.add(key)
            value = True
            if self.peek() == "=":
                self.take()
                value = self.bare()
            output.append((key, value))
            if len(output) > profile.MAX_PARAMETERS:
                _fail("too many parameters")
        return tuple(output)

    def item(self):
        return Item(self.bare(), self.parameters())

    def member(self):
        if self.peek() != "(":
            return self.item()
        self.take()
        items = []
        while True:
            self.spaces()
            if self.peek() == ")":
                self.take()
                break
            items.append(self.item())
            if len(items) > profile.MAX_MEMBERS:
                _fail("too many inner-list items")
            if self.peek() not in (" ", ")"):
                _fail("invalid inner-list separator")
        return InnerList(tuple(items), self.parameters())


def parse_dictionary(value):
    parser = _Parser(value)
    output = []
    seen = set()
    while True:
        parser.spaces()
        key = parser.key()
        if key in seen:
            _fail("duplicate dictionary key")
        seen.add(key)
        member = Item(True)
        if parser.peek() == "=":
            parser.take()
            member = parser.member()
        else:
            member = Item(True, parser.parameters())
        output.append((key, member))
        if len(output) > profile.MAX_MEMBERS:
            _fail("too many dictionary members")
        parser.spaces()
        if parser.done():
            return tuple(output)
        parser.expect(",")


def parse_item(value):
    parser = _Parser(value)
    item = parser.item()
    if not parser.done():
        _fail("trailing input")
    return item


def _serialize_bare(value):
    if value is True:
        return "?1"
    if value is False:
        return "?0"
    if isinstance(value, int):
        if not -(10 ** 15 - 1) <= value <= 10 ** 15 - 1:
            _fail("integer out of range")
        return str(value)
    if isinstance(value, bytes):
        if len(value) > profile.MAX_BYTE_SEQUENCE_BYTES:
            _fail("byte sequence exceeds limit")
        return ":" + base64.b64encode(value).decode("ascii") + ":"
    if isinstance(value, Token):
        allowed = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!#$%&'*+-.^_`|~:/"
        if (not value.value or value.value[0] not in
                "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz*" or
                any(char not in allowed for char in value.value)):
            _fail("empty token")
        return value.value
    if isinstance(value, str):
        if (len(value.encode("utf-8")) > profile.MAX_STRING_BYTES or
                any(ord(char) < 0x20 or ord(char) > 0x7E for char in value)):
            _fail("invalid or oversized string")
        escaped = value.replace("\\", "\\\\").replace('"', '\\"')
        return '"' + escaped + '"'
    _fail("unsupported bare item")


def _serialize_parameters(parameters):
    seen = set()
    output = []
    for key, value in parameters:
        if key in seen:
            _fail("duplicate parameter")
        seen.add(key)
        suffix = ";" + key
        if value is not True:
            suffix += "=" + _serialize_bare(value)
        output.append(suffix)
    return "".join(output)


def serialize_item(item):
    return _serialize_bare(item.value) + _serialize_parameters(item.parameters)


def serialize_member(member):
    if isinstance(member, Item):
        return serialize_item(member)
    if isinstance(member, InnerList):
        return "(" + " ".join(serialize_item(item) for item in member.items) + ")" + _serialize_parameters(member.parameters)
    _fail("unsupported member")


def serialize_dictionary(members):
    seen = set()
    output = []
    for key, member in members:
        if key in seen:
            _fail("duplicate dictionary key")
        seen.add(key)
        if isinstance(member, Item) and member.value is True:
            output.append(key + _serialize_parameters(member.parameters))
        else:
            output.append(key + "=" + serialize_member(member))
    return ", ".join(output)
