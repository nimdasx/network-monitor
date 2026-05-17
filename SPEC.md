# Realtime Network Monitoring TUI — Technical Specification

## Overview

A lightweight realtime terminal-based network monitoring application written in Python.

The application monitors:
- Ping availability and latency
- MAC address detection
- ARP/neighbor state

Hosts/IPs are loaded from a plain text file and displayed in a realtime updating table interface.

The application is intended for:
- Network monitoring
- Internal infrastructure visibility
- Lightweight NOC-style dashboards
- Router/device reachability checks

---

## Goals

- Lightweight and fast
- Realtime updates
- Easy deployment
- Cross-platform where possible
- Minimal dependencies
- Clean terminal UI (TUI)

---

## Technology Stack

| Component | Recommendation |
|---|---|
| Language | Python 3.12+ |
| Package Manager | uv |
| TUI Framework | Textual |
| Async Runtime | asyncio |
| Ping Engine | ping3 or subprocess ping |
| ARP Detection | `ip neigh` (Linux), `arp -a` (macOS) |
| Config Format | Plain text |
| Table rendering | rich |

---

## Functional Requirements

### 1. Host List Input

The application must load monitoring targets from a text file.

Requirements:
- One host/IP per line
- Empty lines ignored
- Comments supported using `#`

Example:
```txt
# Core Router
192.168.1.1
192.168.1.10
google.com
router.local
```

---

### 2. Realtime Ping Monitoring

The application must:
- Continuously ping all hosts
- Display availability status
- Display latency in milliseconds

Update interval: 1 second

---

### 3. Table Layout

| Column | Description |
|---|---|
| HOST/IP | Target hostname or IP |
| PING STATUS | Online/offline status with latency |
| MAC ADDRESS | Detected MAC address |
| ARP STATE | Neighbor/ARP state |
| LAST UPDATE | Timestamp of last successful update |

---

### 4. Status Coloring

#### Ping Status

| Status | Color |
|---|---|
| ONLINE | Green |
| OFFLINE | Red |
| TIMEOUT | Red |
| HIGH LATENCY | Yellow |

#### ARP State

| State | Color |
|---|---|
| REACHABLE | Green |
| STALE | Yellow |
| FAILED | Red |
| INCOMPLETE | Red |
| N/A | Gray |

---

### 5. MAC Address Detection

Requirements:
- Only supported for same Layer-2 network/subnet
- MAC address retrieved from ARP/neighbor table
- Unsupported hosts show `N/A`

Platform implementation:
- Linux: `ip neigh`
- macOS: `arp -a`

---

### 6. Realtime Refresh

The UI must update dynamically without clearing the entire terminal.

Requirements:
- Smooth redraw
- Minimal flicker
- Async updates

---

## Non-Functional Requirements

### Performance

- 100+ hosts simultaneously
- Low CPU usage
- Async/non-blocking architecture

### Portability

Primary target:
- Linux

Secondary support:
- macOS
- Windows (limited ARP support)

### Reliability

- Must survive temporary DNS failures
- Must survive packet loss
- Must continue running indefinitely

---

## Architecture

```text
Host Loader
    ↓
Async Ping Workers (asyncio task per host)
    ↓
ARP/MAC Resolver
    ↓
Shared State Store
    ↓
TUI Renderer (Textual)
```

---

## Project Structure

```text
network-monitor/
├── app.py
├── hosts.txt
├── pyproject.toml
├── uv.lock
└── monitor/
    ├── ping.py
    ├── arp.py
    ├── ui.py
    ├── models.py
    └── config.py
```

---

## Example UI

```text
┌─────────────────┬────────────────┬───────────────────┬────────────┬──────────────┐
│ HOST/IP         │ PING STATUS    │ MAC ADDRESS       │ ARP STATE  │ LAST UPDATE  │
├─────────────────┼────────────────┼───────────────────┼────────────┼──────────────┤
│ 192.168.1.1     │ ONLINE 2ms     │ AA:BB:CC:DD:EE    │ REACHABLE  │ 10:22:01     │
│ 192.168.1.10    │ OFFLINE        │ -                 │ FAILED     │ 10:21:55     │
│ google.com      │ ONLINE 22ms    │ N/A               │ N/A        │ 10:22:01     │
└─────────────────┴────────────────┴───────────────────┴────────────┴──────────────┘
```

---

## Development Phases

### Phase 1
- Host loading
- Ping monitoring
- Realtime table
- Color status

### Phase 2
- MAC detection
- ARP state detection

