import asyncio
import platform
import re

from .models import ArpState, HostEntry

_LINUX_ARP_RE = re.compile(
    r"^(\S+)\s+.*lladdr\s+([0-9a-fA-F:]+)\s+(\S+)", re.MULTILINE
)
_MACOS_ARP_RE = re.compile(
    r"^\S+\s+\(([^)]+)\)\s+at\s+([0-9a-fA-F:]+)\s+on\s+(.+)$", re.MULTILINE
)
_MACOS_INCOMPLETE_RE = re.compile(
    r"^\S+\s+\(([^)]+)\)\s+at\s+\(incomplete\)", re.MULTILINE
)


async def resolve_arp(entries: list[HostEntry]) -> None:
    system = platform.system()
    if system == "Linux":
        await _resolve_linux(entries)
    elif system == "Darwin":
        await _resolve_macos(entries)
    else:
        for entry in entries:
            entry.mac_address = "N/A"
            entry.arp_state = ArpState.NA


async def _resolve_linux(entries: list[HostEntry]) -> None:
    try:
        proc = await asyncio.create_subprocess_exec(
            "ip", "neigh",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL,
        )
        stdout, _ = await proc.communicate()
        output = stdout.decode(errors="replace")
    except OSError:
        for e in entries:
            e.mac_address = "N/A"
            e.arp_state = ArpState.NA
        return

    arp_table: dict[str, tuple[str, str]] = {}
    for match in _LINUX_ARP_RE.finditer(output):
        ip, mac, state = match.group(1), match.group(2), match.group(3)
        arp_table[ip] = (mac.upper(), state.upper())

    _apply_arp_table(entries, arp_table)


async def _resolve_macos(entries: list[HostEntry]) -> None:
    try:
        proc = await asyncio.create_subprocess_exec(
            "arp", "-a",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL,
        )
        stdout, _ = await proc.communicate()
        output = stdout.decode(errors="replace")
    except OSError:
        for e in entries:
            e.mac_address = "N/A"
            e.arp_state = ArpState.NA
        return

    arp_table: dict[str, tuple[str, str]] = {}
    for match in _MACOS_INCOMPLETE_RE.finditer(output):
        ip = match.group(1)
        arp_table[ip] = ("N/A", "INCOMPLETE")
    for match in _MACOS_ARP_RE.finditer(output):
        ip, mac, rest = match.group(1), match.group(2), match.group(3)
        if "permanent" in rest:
            state = "REACHABLE"
        elif "ifscope" in rest:
            state = "REACHABLE"
        else:
            state = "STALE"
        arp_table[ip] = (mac.upper(), state)

    _apply_arp_table(entries, arp_table)


def _apply_arp_table(
    entries: list[HostEntry], arp_table: dict[str, tuple[str, str]]
) -> None:
    for entry in entries:
        if entry.host in arp_table:
            mac, state = arp_table[entry.host]
            entry.mac_address = mac
            entry.arp_state = _parse_state(state)
        else:
            entry.mac_address = "N/A"
            entry.arp_state = ArpState.NA


def _parse_state(state: str) -> ArpState:
    mapping = {
        "REACHABLE": ArpState.REACHABLE,
        "STALE": ArpState.STALE,
        "FAILED": ArpState.FAILED,
        "INCOMPLETE": ArpState.INCOMPLETE,
        "DELAY": ArpState.STALE,
        "PROBE": ArpState.STALE,
        "PERMANENT": ArpState.REACHABLE,
        "EXPIRED": ArpState.STALE,
    }
    return mapping.get(state, ArpState.NA)
