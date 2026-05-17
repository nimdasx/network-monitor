import asyncio
from datetime import datetime

from rich.text import Text
from textual.app import App, ComposeResult
from textual.widgets import DataTable, Footer, Header

from .arp import resolve_arp
from .config import PING_INTERVAL, load_hosts
from .models import ArpState, HostEntry, PingStatus
from .ping import ping_host

COLUMNS = ("HOST/IP", "PING STATUS", "MAC ADDRESS", "ARP STATE", "LAST UPDATE")

PING_COLORS: dict[PingStatus, str] = {
    PingStatus.ONLINE: "green",
    PingStatus.OFFLINE: "red",
    PingStatus.TIMEOUT: "red",
    PingStatus.HIGH_LATENCY: "yellow",
}

ARP_COLORS: dict[ArpState, str] = {
    ArpState.REACHABLE: "green",
    ArpState.STALE: "yellow",
    ArpState.FAILED: "red",
    ArpState.INCOMPLETE: "red",
    ArpState.NA: "bright_black",
}


class NetworkMonitorApp(App):
    CSS = """
    DataTable {
        height: 1fr;
    }
    """
    TITLE = "Network Monitor"
    BINDINGS = [("q", "quit", "Quit")]

    def __init__(self) -> None:
        super().__init__()
        self.entries: list[HostEntry] = []

    def compose(self) -> ComposeResult:
        yield Header()
        yield DataTable()
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.cursor_type = "row"
        for col in COLUMNS:
            table.add_column(col, key=col)

        hosts = load_hosts()
        for host in hosts:
            entry = HostEntry(host=host)
            self.entries.append(entry)
            table.add_row(
                host, _ping_text(entry), "N/A", _arp_text(entry), "-",
                key=host,
            )

        self.run_worker(self._monitor_loop(), exclusive=True)

    async def _monitor_loop(self) -> None:
        while True:
            await asyncio.gather(*(ping_host(e) for e in self.entries))
            await resolve_arp(self.entries)
            self._refresh_table()
            await asyncio.sleep(PING_INTERVAL)

    def _refresh_table(self) -> None:
        table = self.query_one(DataTable)
        for entry in self.entries:
            last = entry.last_update.strftime("%H:%M:%S") if entry.last_update else "-"
            table.update_cell(entry.host, "HOST/IP", entry.host)
            table.update_cell(entry.host, "PING STATUS", _ping_text(entry))
            table.update_cell(entry.host, "MAC ADDRESS", entry.mac_address)
            table.update_cell(entry.host, "ARP STATE", _arp_text(entry))
            table.update_cell(entry.host, "LAST UPDATE", last)


def _ping_text(entry: HostEntry) -> Text:
    label = entry.ping_status.value
    if entry.ping_status == PingStatus.ONLINE and entry.latency_ms is not None:
        label += f" {entry.latency_ms:.0f}ms"
    elif entry.ping_status == PingStatus.HIGH_LATENCY and entry.latency_ms is not None:
        label += f" {entry.latency_ms:.0f}ms"
    color = PING_COLORS.get(entry.ping_status, "white")
    return Text(label, style=color)


def _arp_text(entry: HostEntry) -> Text:
    color = ARP_COLORS.get(entry.arp_state, "bright_black")
    return Text(entry.arp_state.value, style=color)
