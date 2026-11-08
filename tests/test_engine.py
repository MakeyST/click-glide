from __future__ import annotations

from typing import Iterator

import pytest

from click_glide.engine import GlideEngine


class FakeMouse:
    def __init__(self, x: int = 0, y: int = 0, pressed: bool = False) -> None:
        self.x = x
        self.y = y
        self.pressed = pressed
        self.moves: list[tuple[int, int]] = []

    def position(self) -> tuple[int, int]:
        return self.x, self.y

    def move_to(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.moves.append((x, y))

    def left_pressed(self) -> bool:
        return self.pressed


class FakeClock:
    def __init__(self, now: float = 0.0) -> None:
        self.now = now

    def __call__(self) -> float:
        return self.now

    def advance(self, seconds: float) -> None:
        self.now += seconds


@pytest.fixture
def mouse() -> FakeMouse:
    return FakeMouse()


@pytest.fixture
def clock() -> FakeClock:
    return FakeClock()


@pytest.fixture
def engine(mouse: FakeMouse, clock: FakeClock) -> GlideEngine:
    return GlideEngine(width=1920, height=1080, speed=300.0, mouse=mouse, clock=clock, armed=True)


def test_unarmed_engine_ignores_the_button(engine: GlideEngine, mouse: FakeMouse) -> None:
    engine.armed = False
    mouse.pressed = True
    engine.tick()
    assert mouse.moves == []
    assert (mouse.x, mouse.y) == (0, 0)


def test_first_press_centers_the_pointer(engine: GlideEngine, mouse: FakeMouse) -> None:
    mouse.pressed = True
    engine.tick()
    assert (mouse.x, mouse.y) == (960, 540)
    assert len(mouse.moves) == 1


def test_glide_moves_down_at_the_configured_speed(engine: GlideEngine, mouse: FakeMouse, clock: FakeClock) -> None:
    mouse.pressed = True
    engine.tick()  # recenter
    clock.advance(0.1)
    engine.tick()
    assert mouse.x == 960
    assert mouse.y == 540 + 30


def test_glide_keeps_the_pointer_on_the_center_column(engine: GlideEngine, mouse: FakeMouse, clock: FakeClock) -> None:
    mouse.pressed = True
    engine.tick()
    mouse.x = 42  # the user yanks the mouse sideways
    clock.advance(0.05)
    engine.tick()
    assert mouse.x == 960


def test_glide_stops_at_the_bottom_edge(engine: GlideEngine, mouse: FakeMouse, clock: FakeClock) -> None:
    mouse.pressed = True
    engine.tick()
    clock.advance(10.0)
    engine.tick()
    assert mouse.y == 1079


def test_release_stops_the_glide(engine: GlideEngine, mouse: FakeMouse, clock: FakeClock) -> None:
    mouse.pressed = True
    engine.tick()
    clock.advance(0.1)
    engine.tick()
    moved_to = mouse.y

    mouse.pressed = False
    clock.advance(0.1)
    engine.tick()
    assert mouse.y == moved_to


def test_next_press_starts_again_from_the_center(engine: GlideEngine, mouse: FakeMouse, clock: FakeClock) -> None:
    mouse.pressed = True
    engine.tick()
    clock.advance(0.5)
    engine.tick()
    assert mouse.y > 540

    mouse.pressed = False
    engine.tick()

    mouse.pressed = True
    clock.advance(0.1)
    engine.tick()
    assert (mouse.x, mouse.y) == (960, 540)


def test_toggle_disarms_and_ignores_the_next_press(engine: GlideEngine, mouse: FakeMouse) -> None:
    assert engine.toggle() is False
    mouse.pressed = True
    engine.tick()
    assert mouse.moves == []


def test_clock_going_backwards_never_moves_the_pointer_up(engine: GlideEngine, mouse: FakeMouse, clock: FakeClock) -> None:
    mouse.pressed = True
    engine.tick()
    clock.now -= 1.0
    engine.tick()
    assert mouse.y == 540
