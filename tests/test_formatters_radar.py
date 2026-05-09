"""Registry-level tests for RadarFormatter."""

from sqlens.formatters import get_formatter, list_formatters
from sqlens.formatters.radar import RadarFormatter


class TestRadarRegistration:
    def test_radar_in_list(self):
        assert "radar" in list_formatters()

    def test_get_formatter_returns_radar(self):
        fmt = get_formatter("radar")
        assert isinstance(fmt, RadarFormatter)

    def test_get_formatter_case_insensitive(self):
        fmt = get_formatter("Radar")
        assert isinstance(fmt, RadarFormatter)

    def test_list_formatters_sorted(self):
        names = list_formatters()
        assert names == sorted(names)

    def test_radar_formatter_has_name_attr(self):
        assert RadarFormatter.name == "radar"
