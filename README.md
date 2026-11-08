# click-glide

[![CI](https://github.com/MakeyST/click-glide/actions/workflows/ci.yml/badge.svg)](https://github.com/MakeyST/click-glide/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://github.com/MakeyST/click-glide)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

A small accessibility helper for Windows: it turns a left click into a steady,
straight vertical glide. Press the button, the pointer jumps to the centre of
the screen and travels down at one of ten speeds.

It exists for the moments when holding a pointer still is the hard part: moving
a slider one notch, selecting a column of text, drawing a straight line,
keeping the cursor on the same spot while a key is held.

click-glide never presses buttons and never clicks for you. It only moves the
pointer while you hold the left button, and only while the guide is armed.

## What exactly happens

1. `F8` arms or disarms the guide (the default; see `--always`).
2. While armed, pressing the left button moves the pointer to the centre of the
   primary screen.
3. Holding the button keeps `x` at the centre and moves `y` down at the
   selected speed. The pointer stops at the bottom edge.
4. Releasing the button stops the glide; the pointer stays where it is.
5. Every new press starts again from the centre.

The guide is off until you arm it on purpose, so normal work is never hijacked.

## Speeds

| Mode | Pixels per second | Feel |
| ---: | ---: | --- |
| 1 | 600 | quick |
| 2 | 300 | brisk |
| 3 | 200 | steady |
| 4 | 150 | measured |
| 5 | 120 | calm |
| 6 | 100 | slow |
| 7 | 85.7 | slower |
| 8 | 75 | slowest comfortable |
| 9 | 66.7 | very slow |
| 10 | 60 | crawl |

Mode 1 is the fastest and mode 10 the slowest; the speed is 600 / mode pixels
per second.

## Requirements

- Windows 10 or 11
- Python 3.10 or newer
- No third-party packages

## Install

From a checkout:

```bash
python -m pip install .
```

Or run it without installing anything:

```bash
python -m click_glide --mode 3
```

## Usage

```bash
$ python -m click_glide --mode 2
click-glide 0.1.0: mode 2, 300 px/s
guide: pressed F8 toggles it, Ctrl+C quits
screen: 1920x1080, centre (960, 540)
```

Press `F8`, hold the left button, watch the pointer travel down. Press `F8`
again to give normal clicking back.

| Option | Meaning |
| --- | --- |
| `--mode N` | glide speed, `1` (fastest) to `10` (slowest), default `5` |
| `--start-armed` | start with the guide already armed |
| `--always` | glide on every left click, no `F8` needed (intrusive) |
| `--list-modes` | print the speed table and exit |
| `--version` | print the version and exit |

`--always` is there because some people do want it; for most, arming on demand
is the difference between a helper and an obstacle.

## Tests

```bash
python -m pip install -e ".[dev]"
python -m pytest
```

The suite has three layers:

- `tests/test_speeds.py` — the mode table and validation;
- `tests/test_engine.py`, `tests/test_e2e.py` — the glide state machine and full
  simulated sessions (click, centre, glide, release) against a fake pointer and
  a fake clock, so they are deterministic and run anywhere;
- `tests/test_win32_live.py` — an opt-in check against the real pointer:
  `set CLICK_GLIDE_LIVE=1` before running pytest.

CI runs the first two layers on Windows for Python 3.10, 3.12 and 3.13.

## Limitations

- Windows only, primary monitor only.
- DPI awareness is best effort; on a scaled display the centre is still the
  centre, but coordinates are read in physical pixels.
- Secure desktops and a locked session reject pointer movement; the tool prints a
  one-time warning instead of pretending it worked.
- The pointer is moved with `SetCursorPos`, which is fine for a personal
  accessibility aid but is not a general purpose input-injection API.

## License

MIT
