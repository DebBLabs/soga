"""Pure package, address and runtime-manifest validation."""

from __future__ import annotations

import hashlib
import ipaddress
import json
import platform
from dataclasses import dataclass
from pathlib import Path


class PackageValidationError(ValueError):
    pass


@dataclass(frozen=True)
class BindConfiguration:
    address: str
    interface_addresses: tuple
    synthetic_loopback: bool


def validate_private_ipv4(value: str) -> str:
    try:
        address = ipaddress.ip_address(value)
    except ValueError as error:
        raise PackageValidationError("invalid literal IPv4 address") from error
    if (address.version != 4 or str(address) != value or not address.is_private or
            address.is_loopback or address.is_link_local or address.is_multicast or
            address.is_unspecified or address.is_reserved):
        raise PackageValidationError("approved private IPv4 address required")
    return value


def validate_bind_configuration(*, bind_addresses, interface_addresses,
                                synthetic_loopback=False) -> BindConfiguration:
    if not isinstance(synthetic_loopback, bool):
        raise PackageValidationError("synthetic-loopback flag must be boolean")
    if not isinstance(bind_addresses, (tuple, list)) or len(bind_addresses) != 1:
        raise PackageValidationError("exactly one bind address required")
    if not isinstance(interface_addresses, (tuple, list, frozenset, set)):
        raise PackageValidationError("observed interface addresses required")
    address = bind_addresses[0]
    if synthetic_loopback:
        if address != "127.0.0.1":
            raise PackageValidationError("synthetic execution requires literal loopback")
    else:
        validate_private_ipv4(address)
        if address not in interface_addresses:
            raise PackageValidationError("address is not assigned to the selected interface")
    if any(not isinstance(item, str) for item in interface_addresses):
        raise PackageValidationError("interface addresses must be strings")
    observed = tuple(sorted(interface_addresses))
    return BindConfiguration(address=address, interface_addresses=observed,
                             synthetic_loopback=synthetic_loopback)


def _regular_file(root: Path, relative: str) -> Path:
    if (not isinstance(relative, str) or not relative or
            relative != Path(relative).as_posix() or
            Path(relative).is_absolute() or
            any(part in ("", ".", "..") for part in Path(relative).parts)):
        raise PackageValidationError("relative path required")
    path = root / relative
    cursor = root
    for part in Path(relative).parts:
        cursor = cursor / part
        if cursor.is_symlink():
            raise PackageValidationError("symlinked bundle path prohibited")
    try:
        resolved = path.resolve(strict=True)
    except OSError as error:
        raise PackageValidationError("regular bundle file required") from error
    if (not resolved.is_file() or resolved == root or root not in resolved.parents or
            resolved != path):
        raise PackageValidationError("regular bundle file required")
    return resolved


def digest_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while True:
            block = stream.read(65536)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def validate_manifest(bundle_root: Path, manifest_path: Path) -> dict:
    root = bundle_root.resolve(strict=True)
    if bundle_root.is_symlink() or manifest_path.is_symlink():
        raise PackageValidationError("symlinked roots prohibited")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise PackageValidationError("invalid runtime manifest") from error
    required = {"schema", "system", "machine", "python", "files"}
    if not isinstance(manifest, dict) or set(manifest) != required or manifest["schema"] != 1:
        raise PackageValidationError("unexpected runtime manifest shape")
    observed = {
        "system": platform.system(), "machine": platform.machine(),
        "python": platform.python_version(),
    }
    if any(manifest[name] != observed[name] for name in observed):
        raise PackageValidationError("runtime identity mismatch")
    files = manifest["files"]
    if not isinstance(files, dict) or not files:
        raise PackageValidationError("complete file hashes required")
    for relative, expected in sorted(files.items()):
        path = _regular_file(root, relative)
        if not isinstance(expected, str) or len(expected) != 64 or digest_file(path) != expected:
            raise PackageValidationError("runtime file hash mismatch")
    return manifest

