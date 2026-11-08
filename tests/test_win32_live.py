"""Opt-in check against the real Win32 pointer.

Run it locally with CLICK_GLIDE_LIVE=1; it is skipped in CI and on other
platforms because moving the system cursor on a headless runner is pointless.
"""

from __future__ import annotations

import os
import sys

import pytest

pytestmark = pytest.mark.skipif(
    not sys.platform.startswith("win") or os.environ.get("CLICK_GLIDE_LIVE") != "1",
    reason="live pointer test needs Windows and CLICK_GLIDE_LIVE=1",
)


def test_real_pointer_can_be_moved_and_restored() -> None:
    from click_glide.win32 import Win32Mouse, enable_dpi_awareness

    enable_dpi_awareness()
    mouse = Win32Mouse()
    original = mouse.position()
    try:
        mouse.move_to(10, 11)
        if mouse.failed:
            pytest.skip("this desktop refuses pointer moves (locked session or secure desktop)")
        assert mouse.position() == (10, 11)
    finally:
        mouse.move_to(*original)
