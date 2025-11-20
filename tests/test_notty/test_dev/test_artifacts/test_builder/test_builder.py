"""module."""

from pathlib import Path

from notty.dev.artifacts.builder.builder import NottyBuilder


class TestNottyBuilder:
    """Test class."""

    def test_get_add_datas(self) -> None:
        """Test method."""
        datas = NottyBuilder.get_add_datas()
        assert isinstance(datas, list), f"Expected list, got {type(datas)}"

        if not datas:
            return

        tuple_len = 2
        for data in datas:
            assert isinstance(data, tuple), f"Expected tuple, got {type(data)}"
            assert len(data) == tuple_len, (
                f"Expected {tuple_len} elements, got {len(data)}"
            )
            first, second = data
            assert isinstance(first, Path), f"Expected {Path}, got {first}"
            assert isinstance(second, Path), f"Expected {Path}, got {second}"
