import sys
from pathlib import Path

from monitor.ui import NetworkMonitorApp

if __name__ == "__main__":
    hosts_file = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    NetworkMonitorApp(hosts_file=hosts_file).run()
