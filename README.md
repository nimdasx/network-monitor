# Network Monitor

Realtime network monitoring TUI built with Python and Textual.

## Requirements

- Python 3.12+
- [uv](https://github.com/astral-sh/uv)

## Setup

```bash
uv sync
```

## Usage

```bash
uv run python app.py
```

Press `q` to quit.

## Host Configuration

Edit `hosts.txt` — one host/IP per line, `#` for comments:

```txt
# Gateway
192.168.1.1

# DNS
8.8.8.8

# External
google.com
```
