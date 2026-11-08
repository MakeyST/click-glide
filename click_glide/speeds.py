"""Ten glide speeds, from quick (mode 1) to very slow (mode 10)."""

from __future__ import annotations

MODES = range(1, 11)
BASE_SPEED = 600.0  # pixels per second in mode 1


def speed_for(mode: int, base: float = BASE_SPEED) -> float:
    """Return the glide speed in pixels per second for *mode*.

    Mode 1 is the fastest and mode 10 the slowest; speed is inversely
    proportional to the mode number, so the ten steps are easy to reason about.
    """
    if mode not in MODES:
        raise ValueError(f"mode must be between 1 and 10, got {mode!r}")
    return base / mode


def describe(base: float = BASE_SPEED) -> list[tuple[int, float]]:
    """Return ``(mode, pixels per second)`` pairs for the UI and the docs."""
    return [(mode, speed_for(mode, base)) for mode in MODES]
