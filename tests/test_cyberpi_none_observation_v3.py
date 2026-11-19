"""Synthetic fake I/O only. Controller injects observation and protocol modules."""
import json
import unittest


class FakeIO:
    def __init__(self):
        self.now = 0.0
        self.open_count = self.close_count = self.write_count = 0
        self.boot_data = b""
        self.response = b""
        self.written = 16
        self.quiet = True
        self.valid_identity = True
        self.close_error = False
        self.read_error = None
        self.write_error = None

    def open_once(self):
        self.open_count += 1

    def identity_ok(self):
        return self.valid_identity

    def read(self, timeout, limit):
        self.now += timeout
        if self.read_error:
            raise self.read_error
        if self.write_count:
            data, self.response = self.response[:limit], self.response[limit:]
            return data
        if not self.quiet:
            return b"x"
        data, self.boot_data = self.boot_data[:limit], self.boot_data[limit:]
        return data

    def write_once(self, data, timeout):
        self.write_count += 1
        self.asserted_frame = data
        self.write_at = self.now
        if self.write_error:
            raise self.write_error
        return self.written

    def close_once(self):
        self.close_count += 1
        if self.close_error:
            raise OSError("close")


def response_frame(payload, mode=1, index=1):
    body = bytes((0x28, mode)) + index.to_bytes(2, "little") + len(payload).to_bytes(2, "little") + payload
    length = len(body).to_bytes(2, "little")
    return bytes((0xf3, (0xf3 + sum(length)) & 255)) + length + body + bytes((sum(body) & 255, 0xf4))


class ObservationTests(unittest.TestCase):
    def run_fake(self, io):
        result = observation.observe(io, lambda: io.now, lambda data: observation.classify_response(data, protocol))
        self.assertEqual(io.open_count, 1)
        self.assertEqual(io.close_count, 1)
        self.assertLessEqual(io.write_count, 1)
        return result

    def test_silence_full_boot_and_single_write(self):
        io = FakeIO()
        result = self.run_fake(io)
        self.assertGreaterEqual(io.write_at, 12.0)
        self.assertEqual(io.asserted_frame.hex(), "f3fd0a002801010004004e6f6e65bef4")
        self.assertEqual(result["outcome"], "silence")

    def test_json_null_python_none_error_and_bad_grammar(self):
        for payload, kind in ((b'{"ret":null}', "json_null"), (b"{'ret': None}", "python_none"),
                              (b'{"err":"SyntaxError"}', "device_error"), (b"garbage", "unparseable")):
            with self.subTest(payload=payload):
                io = FakeIO()
                io.response = response_frame(payload)
                self.assertEqual(self.run_fake(io)["interpretation"]["kind"], kind)

    def test_wrong_mode_and_index_preserve_raw(self):
        for mode, index in ((0, 1), (1, 2)):
            io = FakeIO()
            io.response = response_frame(b'{"ret":null}', mode, index)
            result = self.run_fake(io)
            self.assertEqual(result["interpretation"]["kind"], "unparseable")
            self.assertEqual(result["response_hex"], io.response.hex() if io.response else response_frame(b'{"ret":null}', mode, index).hex())

    def test_boot_limit_aborts_without_write(self):
        io = FakeIO()
        io.boot_data = b"x" * 4096
        self.assertIn("boot_limit_no_write", self.run_fake(io)["error"])
        self.assertEqual(io.write_count, 0)

    def test_active_boot_at_deadline_aborts_without_write(self):
        io = FakeIO()
        io.quiet = False
        self.assertIn("boot_not_quiet_no_write", self.run_fake(io)["error"])
        self.assertEqual(io.write_count, 0)

    def test_partial_and_eagain_never_retry(self):
        for written, error in ((3, None), (16, BlockingIOError("EAGAIN"))):
            io = FakeIO()
            io.written, io.write_error = written, error
            self.assertEqual(self.run_fake(io)["outcome"], "aborted")
            self.assertEqual(io.write_count, 1)

    def test_read_signal_and_identity_aborts_close(self):
        for error in (OSError("read"), observation.ObservationAbort("SIGINT"), observation.ObservationAbort("SIGTERM")):
            io = FakeIO()
            io.read_error = error
            self.assertEqual(self.run_fake(io)["outcome"], "aborted")
            self.assertEqual(io.write_count, 0)
        io = FakeIO()
        io.valid_identity = False
        self.assertIn("device_changed", self.run_fake(io)["error"])

    def test_response_limit_preserves_bytes(self):
        io = FakeIO()
        io.response = b"x" * 1024
        result = self.run_fake(io)
        self.assertEqual(len(bytes.fromhex(result["response_hex"])), 1024)
        self.assertIn("response_limit", result["error"])

    def test_close_failure_is_not_success(self):
        io = FakeIO()
        io.close_error = True
        result = self.run_fake(io)
        self.assertEqual(result["outcome"], "aborted")
        self.assertTrue(result["close"].startswith("failed:"))

    def test_wall_budget_prevents_write(self):
        io = FakeIO()
        original_open = io.open_once
        def slow_open():
            original_open()
            io.now = 19.0
        io.open_once = slow_open
        result = self.run_fake(io)
        self.assertEqual(result["outcome"], "aborted")
        self.assertEqual(io.write_count, 0)


class SerialLayerTests(unittest.TestCase):
    def setUp(self):
        from types import SimpleNamespace
        from unittest.mock import Mock
        self.config = [99, 99, 1 | 2 | 4 | 8 | 16, 99, 0, 0, [1, 1]]
        self.os = SimpleNamespace(
            O_RDWR=1, O_NOCTTY=2, O_NONBLOCK=4, O_NOFOLLOW=8,
            lstat=Mock(return_value=SimpleNamespace(st_mode=10, st_rdev=7)),
            fstat=Mock(return_value=SimpleNamespace(st_mode=10, st_rdev=7)),
            open=Mock(return_value=4), read=Mock(return_value=b"x"),
            write=Mock(return_value=16), close=Mock(),
        )
        self.termios = SimpleNamespace(
            HUPCL=1, CSIZE=2, PARENB=4, CSTOPB=8, CRTSCTS=16, CS8=32,
            CLOCAL=64, CREAD=128, B115200=115200, VMIN=0, VTIME=1, TCSANOW=0,
            tcgetattr=Mock(return_value=self.config), tcsetattr=Mock(),
        )
        selector = Mock()
        selector.select.return_value = [("ready",)]
        selector.__enter__ = Mock(return_value=selector)
        selector.__exit__ = Mock(return_value=False)
        self.selector = selector
        self.selectors = SimpleNamespace(DefaultSelector=Mock(return_value=selector), EVENT_READ=1, EVENT_WRITE=2)
        self.stat = SimpleNamespace(S_ISCHR=lambda mode: mode == 10)
        self.io = observation.SerialIO("/dev/cu.fake", 7, os_api=self.os,
            termios_api=self.termios, selectors_api=self.selectors, stat_api=self.stat)

    def test_raw_config_retains_hupcl_and_exact_open_flags(self):
        self.io.open_once()
        self.os.open.assert_called_once_with("/dev/cu.fake", 15)
        self.assertEqual(self.config[:2], [0, 0])
        self.assertEqual(self.config[3:], [0, 115200, 115200, [0, 0]])
        self.assertEqual(self.config[2], 1 | 32 | 64 | 128)
        self.assertTrue(self.io.hupcl)
        self.io.close_once()
        self.os.close.assert_called_once_with(4)
        with self.assertRaisesRegex(RuntimeError, "duplicate_close"):
            self.io.close_once()

    def test_duplicate_open_and_identity_changes(self):
        self.io.open_once()
        with self.assertRaisesRegex(RuntimeError, "open_preflight_failed"):
            self.io.open_once()
        self.os.fstat.return_value.st_rdev = 8
        self.assertFalse(self.io.identity_ok())
        self.io.close_once()

    def test_write_timeout_short_and_eagain_do_not_repeat_syscall(self):
        self.io.open_once()
        self.selector.select.return_value = []
        with self.assertRaisesRegex(TimeoutError, "write_not_ready"):
            self.io.write_once(observation.FRAME, 0.5)
        self.os.write.assert_not_called()
        self.assertFalse(self.io.syscall_attempted)
        self.selector.select.return_value = [("ready",)]
        self.os.write.return_value = 3
        self.assertEqual(self.io.write_once(observation.FRAME, 0.5), 3)
        self.os.write.assert_called_once()
        self.os.write.reset_mock()
        self.os.write.side_effect = BlockingIOError("EAGAIN")
        with self.assertRaises(BlockingIOError):
            self.io.write_once(observation.FRAME, 0.5)
        self.os.write.assert_called_once()
        self.io.close_once()

    def test_config_failure_is_closed_by_algorithm(self):
        self.termios.tcsetattr.side_effect = OSError("configure")
        result = observation.observe(self.io, lambda: 0.0, lambda raw: {})
        self.assertEqual(result["outcome"], "aborted")
        self.os.close.assert_called_once_with(4)
        self.assertEqual(result["close"], "closed")

    def test_eof_is_an_abort_not_an_empty_poll(self):
        self.io.open_once()
        self.os.read.return_value = b""
        with self.assertRaisesRegex(EOFError, "device_eof"):
            self.io.read(0.05, 4)
        self.io.close_once()


    def test_expiry_in_open_seam_makes_no_syscall(self):
        def refuse():
            observation.check_open({"observed_at": 100}, {"approved_at": 101, "expires_at": 120},
                                   (110, 10), 20, (120, 20))
        self.io.before_open = refuse
        result = observation.observe(self.io, lambda: 0.0, lambda raw: {})
        self.assertEqual(result["outcome"], "aborted")
        self.os.open.assert_not_called()
        self.os.write.assert_not_called()

    def test_changed_fd_is_closed_without_configuration_or_write(self):
        self.os.fstat.return_value.st_rdev = 8
        result = observation.observe(self.io, lambda: 0.0, lambda raw: {})
        self.assertEqual(result["outcome"], "aborted")
        self.os.open.assert_called_once()
        self.os.close.assert_called_once()
        self.termios.tcsetattr.assert_not_called()
        self.os.write.assert_not_called()

    def test_selector_and_fd_close_failures_are_both_reported(self):
        self.io.open_once()
        self.selector.close.side_effect = OSError("selector")
        self.os.close.side_effect = OSError("fd")
        with self.assertRaisesRegex(RuntimeError, "selector:OSError,fd:OSError"):
            self.io.close_once()
        self.os.close.assert_called_once()


class PhysicalGateTests(unittest.TestCase):
    def setUp(self):
        self.preflight = {
            "confirmed_by": "Deb", "attempt_id": "reviewed-attempt", "host": "reviewed-host",
            "observed_at": 100.0, "device_path": "/dev/cu.fake", "device_rdev": 7,
            "unit_claim": "selected-unit", "firmware_claim": "44.01.016",
            "standalone_observed_seconds": 15, "no_wheel_motion_or_sound_observed": True,
            "wheels_raised": True, "power_controls_accessible": True, "motor_power_off": True,
            "usb_logic_power_confirmed": True, "no_competing_owner": True,
            "battery_startup_visual_baseline": observation.BATTERY_VISUAL_BASELINE,
            "boot_baseline_record": json.dumps({
                "duration_seconds": 15, "screen": "Startup flash followed by blank screen.",
                "lights": "White near wheels and blue eye flashes observed.",
            }),
            "misty_units": [{"unit": "Misty B", "state": "powered_off", "excluded": True}],
        }
        self.metadata = {"canonical": True, "parent": "/dev", "name": "cu.fake", "character": True, "rdev": 7}

    def test_preflight_refuses_each_missing_safety_hold(self):
        observation.validate_preflight(self.preflight, 100.0, self.metadata)
        for key in ("no_wheel_motion_or_sound_observed", "wheels_raised", "power_controls_accessible",
                    "motor_power_off", "usb_logic_power_confirmed", "no_competing_owner"):
            with self.subTest(key=key), self.assertRaisesRegex(RuntimeError, "preflight_hold"):
                observation.validate_preflight(self.preflight | {key: False}, 100.0, self.metadata)

    def test_stale_future_short_boot_and_wrong_device_refused(self):
        for update, now, metadata, error in (
            ({"observed_at": -21}, 100, self.metadata, "stale_preflight"),
            ({"observed_at": 101}, 100, self.metadata, "stale_preflight"),
            ({"standalone_observed_seconds": 14}, 100, self.metadata, "stored_boot_observation"),
            ({}, 100, self.metadata | {"canonical": False}, "device_path_required"),
            ({}, 100, self.metadata | {"character": False}, "device_identity_mismatch"),
            ({}, 100, self.metadata | {"rdev": 8}, "device_identity_mismatch"),
        ):
            with self.subTest(error=error), self.assertRaisesRegex(RuntimeError, error):
                observation.validate_preflight(self.preflight | update, now, metadata)

    def test_previous_animation_hold_schema_is_rejected(self):
        previous = dict(self.preflight)
        del previous["battery_startup_visual_baseline"]
        previous["no_motion_sound_animation"] = previous.pop("no_wheel_motion_or_sound_observed")
        with self.assertRaisesRegex(RuntimeError, "preflight_schema"):
            observation.validate_preflight(previous, 100, self.metadata)

    def test_visual_baseline_is_exact_and_motion_sound_hold_is_literal(self):
        for baseline in ("quiet", "", None, True):
            with self.subTest(baseline=baseline), self.assertRaisesRegex(RuntimeError, "battery_visual_baseline_required"):
                observation.validate_preflight(self.preflight | {"battery_startup_visual_baseline": baseline}, 100, self.metadata)
        for hold in (False, 1, "true", None):
            with self.subTest(hold=hold), self.assertRaisesRegex(RuntimeError, "preflight_hold"):
                observation.validate_preflight(self.preflight | {"no_wheel_motion_or_sound_observed": hold}, 100, self.metadata)

    def test_boot_record_requires_measured_duration_and_both_narratives(self):
        good = json.loads(self.preflight["boot_baseline_record"])
        for update in ({"duration_seconds": True}, {"duration_seconds": 16},
                       {"duration_seconds": float("nan")}, {"screen": ""},
                       {"lights": "not observed"}, {"screen": observation.BATTERY_VISUAL_BASELINE},
                       {"extra": "field"}):
            with self.subTest(update=update), self.assertRaisesRegex(RuntimeError, "boot_baseline_"):
                observation.validate_preflight(self.preflight | {"boot_baseline_record": json.dumps(good | update)}, 100, self.metadata)
        for raw in ("static baseline", "{}", "null", '{"duration_seconds":15,"duration_seconds":15,"screen":"observed flash","lights":"observed lights"}'):
            with self.subTest(raw=raw), self.assertRaisesRegex(RuntimeError, "boot_baseline_"):
                observation.validate_preflight(self.preflight | {"boot_baseline_record": raw}, 100, self.metadata)

    def test_authority_exact_request_risk_and_attempt_count(self):
        authority = {"stable_request_sha256": "hash", "preflight_sha256": "facts",
                     "attempt_id": "reviewed-attempt", "approved_by": "Deb", "attempts": 1,
                     "approval_reference": "approval", "approved_at": 101, "expires_at": 120,
                     "accept_candidate_uncertainty": True, "accept_reset_uncertainty": True}

        def validate(record, verify):
            observation.validate_authority(record, "hash", "facts", "reviewed-attempt", verify)

        validate(authority, lambda: True)
        for change in ({"stable_request_sha256": "other"}, {"preflight_sha256": "other"},
                       {"attempt_id": "other"}, {"attempts": 2}, {"attempts": True},
                       {"approval_reference": ""}, {"accept_reset_uncertainty": False}, {"extra": True}):
            with self.subTest(change=change), self.assertRaisesRegex(RuntimeError, "physical_authority_required"):
                validate(authority | change, lambda: self.fail("invalid record reached signature verification"))
        for invalid in (False, 1, None):
            with self.subTest(invalid=invalid), self.assertRaisesRegex(RuntimeError, "approval_signature_required"):
                validate(authority, lambda: invalid)

    def test_host_unit_firmware_and_exclusions_bind_exactly(self):
        request = dict(self.preflight)
        observation.validate_binding(self.preflight, request)
        for key in ("host", "attempt_id", "unit_claim", "firmware_claim", "misty_units"):
            with self.subTest(key=key), self.assertRaisesRegex(RuntimeError, "preflight_binding_mismatch"):
                observation.validate_binding(self.preflight, request | {key: "other"})

    def test_expiry_after_pins_and_early_cutoff(self):
        authority = {"approved_at": 101, "expires_at": 120}
        self.assertEqual(observation.open_cutoff(self.preflight, authority, (102, 2), (110, 10)), 20)
        with self.assertRaisesRegex(RuntimeError, "preflight_or_approval_expired"):
            observation.open_cutoff(self.preflight, authority, (102, 2), (120, 20))
        with self.assertRaisesRegex(RuntimeError, "monotonic_open_cutoff"):
            observation.check_open(self.preflight, authority, (110, 10), 19.5, (119.5, 19.5))

    def test_sleep_jumps_and_rollback_are_rejected(self):
        authority = {"approved_at": 101, "expires_at": 120}
        for sample in ((119, 10), (111, 15), (109, 11), (110, 9), (121, 11)):
            with self.subTest(sample=sample), self.assertRaisesRegex(RuntimeError, "clock_discontinuity"):
                observation.check_open(self.preflight, authority, (110, 10), 20, sample)

    def test_invalid_clocks_and_timestamps_are_rejected(self):
        authority = {"approved_at": 101, "expires_at": 120}
        for sample in ((True, 10), (110, float("nan")), (float("inf"), 10), (110, -1)):
            with self.subTest(sample=sample), self.assertRaisesRegex(RuntimeError, "invalid_clock_sample"):
                observation.remaining(self.preflight, authority, sample)
        for timestamp in (True, float("nan"), float("inf"), "120"):
            with self.subTest(timestamp=timestamp), self.assertRaisesRegex(RuntimeError, "invalid_gate_timestamp"):
                observation.remaining(self.preflight, authority | {"expires_at": timestamp}, (110, 10))

    def test_reservation_failures_prevent_metadata_work(self):
        steps = []
        def step(name, fail):
            steps.append(name)
            if name == fail:
                raise OSError(name)

        for fail, expected in (("mkdir", ["mkdir"]), ("record", ["mkdir", "record"]),
                               ("fsync", ["mkdir", "record", "fsync"])):
            steps.clear()
            with self.subTest(fail=fail), self.assertRaises(OSError):
                observation.reserve_attempt(lambda: step("mkdir", fail), lambda: step("record", fail),
                                            lambda: step("fsync", fail))
                step("metadata", fail)
            self.assertEqual(steps, expected)
        steps.clear()
        observation.reserve_attempt(lambda: step("mkdir", None), lambda: step("record", None),
                                    lambda: step("fsync", None))
        step("metadata", None)
        self.assertEqual(steps, ["mkdir", "record", "fsync", "metadata"])

    def test_physical_limits_match_reviewed_manifest(self):
        self.assertEqual(observation.physical_limits(), manifest_limits)

    def test_worker_inventory_and_missing_worker_report_fail_closed(self):
        observation.check_inventory(["stdlib"], {"stdlib"})
        with self.assertRaisesRegex(RuntimeError, "unlisted_loaded_runtime"):
            observation.check_inventory(["stdlib", "unexpected"], {"stdlib"})

        def invalid_json(raw):
            raise ValueError("partial")
        self.assertIsNone(observation.worker_report(b"partial", invalid_json))
        self.assertIsNone(observation.worker_report(b"{}", lambda raw: {}))

        def duplicate_key(raw):
            raise RuntimeError("duplicate_key")
        self.assertIsNone(observation.worker_report(b"duplicate", duplicate_key))

    def test_parent_abort_grace_for_both_signals_at_each_phase(self):
        for signum in (2, 15):
            for phase in ("boot", "response", "close"):
                with self.subTest(signum=signum, phase=phase):
                    policy = observation.AbortPolicy()
                    self.assertEqual(policy.action(1.0, 20.0), "continue")
                    policy.receive(signum)
                    self.assertEqual(policy.action(2.0, 20.0), "forward")
                    self.assertEqual(policy.action(2.5, 20.0), "wait")
                    policy.receive(2)
                    self.assertEqual(policy.signum, signum)
                    self.assertEqual(policy.action(3.0, 20.0), "kill")
                    self.assertEqual(policy.action(20.0, 20.0), "kill")
                    # A kill means raw-loss/unknown close, never a clean-close claim.
