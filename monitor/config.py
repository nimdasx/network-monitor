from pathlib import Path

PING_INTERVAL = 1.0
PING_TIMEOUT = 2.0
HIGH_LATENCY_THRESHOLD_MS = 100.0
DEFAULT_HOSTS_FILE = Path("hosts.txt")


def load_hosts(path: Path = DEFAULT_HOSTS_FILE) -> list[str]:
    lines = path.read_text().splitlines()
    hosts = []
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        hosts.append(stripped)
    return hosts
