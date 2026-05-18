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

Or specify a custom hosts file:

```bash
uv run python app.py servers.txt
```

Press `q` to quit.

## Host Configuration

One host/IP per line. Comments (`#`) above a host become its label in the NAME column:

```txt
# Gateway
192.168.1.1

# DNS
8.8.8.8

# External
google.com
```
