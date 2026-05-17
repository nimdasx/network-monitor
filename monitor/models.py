from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class PingStatus(Enum):
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"
    TIMEOUT = "TIMEOUT"
    HIGH_LATENCY = "HIGH LATENCY"


class ArpState(Enum):
    REACHABLE = "REACHABLE"
    STALE = "STALE"
    FAILED = "FAILED"
    INCOMPLETE = "INCOMPLETE"
    NA = "N/A"


@dataclass
class HostEntry:
    host: str
    ping_status: PingStatus = PingStatus.OFFLINE
    latency_ms: float | None = None
    mac_address: str = "N/A"
    arp_state: ArpState = ArpState.NA
    last_update: datetime | None = None
