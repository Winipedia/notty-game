"""test module."""

from pyrig.dev.configs.pyproject import PyprojectConfigFile
from pyrig.src.os.os import run_subprocess


def test_main() -> None:
    """Test func for main."""
    project_name = PyprojectConfigFile.get_project_name()
    stdout = run_subprocess(["poetry", "run", project_name, "--help"]).stdout.decode(
        "utf-8"
    )
    assert project_name in stdout


def test_run() -> None:
    """Test function."""


def test_get_screen() -> None:
    """Test function."""


def test_simulate_first_shuffle_and_deal() -> None:
    """Test function."""


def test_run_event_loop() -> None:
    """Test function."""


def test_show_winner() -> None:
    """Test function."""


def test_start_background_music() -> None:
    """Test function."""
