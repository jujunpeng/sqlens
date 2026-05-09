import pytest
from sqlens.formatters import get_formatter, list_formatters
from sqlens.formatters.timeline_gantt import TimelineGanttFormatter
from sqlens.formatters.treemap import TreemapFormatter


class TestGanttRegistration:
    def test_gantt_in_list(self):
        names = list_formatters()
        assert "gantt" in names

    def test_get_formatter_returns_gantt(self):
        fmt = get_formatter("gantt")
        assert isinstance(fmt, TimelineGanttFormatter)

    def test_get_formatter_gantt_case_insensitive(self):
        fmt = get_formatter("GANTT")
        assert isinstance(fmt, TimelineGanttFormatter)


class TestTreemapRegistration:
    def test_treemap_in_list(self):
        names = list_formatters()
        assert "treemap" in names

    def test_get_formatter_returns_treemap(self):
        fmt = get_formatter("treemap")
        assert isinstance(fmt, TreemapFormatter)

    def test_get_formatter_treemap_case_insensitive(self):
        fmt = get_formatter("Treemap")
        assert isinstance(fmt, TreemapFormatter)

    def test_list_formatters_sorted(self):
        names = list_formatters()
        assert names == sorted(names)
