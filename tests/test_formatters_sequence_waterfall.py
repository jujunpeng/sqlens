"""Registry integration tests for SequenceFormatter and WaterfallFormatter."""

from __future__ import annotations

from sqlens.formatters import get_formatter, list_formatters
from sqlens.formatters.sequence import SequenceFormatter
from sqlens.formatters.waterfall import WaterfallFormatter


class TestSequenceRegistration:
    def test_sequence_in_list(self) -> None:
        assert "sequence" in list_formatters()

    def test_get_formatter_returns_sequence(self) -> None:
        assert isinstance(get_formatter("sequence"), SequenceFormatter)

    def test_get_formatter_sequence_case_insensitive(self) -> None:
        assert isinstance(get_formatter("SEQUENCE"), SequenceFormatter)


class TestWaterfallRegistration:
    def test_waterfall_in_list(self) -> None:
        assert "waterfall" in list_formatters()

    def test_get_formatter_returns_waterfall(self) -> None:
        assert isinstance(get_formatter("waterfall"), WaterfallFormatter)

    def test_get_formatter_waterfall_case_insensitive(self) -> None:
        assert isinstance(get_formatter("WATERFALL"), WaterfallFormatter)


class TestListFormattersOrdering:
    def test_list_formatters_sorted(self) -> None:
        names = list_formatters()
        assert names == sorted(names)

    def test_both_formatters_present(self) -> None:
        names = list_formatters()
        assert "sequence" in names
        assert "waterfall" in names
