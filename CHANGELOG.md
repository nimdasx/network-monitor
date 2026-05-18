# Changelog

## 0.1.1 — 2026-05-18

### Added
- Custom hosts file via CLI argument: `uv run python app.py myfile.txt`
- Falls back to `hosts.txt` when no argument is provided

## 0.1.0 — 2026-05-18

### Added
- Realtime ping monitoring with latency display
- MAC address detection via ARP table (Linux + macOS)
- ARP state detection (REACHABLE, STALE, FAILED, INCOMPLETE)
- Color-coded status (green/red/yellow) for ping and ARP
- NAME column parsed from `#` comments in hosts.txt
- Textual-based TUI with auto-refresh every 1 second
- Support for 100+ hosts via async architecture
- Keyboard shortcut `q` to quit
