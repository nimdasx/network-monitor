from pathlib import Path

PING_INTERVAL = 1.0
PING_TIMEOUT = 2.0
HIGH_LATENCY_THRESHOLD_MS = 100.0
DEFAULT_HOSTS_FILE = Path("hosts.txt")


def load_hosts(path: Path = DEFAULT_HOSTS_FILE) -> list[tuple[str, str]]:
    lines = path.read_text().splitlines()
    hosts: list[tuple[str, str]] = []
    current_name = ""
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            current_name = stripped.lstrip("# ").strip()
            continue
        hosts.append((stripped, current_name))
        current_name = ""
    return hosts
