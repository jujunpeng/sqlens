import pytest
from sqlens.formatters import get_formatter, list_formatters
from sqlens.formatters.boxplot import BoxplotFormatter


class TestBoxplotRegistration:
    def test_boxplot_in_list(self):
        names = list_formatters()
        assert "boxplot" in names

    def test_get_formatter_returns_boxplot(self):
        fmt = get_formatter("boxplot")
        assert isinstance(fmt, BoxplotFormatter)

    def test_get_formatter_case_insensitive(self):
        fmt = get_formatter("Boxplot")
        assert isinstance(fmt, BoxplotFormatter)

        fmt2 = get_formatter("BOXPLOT")
        assert isinstance(fmt2, BoxplotFormatter)

    def test_list_formatters_sorted(self):
        names = list_formatters()
        assert names == sorted(names)

    def test_unknown_formatter_raises(self):
        with pytest.raises(ValueError, match="Unknown formatter"):
            get_formatter("notaformatter")
