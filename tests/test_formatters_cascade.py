"""Registry tests for CascadeFormatter."""

from __future__ import annotations

import pytest

from sqlens.formatters import get_formatter, list_formatters
from sqlens.formatters.cascade import CascadeFormatter


class TestCascadeRegistration:
    def test_cascade_in_list(self) -> None:
        assert "cascade" in list_formatters()

    def test_get_formatter_returns_cascade(self) -> None:
        fmt = get_formatter("cascade")
        assert isinstance(fmt, CascadeFormatter)

    def test_get_formatter_case_insensitive(self) -> None:
        fmt = get_formatter("Cascade")
        assert isinstance(fmt, CascadeFormatter)

    def test_list_formatters_sorted(self) -> None:
        names = list_formatters()
        assert names == sorted(names)

    def test_unknown_formatter_raises(self) -> None:
        with pytest.raises(ValueError, match="Unknown formatter"):
            get_formatter("cascade_unknown_xyz")
