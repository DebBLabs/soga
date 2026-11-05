"""Offline F3/F4 candidates. No device I/O."""
import json
from enum import Enum
from functools import reduce
from operator import xor

MAX_BODY = 256
MAX_STREAM = 4096
SCRIPT = bytes.fromhex("f3 0a 17 00 28 01 01 00 11 00 63 79 62 65 72 70 69 2e 67 65 74 5f 62 72 69 28 29 59 f4")


class Fixture(Enum):
    REPORTED_SCRIPT = "G readiness vector"
    ADDITIVE_SCRIPT = "G readiness vector rebuilt using stated sum"
    REPORTED_ONLINE = "G online vector"
    REPORTED_OFFLINE = "G offline vector"


def fixture_bytes(name):
    if type(name) is not Fixture:
        raise TypeError("expected Fixture")
    return {
        Fixture.REPORTED_SCRIPT: SCRIPT,
        Fixture.ADDITIVE_SCRIPT: SCRIPT[:-2] + bytes((sum(SCRIPT[4:-2]) & 255, 0xf4)),
        Fixture.REPORTED_ONLINE: bytes.fromhex("f3 f6 03 00 0d 00 01 0e f4"),
        Fixture.REPORTED_OFFLINE: bytes.fromhex("f3 f6 03 00 0d 00 00 0e f4"),
    }[name]


def fixture_record(name):
    raw = fixture_bytes(name)
    return {
        "bytes": raw.hex(),
        "provenance": name.value,
        "packet_class": "TYPE_SCRIPT" if raw[4] == 0x28 else "TYPE_ONLINE",
        "assumption": "stated_additive_rule" if name is Fixture.ADDITIVE_SCRIPT else "reported_bytes",
        "device_correct_oracle": False,
        "sensor_related_inert_data": raw[4] == 0x28,
    }


def checksum_candidates():
    result = {"handoff": sum(SCRIPT[4:-2]) & 255}
    for label, data in (("data", SCRIPT[8:-2]), ("script", SCRIPT[10:-2])):
        total = sum(data)
        result.update({
            label + "_sum": total & 255,
            label + "_ones": ~total & 255,
            label + "_twos": -total & 255,
            label + "_xor": reduce(xor, data, 0),
        })
    return result


def _object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate_key")
        result[key] = value
    return result


def _invalid_constant(value):
    raise ValueError("json_constant")


def _size(header):
    if header[0] != 0xf3:
        raise ValueError("header")
    if header[1] != (0xf3 + header[2] + header[3]) & 255:
        raise ValueError("header_checksum")
    size = int.from_bytes(header[2:4], "little")
    if not 6 <= size <= MAX_BODY:
        raise ValueError("outer_length")
    return size + 6


def parse_complete(frame, expected_index, *, python_fixture=False):
    if type(frame) is not bytes or type(expected_index) is not int or not 1 <= expected_index <= 65535:
        raise ValueError("input")
    if type(python_fixture) is not bool:
        raise ValueError("input")
    index, result = _validated_response(frame, python_fixture)
    if index != expected_index:
        raise ValueError("index")
    return result


def _validated_response(frame, python_fixture):
    if len(frame) < 4 or len(frame) != _size(frame):
        raise ValueError("frame_size")
    if frame[4] != 0x28:
        raise ValueError("packet_type")
    if frame[5] != 1:
        raise ValueError("mode")
    index = int.from_bytes(frame[6:8], "little")
    payload = frame[10:-2]
    if int.from_bytes(frame[8:10], "little") != len(payload):
        raise ValueError("inner_length")
    if frame[-2] != sum(frame[4:-2]) & 255:
        raise ValueError("payload_checksum")
    if frame[-1] != 0xf4:
        raise ValueError("footer")
    value = payload.decode("utf-8")
    if python_fixture:
        if value not in ("{'ret': None}", '{"ret": None}'):
            raise ValueError("python_fixture")
        return index, ("python_none", None)
    obj = json.loads(value, object_pairs_hook=_object, parse_constant=_invalid_constant)
    if type(obj) is not dict:
        raise ValueError("non_object")
    if obj.keys() == {"err"} and type(obj["err"]) is str:
        return index, ("device_error", obj["err"])
    if obj.keys() == {"ret"}:
        return index, (("json_null" if obj["ret"] is None else "json_return"), obj["ret"])
    raise ValueError("envelope")


class ResponseStream:
    """One monotonically advancing sequence per bounded stream lifetime."""
    def __init__(self, *, python_fixture=False):
        if type(python_fixture) is not bool:
            raise ValueError("input")
        self.python_fixture = python_fixture
        self.total = self.noise = 0
        self.rejections = []
        self._buffer = bytearray()
        self._active_size = 0
        self._pending = None
        self._last = 0
        self._retired = {}
        self._overflow = False

    def expect(self, index):
        if type(index) is not int or self._pending is not None or not self._last < index <= 65535:
            raise ValueError("sequence")
        self._pending = self._last = index

    def retire(self):
        if self._pending is None:
            raise ValueError("no_pending_index")
        self._retired[self._pending] = "late"
        self._pending = None

    def _discard_noise(self):
        while self._buffer and self._buffer[0] != 0xf3:
            del self._buffer[0]
            self.noise += 1

    def feed(self, chunk):
        if type(chunk) is not bytes:
            raise ValueError("input")
        if self._overflow or len(chunk) > MAX_STREAM - self.total:
            self._overflow = True
            self._buffer.clear()
            raise ValueError("overflow")
        self.total += len(chunk)
        results = []
        for byte in chunk:
            self._buffer.append(byte)
            if not self._active_size:
                self._discard_noise()
                if len(self._buffer) < 4:
                    continue
                try:
                    self._active_size = _size(self._buffer)
                except ValueError as error:
                    self.rejections.append(str(error))
                    del self._buffer[0]
                    self.noise += 1
                    self._discard_noise()
                    continue
            if len(self._buffer) != self._active_size:
                continue
            frame = bytes(self._buffer)
            self._buffer.clear()
            self._active_size = 0
            try:
                index, result = _validated_response(frame, self.python_fixture)
            except UnicodeDecodeError:
                self.rejections.append("utf8")
            except json.JSONDecodeError:
                self.rejections.append("json")
            except ValueError as error:
                self.rejections.append(str(error))
            else:
                if index != self._pending:
                    reason = self._retired.get(index, "stale" if index < self._last else "index")
                    self.rejections.append(reason)
                    continue
                self._retired[index] = "duplicate"
                self._pending = None
                results.append(result)
        return results
