"""Bounded observation algorithm with injected I/O. No device access."""
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
        except (ValueError, UnicodeError):
            continue
        if kind in ("json_null", "python_none", "device_error"):
            return {"kind": kind, "value": value, "scope": "one_candidate_only"}
        return {"kind": "unregistered_return", "value": value}
    return {"kind": "unparseable", "raw_hex": raw.hex()}


class SerialIO:
    def __init__(self, path, device_number, *, os_api, termios_api, selectors_api, stat_api):
        self.path = path
        self.device_number = device_number
        self.os, self.termios = os_api, termios_api
        self.selectors, self.stat = selectors_api, stat_api
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
            return self.fd is None or self.os.fstat(self.fd).st_rdev == self.device_number
        except OSError:
            return False

    def open_once(self):
        if self.attempted or not self.identity_ok():
            raise RuntimeError("open_preflight_failed")
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
        try:
            if self.selector is not None:
                self.selector.close()
        finally:
            if self.fd is not None:
                fd, self.fd = self.fd, None
                self.os.close(fd)
                return 'closed'
            return 'not_opened'



def validate_preflight(preflight, now, device):
    required = {"confirmed_by", "observed_at", "device_path", "device_rdev", "unit_claim",
                "firmware_claim", "standalone_observed_seconds", "no_motion_sound_animation",
                "wheels_raised", "power_controls_accessible", "motor_power_off",
                "usb_logic_power_confirmed", "no_competing_owner", "boot_baseline_record", "misty_units"}
    if type(preflight) is not dict or set(preflight) != required or preflight["confirmed_by"] != "Deb":
        raise RuntimeError("preflight_schema")
    for key in ("unit_claim", "firmware_claim", "boot_baseline_record", "device_path"):
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
    if not device["canonical"] or device["parent"] != "/dev" or not device["name"].startswith("cu."):
        raise RuntimeError("device_path_required")
    if type(preflight["device_rdev"]) is not int or not device["character"] or device["rdev"] != preflight["device_rdev"]:
        raise RuntimeError("device_identity_mismatch")


def validate_authority(authority, request_hash):
    if type(authority) is not dict or authority != {
        "request_sha256": request_hash, "approved_by": "Deb", "attempts": 1,
        "accept_candidate_uncertainty": True, "accept_reset_uncertainty": True,
    } or type(authority.get("attempts")) is not int or any(
        authority.get(key) is not True for key in ("accept_candidate_uncertainty", "accept_reset_uncertainty")
    ):
        raise RuntimeError("physical_authority_required")


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
