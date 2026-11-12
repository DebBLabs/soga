"""Bounded observation algorithm with injected I/O. No device access."""
import math


FRAME = bytes.fromhex("f3 fd 0a 00 28 01 01 00 04 00 4e 6f 6e 65 be f4")
BOOT_SECONDS = 12.0
QUIET_SECONDS = 1.0
WRITE_SECONDS = 0.5
RESPONSE_SECONDS = 2.0
WALL_SECONDS = 18.0
BOOT_LIMIT = 4096
RESPONSE_LIMIT = 1024


class ObservationAbort(Exception):
    pass


def observe(io, clock, classify):
    """io owns exactly one open/close and one write syscall per attempt.

    read(timeout, limit) returns bounded bytes and honors its deadline.
    write_once(frame, timeout) performs at most one write syscall.
    identity_ok() checks the pinned open handle and selected device identity.
    Signal handlers raise ObservationAbort. Raw capture survives all failures.
    """
    result = {
        "outcome": "not_started", "write_count": 0, "write_return": None,
        "boot_hex": "", "response_hex": "", "interpretation": None,
        "close": "not_opened", "error": None, "after_close_captured": False,
    }
    boot, response = bytearray(), bytearray()
    opened = False
    started = clock()
    last_byte = None
    try:
        opened = True
        io.open_once()
        opened_at = clock()
        result["opened_at"] = opened_at
        while clock() - opened_at < BOOT_SECONDS:
            if clock() - started >= WALL_SECONDS:
                raise ObservationAbort("wall_deadline")
            if not io.identity_ok():
                raise ObservationAbort("device_changed")
            remaining = BOOT_SECONDS - (clock() - opened_at)
            data = io.read(min(0.05, max(0.0, remaining)), BOOT_LIMIT - len(boot))
            if type(data) is not bytes or len(data) > BOOT_LIMIT - len(boot):
                raise ObservationAbort("invalid_boot_read")
            if data:
                boot.extend(data)
                last_byte = clock()
            if len(boot) >= BOOT_LIMIT:
                raise ObservationAbort("boot_limit_no_write")
        now = clock()
        if last_byte is not None and now - last_byte < QUIET_SECONDS:
            raise ObservationAbort("boot_not_quiet_no_write")
        if WALL_SECONDS - (now - started) < WRITE_SECONDS + RESPONSE_SECONDS:
            raise ObservationAbort("budget_no_write")
        if not io.identity_ok():
            raise ObservationAbort("device_changed")
        result["write_count"] = 1
        write_started = clock()
        written = io.write_once(FRAME, WRITE_SECONDS)
        result["write_return"] = written
        if type(written) is not int or written != len(FRAME):
            raise ObservationAbort("partial_or_ambiguous_write")
        if clock() - write_started > WRITE_SECONDS:
            raise ObservationAbort("write_deadline")
        response_started = clock()
        while clock() - response_started < RESPONSE_SECONDS:
            remaining_wall = WALL_SECONDS - (clock() - started)
            if remaining_wall <= 0:
                raise ObservationAbort("wall_deadline")
            if not io.identity_ok():
                raise ObservationAbort("device_changed")
            remaining = RESPONSE_SECONDS - (clock() - response_started)
            data = io.read(min(0.05, max(0.0, remaining), remaining_wall), RESPONSE_LIMIT - len(response))
            if type(data) is not bytes or len(data) > RESPONSE_LIMIT - len(response):
                raise ObservationAbort("invalid_response_read")
            response.extend(data)
            if len(response) >= RESPONSE_LIMIT:
                raise ObservationAbort("response_limit")
        result["outcome"] = "silence" if not response else "captured"
        if response:
            result["interpretation"] = classify(bytes(response))
    except BaseException as error:
        result["outcome"] = "aborted"
        result["error"] = type(error).__name__ + ":" + str(error)
    finally:
        result["boot_hex"], result["response_hex"] = boot.hex(), response.hex()
        if opened:
            try:
                close_result = io.close_once()
                result["close"] = "closed" if close_result is None else close_result
            except BaseException as error:
                result["close"] = "failed:" + type(error).__name__ + ":" + str(error)
                result["outcome"] = "aborted"
        result["elapsed"] = clock() - started
    return result


def classify_response(raw, protocol):
    """Preserve raw failures, including an otherwise valid wrong mode/index."""
    if not raw:
        return {"kind": "silence"}
    for python_fixture in (False, True):
        try:
            kind, value = protocol.parse_complete(raw, 1, python_fixture=python_fixture)
        except (ValueError, RuntimeError):
            continue
        if kind in ("json_null", "python_none", "device_error"):
            return {"kind": kind, "value": value, "scope": "one_candidate_only"}
        return {"kind": "unregistered_return", "value": value}
    return {"kind": "unparseable", "raw_hex": raw.hex()}


class SerialIO:
    def __init__(self, path, device_number, *, os_api, termios_api, selectors_api, stat_api, before_open=None):
        self.path = path
        self.device_number = device_number
        self.os, self.termios = os_api, termios_api
        self.selectors, self.stat = selectors_api, stat_api
        self.before_open = before_open
        self.fd = None
        self.attempted = False
        self.closed = False
        self.selector = None
        self.hupcl = None
        self.syscall_attempted = False

    def identity_ok(self):
        try:
            current = self.os.lstat(self.path)
            if not self.stat.S_ISCHR(current.st_mode) or current.st_rdev != self.device_number:
                return False
            if self.fd is None:
                return True
            opened = self.os.fstat(self.fd)
            return self.stat.S_ISCHR(opened.st_mode) and opened.st_rdev == self.device_number
        except OSError:
            return False

    def open_once(self):
        if self.attempted or not self.identity_ok():
            raise RuntimeError("open_preflight_failed")
        if self.before_open is not None:
            self.before_open()
        self.attempted = True
        fd = self.os.open(self.path, self.os.O_RDWR | self.os.O_NOCTTY | self.os.O_NONBLOCK | self.os.O_NOFOLLOW)
        self.fd = fd
        try:
            if not self.identity_ok():
                raise RuntimeError("open_identity_changed")
            config = self.termios.tcgetattr(fd)
            self.hupcl = bool(config[2] & self.termios.HUPCL)
            config[0] = config[1] = config[3] = 0
            config[2] &= ~(self.termios.CSIZE | self.termios.PARENB | self.termios.CSTOPB | getattr(self.termios, "CRTSCTS", 0))
            config[2] |= self.termios.CS8 | self.termios.CLOCAL | self.termios.CREAD
            config[4] = config[5] = self.termios.B115200
            config[6][self.termios.VMIN] = config[6][self.termios.VTIME] = 0
            self.termios.tcsetattr(fd, self.termios.TCSANOW, config)
            self.selector = self.selectors.DefaultSelector()
            self.selector.register(fd, self.selectors.EVENT_READ)
        except BaseException:
            raise

    def read(self, timeout, limit):
        if not self.selector.select(timeout):
            return b""
        try:
            data = self.os.read(self.fd, limit)
            if not data:
                raise EOFError("device_eof")
            return data
        except BlockingIOError:
            return b""

    def write_once(self, frame, timeout):
        # Readiness wait does not send bytes; exactly one self.os.write call follows.
        with self.selectors.DefaultSelector() as writable:
            writable.register(self.fd, self.selectors.EVENT_WRITE)
            if not writable.select(timeout):
                raise TimeoutError("write_not_ready")
            self.syscall_attempted = True
            return self.os.write(self.fd, frame)

    def close_once(self):
        if self.closed:
            raise RuntimeError("duplicate_close")
        self.closed = True
        errors = []
        outcome = "not_opened"
        try:
            if self.selector is not None:
                self.selector.close()
        except Exception as error:
            errors.append("selector:" + type(error).__name__)
        finally:
            if self.fd is not None:
                fd, self.fd = self.fd, None
                try:
                    self.os.close(fd)
                    outcome = "closed"
                except Exception as error:
                    errors.append("fd:" + type(error).__name__)
        if errors:
            raise RuntimeError(",".join(errors))
        return outcome


def validate_preflight(preflight, now, device=None):
    required = {"confirmed_by", "observed_at", "device_path", "device_rdev", "unit_claim",
                "firmware_claim", "standalone_observed_seconds", "no_motion_sound_animation",
                "wheels_raised", "power_controls_accessible", "motor_power_off",
                "usb_logic_power_confirmed", "no_competing_owner", "boot_baseline_record", "misty_units",
                "attempt_id", "host"}
    if type(preflight) is not dict or set(preflight) != required or preflight["confirmed_by"] != "Deb":
        raise RuntimeError("preflight_schema")
    for key in ("unit_claim", "firmware_claim", "boot_baseline_record", "device_path", "attempt_id", "host"):
        if type(preflight[key]) is not str or not preflight[key] or len(preflight[key]) > 1024:
            raise RuntimeError("preflight_claim_required")
    if type(preflight["misty_units"]) is not list or any(
        type(unit) is not dict or set(unit) != {"unit", "state", "excluded"} or
        type(unit["unit"]) is not str or not unit["unit"] or
        unit["state"] != "powered_off" or unit["excluded"] is not True
        for unit in preflight["misty_units"]
    ):
        raise RuntimeError("misty_inventory_required")
    for key in ("no_motion_sound_animation", "wheels_raised", "power_controls_accessible",
                "motor_power_off", "usb_logic_power_confirmed", "no_competing_owner"):
        if preflight[key] is not True:
            raise RuntimeError("preflight_hold:" + key)
    if type(preflight["standalone_observed_seconds"]) not in (int, float) or not 15 <= preflight["standalone_observed_seconds"] <= 300:
        raise RuntimeError("stored_boot_observation")
    if type(preflight["observed_at"]) not in (int, float) or not 0 <= now - preflight["observed_at"] <= 120:
        raise RuntimeError("stale_preflight")
    if type(preflight["device_rdev"]) is not int or preflight["device_rdev"] < 0:
        raise RuntimeError("device_identity_mismatch")
    path = preflight["device_path"]
    if not path.startswith("/dev/cu.") or "/" in path[len("/dev/"):]:
        raise RuntimeError("device_path_required")
    if device is None:
        return
    if not device["canonical"] or device["parent"] != "/dev" or not device["name"].startswith("cu."):
        raise RuntimeError("device_path_required")
    if not device["character"] or device["rdev"] != preflight["device_rdev"]:
        raise RuntimeError("device_identity_mismatch")


def validate_authority(authority, request_hash, preflight_hash, attempt_id, verify):
    required = {"stable_request_sha256", "preflight_sha256", "attempt_id", "approved_by",
                "approval_reference", "approved_at", "expires_at", "attempts",
                "accept_candidate_uncertainty", "accept_reset_uncertainty"}
    if (type(authority) is not dict or set(authority) != required
            or authority["stable_request_sha256"] != request_hash
            or authority["preflight_sha256"] != preflight_hash
            or authority["attempt_id"] != attempt_id or authority["approved_by"] != "Deb"
            or type(authority["approval_reference"]) is not str
            or not authority["approval_reference"] or len(authority["approval_reference"]) > 1024
            or type(authority["attempts"]) is not int or authority["attempts"] != 1
            or authority["accept_candidate_uncertainty"] is not True
            or authority["accept_reset_uncertainty"] is not True):
        raise RuntimeError("physical_authority_required")
    if verify() is not True:
        raise RuntimeError("approval_signature_required")


def validate_binding(preflight, request):
    for key in ("attempt_id", "host", "unit_claim", "firmware_claim", "misty_units"):
        if preflight[key] != request[key]:
            raise RuntimeError("preflight_binding_mismatch:" + key)


def checked_sample(sample):
    wall, monotonic = sample
    if not all(type(value) in (int, float) and -1e12 < value < 1e12 and math.isfinite(value)
               for value in sample) or wall <= 0 or monotonic < 0:
        raise RuntimeError("invalid_clock_sample")
    return wall, monotonic


def remaining(preflight, authority, sample, previous=None):
    wall, monotonic = checked_sample(sample)
    if previous is not None:
        earlier_wall, earlier_mono = checked_sample(previous)
        if (wall < earlier_wall or monotonic < earlier_mono
                or abs((wall - earlier_wall) - (monotonic - earlier_mono)) > 1):
            raise RuntimeError("clock_discontinuity")
    observed, approved, expiry = (
        preflight["observed_at"], authority["approved_at"], authority["expires_at"]
    )
    if not all(type(value) in (float, int) and 0 < value < 1e12
               for value in (observed, approved, expiry)):
        raise RuntimeError("invalid_gate_timestamp")
    if not observed <= approved <= wall < expiry <= observed + 120:
        raise RuntimeError("preflight_or_approval_expired")
    return expiry - wall


def open_cutoff(preflight, authority, initial, final):
    start_budget = remaining(preflight, authority, initial)
    final_budget = remaining(preflight, authority, final, initial)
    return min(initial[1] + start_budget, final[1] + final_budget)


def check_open(preflight, authority, parent_sample, cutoff, sample):
    remaining(preflight, authority, sample, parent_sample)
    if sample[1] >= cutoff:
        raise RuntimeError("monotonic_open_cutoff")


def check_inventory(paths, runtime):
    for path in paths:
        if path not in runtime:
            raise RuntimeError("unlisted_loaded_runtime:" + path)


def reserve_attempt(create, persist, sync_parent):
    create()
    persist()
    sync_parent()


def physical_limits():
    return {"preflight_seconds": 120, "clock_divergence_seconds": 1,
            "boot_seconds": BOOT_SECONDS, "quiet_seconds": QUIET_SECONDS,
            "boot_bytes": BOOT_LIMIT, "write_calls": 1, "frame_bytes": len(FRAME),
            "write_ready_seconds": WRITE_SECONDS, "response_seconds": RESPONSE_SECONDS,
            "response_bytes": RESPONSE_LIMIT, "worker_seconds": WALL_SECONDS,
            "capture_seconds": 20, "worker_output_bytes": 32768}


def worker_report(raw, decode):
    try:
        report = decode(raw)
    except (ValueError, RuntimeError):
        return None
    required = {"outcome", "write_count", "boot_hex", "response_hex", "close",
                "physical_outcome", "operator_postflight"}
    if type(report) is not dict or not required.issubset(report):
        return None
    return report


class AbortPolicy:
    """Parent signal/grace state; no OS operations."""
    def __init__(self):
        self.signum = None
        self.forwarded_at = None

    def receive(self, signum):
        if self.signum is None:
            self.signum = signum

    def action(self, now, hard_deadline):
        if now >= hard_deadline:
            return "kill"
        if self.signum is None:
            return "continue"
        if self.forwarded_at is None:
            self.forwarded_at = now
            return "forward"
        return "kill" if now - self.forwarded_at >= 1.0 else "wait"
