"""End-to-end simulations of a whole session against a fake pointer.

These tests drive the engine exactly like the CLI loop does, so they cover the
full click -> centre -> glide -> release cycle without moving a real cursor.
"""

from __future__ import annotations

from click_glide.engine import GlideEngine
from tests.test_engine import FakeClock, FakeMouse

TICK = 0.05
SPEED = 200.0


def make_engine() -> tuple[GlideEngine, FakeMouse, FakeClock]:
    mouse, clock = FakeMouse(x=120, y=800), FakeClock()
    engine = GlideEngine(
        width=1920,
        height=1080,
        speed=SPEED,
        mouse=mouse,
        clock=clock,
        armed=True,
    )
    return engine, mouse, clock


def run(engine: GlideEngine, mouse: FakeMouse, clock: FakeClock, ticks: int) -> None:
    for _ in range(ticks):
        engine.tick()
        clock.advance(TICK)


def test_session_glides_down_from_the_center() -> None:
    engine, mouse, clock = make_engine()
    mouse.pressed = True
    run(engine, mouse, clock, ticks=30)

    assert mouse.x == 960
    expected_y = 540 + SPEED * TICK * 29
    assert mouse.y == expected_y
    assert all(x == 960 for x, _ in mouse.moves)


def test_session_recenters_between_presses() -> None:
    engine, mouse, clock = make_engine()

    for _ in range(3):
        mouse.pressed = True
        engine.tick()
        assert (mouse.x, mouse.y) == (960, 540)

        clock.advance(TICK)
        engine.tick()
        assert mouse.y == 540 + SPEED * TICK

        mouse.pressed = False
        engine.tick()


def test_session_never_leaves_the_screen() -> None:
    engine, mouse, clock = make_engine()
    mouse.pressed = True
    run(engine, mouse, clock, ticks=200)

    ys = [y for _, y in mouse.moves] + [mouse.y]
    assert min(ys) >= 0
    assert max(ys) <= 1079
