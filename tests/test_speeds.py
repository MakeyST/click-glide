from __future__ import annotations

import pytest

from click_glide.speeds import describe, speed_for


def test_mode_one_is_the_fastest_and_mode_ten_the_slowest() -> None:
    speeds = [speed_for(mode) for mode in range(1, 11)]
    assert speeds == sorted(speeds, reverse=True)
    assert len(set(speeds)) == 10


def test_known_speeds() -> None:
    assert speed_for(1) == 600.0
    assert speed_for(2) == 300.0
    assert speed_for(10) == 60.0


@pytest.mark.parametrize("mode", [0, 11, -1, 100])
def test_mode_out_of_range_is_rejected(mode: int) -> None:
    with pytest.raises(ValueError):
        speed_for(mode)


def test_describe_lists_every_mode() -> None:
    table = describe()
    assert [mode for mode, _ in table] == list(range(1, 11))
