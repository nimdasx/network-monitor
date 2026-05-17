import asyncio
import platform
import re
from datetime import datetime

from .config import HIGH_LATENCY_THRESHOLD_MS, PING_TIMEOUT
from .models import HostEntry, PingStatus


async def ping_host(entry: HostEntry) -> None:
    try:
        if platform.system() == "Windows":
            cmd = ["ping", "-n", "1", "-w", str(int(PING_TIMEOUT * 1000)), entry.host]
        else:
            cmd = ["ping", "-c", "1", "-W", str(int(PING_TIMEOUT)), entry.host]

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL,
        )
        stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=PING_TIMEOUT + 1)
        output = stdout.decode(errors="replace")

        if proc.returncode == 0:
            latency = _parse_latency(output)
            entry.latency_ms = latency
            if latency is not None and latency > HIGH_LATENCY_THRESHOLD_MS:
                entry.ping_status = PingStatus.HIGH_LATENCY
            else:
                entry.ping_status = PingStatus.ONLINE
            entry.last_update = datetime.now()
        else:
            entry.ping_status = PingStatus.OFFLINE
            entry.latency_ms = None
    except asyncio.TimeoutError:
        entry.ping_status = PingStatus.TIMEOUT
        entry.latency_ms = None
    except OSError:
        entry.ping_status = PingStatus.OFFLINE
        entry.latency_ms = None


_LATENCY_RE = re.compile(r"time[=<]\s*([\d.]+)\s*ms")
_ROUNDTRIP_RE = re.compile(r"min/avg/max/\w+\s*=\s*[\d.]+/([\d.]+)/")


def _parse_latency(output: str) -> float | None:
    match = _LATENCY_RE.search(output)
    if match:
        return float(match.group(1))
    match = _ROUNDTRIP_RE.search(output)
    if match:
        return float(match.group(1))
    return None
