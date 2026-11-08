from __future__ import annotations

import pytest

from click_glide.cli import main


def test_list_modes_prints_the_speed_table(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["--list-modes"]) == 0
    out = capsys.readouterr().out
    assert "pixels per second" in out
    assert "600.0" in out
    assert "60.0" in out


@pytest.mark.parametrize("argv", [["--mode", "0"], ["--mode", "11"], ["--mode", "fast"]])
def test_invalid_mode_is_a_usage_error(argv: list[str]) -> None:
    with pytest.raises(SystemExit) as exit_info:
        main(argv)
    assert exit_info.value.code == 2


def test_version_flag(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exit_info:
        main(["--version"])
    assert exit_info.value.code == 0
    assert "click-glide" in capsys.readouterr().out
