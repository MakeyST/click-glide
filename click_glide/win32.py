"""Minimal Win32 bindings: cursor position, primary screen size, buttons.

Only imported on Windows, so the rest of the package and the tests stay
platform independent.
"""

from __future__ import annotations

import ctypes
from ctypes import wintypes

user32 = ctypes.WinDLL("user32", use_last_error=True)


class POINT(ctypes.Structure):
    _fields_ = [("x", wintypes.LONG), ("y", wintypes.LONG)]


user32.GetCursorPos.argtypes = [ctypes.POINTER(POINT)]
user32.GetCursorPos.restype = wintypes.BOOL

user32.SetCursorPos.argtypes = [ctypes.c_int, ctypes.c_int]
user32.SetCursorPos.restype = wintypes.BOOL

user32.GetSystemMetrics.argtypes = [ctypes.c_int]
user32.GetSystemMetrics.restype = ctypes.c_int

user32.GetAsyncKeyState.argtypes = [ctypes.c_int]
user32.GetAsyncKeyState.restype = wintypes.SHORT

VK_LBUTTON = 0x01
VK_F8 = 0x77

SM_CXSCREEN = 0
SM_CYSCREEN = 1


def enable_dpi_awareness() -> None:
    """Best effort: make GetSystemMetrics/SetCursorPos use physical pixels."""
    try:
        user32.SetProcessDpiAwarenessContext(ctypes.c_void_p(-4))
    except (AttributeError, OSError):
        pass


def screen_size() -> tuple[int, int]:
    return user32.GetSystemMetrics(SM_CXSCREEN), user32.GetSystemMetrics(SM_CYSCREEN)


def _is_down(vk: int) -> bool:
    return bool(user32.GetAsyncKeyState(vk) & 0x8000)


class Win32Mouse:
    """Thin adapter used by :class:`click_glide.engine.GlideEngine`."""

    def __init__(self) -> None:
        self.failed = False

    def position(self) -> tuple[int, int]:
        point = POINT()
        user32.GetCursorPos(ctypes.byref(point))
        return point.x, point.y

    def move_to(self, x: int, y: int) -> None:
        if not user32.SetCursorPos(x, y):
            # A locked session or the secure desktop silently refuses moves.
            self.failed = True

    def left_pressed(self) -> bool:
        return _is_down(VK_LBUTTON)

    @staticmethod
    def toggle_pressed() -> bool:
        return _is_down(VK_F8)
