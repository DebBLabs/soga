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
            "confirmed_by": "Deb", "attempt_id": "cyberpi-none-v3-physical-reviewed-attempt",
            "host": "reviewed-host", "observed_at": 100.0,
            "device_path": "/dev/cu.fake", "device_rdev": 7,
            "unit_claim": "selected-unit", "firmware_claim": "44.01.016",
            "wheels_raised": True, "power_controls_accessible": True, "no_competing_owner": True,
            "misty_units": [dict(unit) for unit in observation.MISTY_UNITS],
            "shield_switch_off": True, "motor_connection_state": "connected_no_isolation_claim",
            "support_configuration": "assembled_freely_resting_passive_support",
            "usb_connection_state_at_approval": "disconnected",
            "usb_startup_evidence_sha256": observation.USB_STARTUP_EVIDENCE_SHA256,
            "device_identity_basis": "prior_passive_record_rechecked_at_open",
            "device_identity_record_sha256": "a" * 64, "support_clearance_confirmed": True,
            "accept_connected_motor_uncertainty": True,
            "accept_freely_resting_support_uncertainty": True,
            "accept_usb_stop_uncertainty": True, "serial_topology_unambiguous": True,
            "accept_shield_on_battery_program_uncertainty": True,
        }
        self.metadata = {"canonical": True, "parent": "/dev", "name": "cu.fake", "character": True, "rdev": 7}
        self.request = {key: self.preflight[key] for key in
                        ("host", "attempt_id", "unit_claim", "firmware_claim", "misty_units",
                         "device_identity_record_sha256")}
        self.request.update(execution_policy=observation.EXECUTION_POLICY)
        self.identity = {
            "schema": "cyberpi-passive-identity-v1", "confirmed_by": "Deb",
            "host": "reviewed-host", "unit_claim": "selected-unit",
            "device_path": "/dev/cu.fake", "device_rdev": 7, "observed_at": 90,
            "method": "manual_usb_namespace_metadata_no_serial_open",
            "approval_reference": "prior-manual-session", "namespace_unambiguous": True,
        }
        self.authority = {
            "stable_request_sha256": "b" * 64, "preflight_sha256": "c" * 64,
            "attempt_id": self.preflight["attempt_id"], "approved_by": "Deb", "attempts": 1,
            "approval_reference": observation.APPROVAL_REFERENCE_PREFIX + "actual-approval",
            "approved_at": 101, "expires_at": 120,
            "accept_candidate_uncertainty": True, "accept_reset_uncertainty": True,
        }

    def test_cold_preflight_requires_each_literal_hold(self):
        # No node metadata exists at cold approval; actual-open validation is separate.
        observation.validate_preflight(self.preflight, 100)
        observation.validate_preflight(self.preflight, 100, self.metadata)
        for key in ("wheels_raised", "power_controls_accessible", "no_competing_owner",
                    "shield_switch_off", "support_clearance_confirmed", "accept_connected_motor_uncertainty",
                    "accept_freely_resting_support_uncertainty", "accept_usb_stop_uncertainty",
                    "serial_topology_unambiguous", "accept_shield_on_battery_program_uncertainty"):
            for value in (False, 1, "true", None):
                with self.subTest(key=key, value=value), self.assertRaisesRegex(RuntimeError, "preflight_hold"):
                    observation.validate_preflight(self.preflight | {key: value}, 100)

    def test_exact_cold_schema_rejects_missing_legacy_and_extra_fields(self):
        for key in self.preflight:
            missing = dict(self.preflight)
            del missing[key]
            with self.subTest(missing=key), self.assertRaisesRegex(RuntimeError, "preflight_schema"):
                observation.validate_preflight(missing, 100)
        for key in ("motor_power_off", "usb_logic_power_confirmed", "standalone_observed_seconds",
                    "no_wheel_motion_or_sound_observed", "boot_baseline_record",
                    "battery_startup_visual_baseline", "no_motion_sound_animation", "extra"):
            with self.subTest(legacy=key), self.assertRaisesRegex(RuntimeError, "preflight_schema"):
                observation.validate_preflight(self.preflight | {key: True}, 100)

    def test_configuration_and_reference_modes_are_exact(self):
        for key in ("motor_connection_state", "support_configuration", "usb_connection_state_at_approval",
                    "device_identity_basis", "usb_startup_evidence_sha256"):
            for value in ("other", "", True, None):
                with self.subTest(key=key, value=value), self.assertRaisesRegex(RuntimeError, "preflight_policy"):
                    observation.validate_preflight(self.preflight | {key: value}, 100)
        for value in ("a", "A" * 64, "g" * 64, True, None):
            with self.subTest(digest=value), self.assertRaisesRegex(RuntimeError, "prior_identity_digest_required"):
                observation.validate_preflight(self.preflight | {"device_identity_record_sha256": value}, 100)

    def test_stale_future_and_actual_device_changes_refuse(self):
        for timestamp in (-21, 101, True, float("nan"), float("inf"), "100"):
            with self.subTest(timestamp=timestamp), self.assertRaisesRegex(RuntimeError, "stale_preflight"):
                observation.validate_preflight(self.preflight | {"observed_at": timestamp}, 100)
        for metadata, error in ((self.metadata | {"canonical": False}, "device_path_required"),
                                (self.metadata | {"character": False}, "device_identity_mismatch"),
                                (self.metadata | {"rdev": 8}, "device_identity_mismatch")):
            with self.subTest(metadata=metadata), self.assertRaisesRegex(RuntimeError, error):
                observation.validate_preflight(self.preflight, 100, metadata)
        for path in ("/dev/cu.", "/dev/cu.fake/other", "/tmp/cu.fake", "/dev/cu.bad name"):
            with self.subTest(path=path), self.assertRaisesRegex(RuntimeError, "device_path_required"):
                observation.validate_preflight(self.preflight | {"device_path": path}, 100)
        for rdev in (True, -1, "7"):
            with self.subTest(rdev=rdev), self.assertRaisesRegex(RuntimeError, "device_identity_mismatch"):
                observation.validate_preflight(self.preflight | {"device_rdev": rdev}, 100)

    def test_misty_inventory_rejects_missing_or_nonliteral_exclusion(self):
        for units in ([], self.preflight["misty_units"][:1],
                      [self.preflight["misty_units"][0] | {"excluded": 1}, self.preflight["misty_units"][1]]):
            with self.subTest(units=units), self.assertRaisesRegex(RuntimeError, "misty_inventory_required"):
                observation.validate_preflight(self.preflight | {"misty_units": units}, 100)

    def test_authority_exact_request_risk_and_attempt_count(self):
        def validate(record, verify):
            observation.validate_authority(record, "b" * 64, "c" * 64, self.preflight["attempt_id"], verify)
        validate(self.authority, lambda: True)
        for change in ({"stable_request_sha256": "d" * 64}, {"preflight_sha256": "e" * 64},
                       {"attempt_id": "other"}, {"attempts": 2}, {"attempts": True},
                       {"approval_reference": ""}, {"accept_reset_uncertainty": False},
                       {"approved_at": True}, {"approved_at": 120}, {"expires_at": 222}, {"extra": True}):
            with self.subTest(change=change), self.assertRaisesRegex(RuntimeError, "physical_authority_required"):
                validate(self.authority | change, lambda: self.fail("invalid record reached verifier"))
        for invalid in (False, 1, None):
            with self.subTest(invalid=invalid), self.assertRaisesRegex(RuntimeError, "approval_signature_required"):
                validate(self.authority, lambda: invalid)

    def test_signer_token_constraints_and_scope_prefix(self):
        for reference in (observation.APPROVAL_REFERENCE_PREFIX, "old-approval", "x" * 129,
                          "cold-sign-lifted-connected-stop-uncertain-v1.actual-approval",
                          observation.APPROVAL_REFERENCE_PREFIX + "bad space", "é"):
            with self.subTest(reference=reference), self.assertRaisesRegex(RuntimeError, "physical_authority_required"):
                observation.validate_authority(self.authority | {"approval_reference": reference},
                                               "b" * 64, "c" * 64, self.preflight["attempt_id"], lambda: True)
        for attempt in ("old-attempt", "cyberpi-none-v3-physical-", "x" * 129):
            with self.subTest(attempt=attempt), self.assertRaisesRegex(RuntimeError, "physical_authority_required"):
                observation.validate_authority(self.authority | {"attempt_id": attempt},
                                               "b" * 64, "c" * 64, attempt, lambda: True)
        reference = observation.APPROVAL_REFERENCE_PREFIX + "x" * (128 - len(observation.APPROVAL_REFERENCE_PREFIX))
        observation.validate_authority(self.authority | {"approval_reference": reference},
                                       "b" * 64, "c" * 64, self.preflight["attempt_id"], lambda: True)

    def test_all_cold_identity_bindings_and_execution_policy_are_exact(self):
        observation.validate_binding(self.preflight, self.request)
        for key in ("host", "attempt_id", "unit_claim", "firmware_claim", "misty_units",
                    "device_identity_record_sha256"):
            with self.subTest(key=key), self.assertRaisesRegex(RuntimeError, "preflight_binding_mismatch"):
                observation.validate_binding(self.preflight, self.request | {key: "other"})
        for policy in ("old", "cold_sign_supported_usb_v1", "cold_sign_supported_usb_shield_on_v1", None, True):
            with self.subTest(policy=policy), self.assertRaisesRegex(RuntimeError, "execution_policy_required"):
                observation.validate_binding(self.preflight, self.request | {"execution_policy": policy})

    def test_prior_identity_valid_record_and_hash_refusal(self):
        observation.validate_prior_identity(self.identity, self.preflight, self.request, "a" * 64)
        for digest in ("b" * 64, "bad", None):
            with self.subTest(digest=digest), self.assertRaisesRegex(RuntimeError, "prior_identity_hash_mismatch"):
                observation.validate_prior_identity(self.identity, self.preflight, self.request, digest)
        with self.assertRaisesRegex(RuntimeError, "prior_identity_hash_mismatch"):
            observation.validate_prior_identity(self.identity, self.preflight,
                                                self.request | {"device_identity_record_sha256": "b" * 64}, "a" * 64)

    def test_prior_identity_schema_and_chronology_refuse(self):
        for update in ({"extra": 1}, {"schema": "old"}, {"confirmed_by": "other"},
                       {"method": "serial_probe"}, {"namespace_unambiguous": 1}, {"approval_reference": ""}):
            with self.subTest(update=update), self.assertRaisesRegex(RuntimeError, "prior_identity_schema"):
                observation.validate_prior_identity(self.identity | update, self.preflight, self.request, "a" * 64)
        for value in (True, 0, 101, float("inf"), float("nan"), "90"):
            with self.subTest(value=value), self.assertRaisesRegex(RuntimeError, "prior_identity_chronology"):
                observation.validate_prior_identity(self.identity | {"observed_at": value},
                                                    self.preflight, self.request, "a" * 64)

    def test_prior_identity_unit_host_path_and_rdev_bind_to_cold_facts(self):
        for key, value in (("host", "other"), ("unit_claim", "other"),
                           ("device_path", "/dev/cu.other"), ("device_rdev", 8)):
            with self.subTest(key=key), self.assertRaisesRegex(RuntimeError, "prior_identity_binding_mismatch"):
                observation.validate_prior_identity(self.identity | {key: value},
                                                    self.preflight, self.request, "a" * 64)
        with self.assertRaisesRegex(RuntimeError, "prior_identity_binding_mismatch"):
            observation.validate_prior_identity(self.identity, self.preflight,
                                                self.request | {"host": "other"}, "a" * 64)

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
