"""Registry tests for TreeListFormatter."""

import pytest
from sqlens.formatters import get_formatter, list_formatters
from sqlens.formatters.treelist import TreeListFormatter


class TestTreeListRegistration:
    def test_treelist_in_list(self):
        names = list_formatters()
        assert "treelist" in names

    def test_get_formatter_returns_treelist(self):
        fmt = get_formatter("treelist")
        assert isinstance(fmt, TreeListFormatter)

    def test_get_formatter_case_insensitive(self):
        fmt = get_formatter("TreeList")
        assert isinstance(fmt, TreeListFormatter)

    def test_list_formatters_sorted(self):
        names = list_formatters()
        assert names == sorted(names)

    def test_get_formatter_unknown_raises(self):
        with pytest.raises(ValueError):
            get_formatter("treelist_nonexistent_xyz")
