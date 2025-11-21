"""test module."""

import pytest
from pyrig.dev.configs.pyproject import PyprojectConfigFile
from pyrig.src.os.os import run_subprocess


def test_main() -> None:
    """Test func for main."""
    project_name = PyprojectConfigFile.get_project_name()
    stdout = run_subprocess(["poetry", "run", project_name, "--help"]).stdout.decode(
        "utf-8"
    )
    assert project_name in stdout


@pytest.mark.skip(reason="Won't test UI")
def test_run() -> None:
    """Test function."""
    raise NotImplementedError


@pytest.mark.skip(reason="Won't test UI")
def test_create_window() -> None:
    """Test function."""
    raise NotImplementedError


@pytest.mark.skip(reason="Won't test UI")
def test_init_game() -> None:
    """Test function."""
    raise NotImplementedError


@pytest.mark.skip(reason="Won't test UI")
def test_get_players() -> None:
    """Test function."""
    raise NotImplementedError


@pytest.mark.skip(reason="Won't test UI")
def test_show_deck() -> None:
    """Test function."""
    raise NotImplementedError


@pytest.mark.skip(reason="Won't test UI")
def test_show_players() -> None:
    """Test function."""
    raise NotImplementedError


@pytest.mark.skip(reason="Won't test UI")
def test_show_player_with_hand() -> None:
    """Test function."""
    raise NotImplementedError


@pytest.mark.skip(reason="Won't test UI")
def test_run_event_loop() -> None:
    """Test function."""
    raise NotImplementedError


@pytest.mark.skip(reason="Won't test UI")
def test_load_background() -> None:
    """Test function."""
    raise NotImplementedError


@pytest.mark.skip(reason="Won't test UI")
def test_get_window_size() -> None:
    """Test function."""
    raise NotImplementedError


@pytest.mark.skip(reason="Won't test UI")
def test_simulate_first_shuffle_and_deal() -> None:
    """Test function."""
    raise NotImplementedError


@pytest.mark.skip(reason="Won't test UI")
def test_get_player_display_order() -> None:
    """Test function."""
    raise NotImplementedError


@pytest.mark.skip(reason="Won't test UI")
def test_show_actions() -> None:
    """Test function."""
    raise NotImplementedError
