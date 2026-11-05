"""Synthetic candidates only. The controller injects the exact protocol module."""
import ast
import unittest


def frame(payload=b'{"ret":null}', index=1):
    body = bytes((0x28, 1)) + index.to_bytes(2, "little") + len(payload).to_bytes(2, "little") + payload
    length = len(body).to_bytes(2, "little")
    return bytes((0xf3, (0xf3 + sum(length)) & 255)) + length + body + bytes((sum(body) & 255, 0xf4))


def change(value, offset, byte):
    output = bytearray(value)
    output[offset] = byte
    return bytes(output)


class ProtocolTests(unittest.TestCase):
    def test_fixture_set_and_checksums(self):
        expected = {
            "REPORTED_SCRIPT": "f30a1700280101001100637962657270692e6765745f627269282959f4",
            "ADDITIVE_SCRIPT": "f30a1700280101001100637962657270692e6765745f627269282984f4",
            "REPORTED_ONLINE": "f3f603000d00010ef4",
            "REPORTED_OFFLINE": "f3f603000d00000ef4",
        }
        self.assertEqual({item.name: protocol.fixture_bytes(item).hex() for item in protocol.Fixture}, expected)
        rules = protocol.checksum_candidates()
        self.assertEqual(rules, {
            "handoff": 0x84, "data_sum": 0x5a, "data_ones": 0xa5,
            "data_twos": 0xa6, "data_xor": 0x18, "script_sum": 0x49,
            "script_ones": 0xb6, "script_twos": 0xb7, "script_xor": 0x09,
        })
        for item in protocol.Fixture:
            script = item.name.endswith("SCRIPT")
            self.assertEqual(protocol.fixture_record(item), {
                "bytes": expected[item.name], "provenance": item.value,
                "packet_class": "TYPE_SCRIPT" if script else "TYPE_ONLINE",
                "assumption": "stated_additive_rule" if item.name == "ADDITIVE_SCRIPT" else "reported_bytes",
                "device_correct_oracle": False, "sensor_related_inert_data": script,
            })
        self.assertNotIn(0x59, rules.values())
        online, offline = (bytes.fromhex(expected[key]) for key in ("REPORTED_ONLINE", "REPORTED_OFFLINE"))
        self.assertEqual(sum(online[4:-2]), online[-2])
        self.assertEqual((sum(offline[4:-2]), offline[-2]), (0x0d, 0x0e))

    def test_closed_builder(self):
        for invalid in ("REPORTED_SCRIPT", b"arbitrary", None):
            with self.assertRaises(TypeError):
                protocol.fixture_bytes(invalid)

    def test_every_split(self):
        sample = frame()
        for split in range(len(sample) + 1):
            stream = protocol.ResponseStream()
            stream.expect(1)
            self.assertEqual(stream.feed(sample[:split]) + stream.feed(sample[split:]), [("json_null", None)])

    def test_complete_frame_invariants(self):
        valid = frame()
        cases = [
            (change(valid, 0, 0), "header"),
            (change(valid, 1, 0), "header_checksum"),
            (bytes.fromhex("f3 f3 00 00"), "outer_length"),
            (bytes.fromhex("f3 f5 01 01"), "outer_length"),
            (change(valid, 4, 0), "packet_type"),
            (change(valid, 5, 0), "mode"),
            (frame(index=2), "index"),
            (change(valid, 8, 0), "inner_length"),
            (change(valid, -2, 0), "payload_checksum"),
            (change(valid, -1, 0), "footer"),
            (valid + b"x", "frame_size"),
            (valid[:-1], "frame_size"),
            (frame(b'{"ret":1,"ret":2}'), "duplicate_key"),
            (frame(b'{"ret":{"x":1,"x":2}}'), "duplicate_key"),
            (frame(b"[]"), "non_object"),
            (frame(b'{"ret":NaN}'), "json_constant"),
            (frame(b'{"ret":null,"extra":0}'), "envelope"),
        ]
        for sample, reason in cases:
            with self.subTest(reason=reason), self.assertRaisesRegex(ValueError, reason):
                protocol.parse_complete(sample, 1)
        with self.assertRaises(UnicodeDecodeError):
            protocol.parse_complete(frame(b'{"ret":"\xff"}'), 1)

    def test_response_grammars(self):
        self.assertEqual(protocol.parse_complete(frame(), 1), ("json_null", None))
        self.assertEqual(protocol.parse_complete(frame(b'{"ret":0}'), 1), ("json_return", 0))
        self.assertEqual(protocol.parse_complete(frame(b'{"err":"SyntaxError"}'), 1), ("device_error", "SyntaxError"))
        sample = frame(b"{'ret': None}")
        self.assertEqual(protocol.parse_complete(sample, 1, python_fixture=True), ("python_none", None))
        with self.assertRaises(ValueError):
            protocol.parse_complete(sample, 1)
        with self.assertRaises(ValueError):
            protocol.parse_complete(frame(), 1, python_fixture=True)

    def test_noise_invalid_headers_and_active_false_header(self):
        stream = protocol.ResponseStream()
        stream.expect(1)
        fake = bytes.fromhex("f3 f9 06 00")
        sample = b"boot" + bytes.fromhex("f3 00 00 00 f3 f3 00 00") + frame(fake) + frame()
        self.assertEqual(stream.feed(sample), [("json_null", None)])
        self.assertEqual(stream.noise, 12)
        self.assertEqual(stream.rejections, ["header_checksum", "outer_length", "header_checksum", "utf8"])

    def test_chunk_boundary_noise(self):
        stream = protocol.ResponseStream()
        self.assertEqual(stream.feed(bytes.fromhex("f3 00 00 00")), [])
        self.assertEqual(stream.noise, 4)
        self.assertEqual(stream.rejections, ["header_checksum"])

    def test_valid_looking_header_in_boot_noise(self):
        stream = protocol.ResponseStream()
        stream.expect(1)
        false_frame = change(frame(index=9), 4, 0x0d)
        self.assertEqual(stream.feed(b"boot" + false_frame[:-1]), [])
        self.assertEqual(stream.rejections, [])
        self.assertEqual(stream.feed(false_frame[-1:] + frame()), [("json_null", None)])
        self.assertEqual(stream.rejections, ["packet_type"])

    def test_header_byte_inside_valid_utf8(self):
        stream = protocol.ResponseStream()
        stream.expect(1)
        # U+C0000 starts with byte F3. A full valid wire header with a
        # bounded length cannot occur raw inside a JSON string because it includes NUL.
        value = chr(0xc0000)
        payload = ('{"ret":"' + value + '"}').encode("utf-8")
        self.assertIn(0xf3, payload)
        self.assertEqual(stream.feed(frame(payload)), [("json_return", value)])
        self.assertEqual(stream.rejections, [])

    def test_bad_retired_frame_reports_integrity_failure(self):
        stream = protocol.ResponseStream()
        stream.expect(1)
        stream.retire()
        stream.expect(2)
        stream.feed(change(frame(), -1, 0) + frame())
        self.assertEqual(stream.rejections, ["footer", "late"])

    def test_active_rejections_recover(self):
        for sample, reason in (
            (change(frame(), 8, 0), "inner_length"),
            (change(frame(), 4, 0), "packet_type"),
            (change(frame(), 5, 0), "mode"),
            (frame(index=2), "index"),
            (change(frame(), -2, 0), "payload_checksum"),
            (change(frame(), -1, 0), "footer"),
            (frame(b"oops"), "json"),
        ):
            stream = protocol.ResponseStream()
            stream.expect(1)
            self.assertEqual(stream.feed(sample + frame()), [("json_null", None)])
            self.assertEqual(stream.rejections, [reason])

    def test_late_stale_duplicate_and_retirement(self):
        stream = protocol.ResponseStream()
        stream.expect(2)
        stream.retire()
        with self.assertRaisesRegex(ValueError, "sequence"):
            stream.expect(2)
        stream.expect(3)
        third = frame(index=3)
        self.assertEqual(stream.feed(frame(index=2) + frame() + third + third), [("json_null", None)])
        self.assertEqual(stream.rejections, ["late", "stale", "duplicate"])

    def test_overflow_is_terminal(self):
        stream = protocol.ResponseStream()
        stream.feed(b"x" * protocol.MAX_STREAM)
        for sample in (b"x", b""):
            with self.assertRaisesRegex(ValueError, "overflow"):
                stream.feed(sample)

    def test_file_specific_ast_boundaries(self):
        common_denials = {
            "eval", "__import__", "getattr", "setattr", "globals", "locals",
            "importlib", "serial", "pyserial", "makeblock", "cyberpi", "socket",
            "connect", "bind", "listen", "send", "sendall", "display", "led",
            "motor", "move", "audio", "play", "repl", "reset", "subscribe",
            "get_bri", "read_sensor", "ctypes", "system", "fork",
        }
        rules = (
            ("protocol", protocol_source, {"enum", "json", "functools", "operator"}),
            ("tests", test_source, {"ast", "unittest"}),
            ("controller", controller_source, {
                "ast", "enum", "functools", "operator", "hashlib", "json", "os",
                "pathlib", "selectors", "stat", "subprocess", "sys", "time",
                "types", "unittest",
            }),
        )
        controller_exceptions = {
            ("git", "subprocess"), ("capture", "subprocess"),
            ("child", "exec"), ("child", "compile"),
            ("checked_bytes", "open"), ("main", "open"),
        }
        for label, source, modules in rules:
            tree = ast.parse(source)
            parents = {child: node for node in ast.walk(tree) for child in ast.iter_child_nodes(node)}
            for node in ast.walk(tree):
                scope = parents.get(node)
                while scope is not None and not isinstance(scope, ast.FunctionDef):
                    scope = parents.get(scope)
                function = scope.name if scope else None
                if isinstance(node, ast.Import):
                    self.assertTrue(all(alias.name in modules and alias.asname is None for alias in node.names))
                if isinstance(node, ast.ImportFrom):
                    self.assertIn(node.module, modules)
                    self.assertEqual(node.level, 0)
                    self.assertTrue(all(alias.asname is None and alias.name != "*" for alias in node.names))
                if isinstance(node, (ast.Name, ast.Attribute)):
                    name = node.id if isinstance(node, ast.Name) else node.attr
                    self.assertNotIn(name.lower(), common_denials)
                    if name in {"subprocess", "exec", "compile", "open"}:
                        self.assertEqual(label, "controller")
                        self.assertIn((function, name), controller_exceptions)
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                    target = node.func
                    if isinstance(target.value, ast.Name) and target.value.id == "subprocess":
                        self.assertIn((function, target.attr), {("git", "check_output"), ("capture", "Popen")})
                if isinstance(node, ast.Constant) and isinstance(node.value, str) and node.value.startswith("/dev/"):
                    if (label, function, node.value) == ("tests", "test_file_specific_ast_boundaries", "/dev/"):
                        continue
                    self.assertEqual(label, "controller")
                    self.assertIn(function, {"audit", "child"})
