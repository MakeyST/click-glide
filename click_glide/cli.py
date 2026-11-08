"""Command line loop for click-glide."""

from __future__ import annotations

import argparse
import sys
import time
from typing import Sequence

from . import __version__
from .engine import GlideEngine
from .speeds import MODES, describe, speed_for

TICK_SECONDS = 0.008


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="click-glide",
        description="Glide the pointer straight down while the left button is held.",
    )
    parser.add_argument(
        "--mode",
        type=int,
        default=5,
        choices=list(MODES),
        help="glide speed, 1 is fastest and 10 is slowest (default: 5)",
    )
    parser.add_argument(
        "--always",
        action="store_true",
        help="glide on every left click, without arming the guide with F8 first",
    )
    parser.add_argument(
        "--start-armed",
        action="store_true",
        help="start with the guide already armed",
    )
    parser.add_argument("--list-modes", action="store_true", help="print the speed table and exit")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def _print_modes() -> None:
    print("mode  pixels per second")
    for mode, speed in describe():
        print(f"{mode:>4}  {speed:>17.1f}")


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)

    if args.list_modes:
        _print_modes()
        return 0

    if not sys.platform.startswith("win"):
        print("click-glide: this build supports Windows only", file=sys.stderr)
        return 2

    from .win32 import Win32Mouse, enable_dpi_awareness, screen_size

    enable_dpi_awareness()
    width, height = screen_size()
    mouse = Win32Mouse()
    engine = GlideEngine(
        width=width,
        height=height,
        speed=speed_for(args.mode),
        mouse=mouse,
        clock=time.perf_counter,
        armed=args.always or args.start_armed,
    )

    print(f"click-glide {__version__}: mode {args.mode}, {engine.speed:.0f} px/s")
    if args.always:
        print("guide: always on")
    else:
        print("guide: pressed F8 toggles it, Ctrl+C quits")
    print(f"screen: {width}x{height}, centre {engine.center}")

    was_down = False
    warned = False
    try:
        while True:
            if not args.always:
                down = Win32Mouse.toggle_pressed()
                if down and not was_down:
                    state = "on" if engine.toggle() else "off"
                    print(f"guide: {state}")
                was_down = down
            engine.tick()
            if mouse.failed and not warned:
                print(
                    "click-glide: Windows refused to move the pointer; is the session locked?",
                    file=sys.stderr,
                )
                warned = True
            time.sleep(TICK_SECONDS)
    except KeyboardInterrupt:
        print("\nclick-glide: stopped")
    return 0


def entry() -> None:  # pragma: no cover - console script wrapper
    raise SystemExit(main())
