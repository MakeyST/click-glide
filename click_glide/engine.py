"""The platform-independent glide state machine.

The engine owns no Win32 calls: it talks to a :class:`MousePort` and a clock,
which keeps the whole behaviour testable without touching a real pointer.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Protocol


class MousePort(Protocol):
    def position(self) -> tuple[int, int]: ...

    def move_to(self, x: int, y: int) -> None: ...

    def left_pressed(self) -> bool: ...


class Clock(Protocol):
    def __call__(self) -> float: ...


@dataclass
class GlideEngine:
    """Turns a held left button into a straight downward glide.

    While the guide is armed and the left button is held, the pointer is
    pinned to the horizontal centre of the screen and travels down at
    ``speed`` pixels per second. Releasing the button stops the glide.
    """

    width: int
    height: int
    speed: float
    mouse: MousePort
    clock: Clock
    armed: bool = False

    _gliding: bool = False
    _last_tick: Optional[float] = None

    @property
    def center(self) -> tuple[int, int]:
        return self.width // 2, self.height // 2

    def toggle(self) -> bool:
        """Flip the armed state and return the new value."""
        self.armed = not self.armed
        self._gliding = False
        self._last_tick = None
        return self.armed

    def tick(self) -> None:
        """Advance the engine by one loop iteration."""
        now = self.clock()
        if not (self.armed and self.mouse.left_pressed()):
            self._gliding = False
            self._last_tick = None
            return

        if not self._gliding:
            self._gliding = True
            self._last_tick = now
            self.mouse.move_to(*self.center)
            return

        assert self._last_tick is not None
        elapsed = max(now - self._last_tick, 0.0)
        self._last_tick = now

        x, y = self.mouse.position()
        center_x, _ = self.center
        next_y = min(y + self.speed * elapsed, self.height - 1)
        if (x, int(next_y)) != (center_x, y):
            self.mouse.move_to(center_x, int(next_y))
