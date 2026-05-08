import pytest
from sqlens.formatters import get_formatter, list_formatters
from sqlens.formatters.sunburst import SunburstFormatter


class TestSunburstRegistration:
    def test_sunburst_in_list(self):
        assert "sunburst" in list_formatters()

    def test_get_formatter_returns_sunburst(self):
        fmt = get_formatter("sunburst")
        assert isinstance(fmt, SunburstFormatter)

    def test_get_formatter_case_insensitive(self):
        fmt = get_formatter("Sunburst")
        assert isinstance(fmt, SunburstFormatter)

    def test_list_formatters_sorted(self):
        names = list_formatters()
        assert names == sorted(names)

    def test_unknown_formatter_raises(self):
        with pytest.raises(ValueError, match="Unknown formatter"):
            get_formatter("nonexistent_fmt")

    def test_error_message_lists_available(self):
        with pytest.raises(ValueError, match="sunburst"):
            get_formatter("nonexistent_fmt")
