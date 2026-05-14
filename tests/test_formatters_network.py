"""Registry integration tests for NetworkFormatter."""

from __future__ import annotations

from sqlens.formatters import get_formatter, list_formatters
from sqlens.formatters.network import NetworkFormatter


class TestNetworkRegistration:
    def test_network_in_list(self) -> None:
        names = list_formatters()
        assert "network" in names

    def test_get_formatter_returns_network(self) -> None:
        fmt = get_formatter("network")
        assert isinstance(fmt, NetworkFormatter)

    def test_get_formatter_case_insensitive(self) -> None:
        fmt = get_formatter("Network")
        assert isinstance(fmt, NetworkFormatter)

    def test_list_formatters_sorted(self) -> None:
        names = list_formatters()
        assert names == sorted(names)

    def test_network_format_callable(self) -> None:
        fmt = get_formatter("network")
        assert callable(getattr(fmt, "format", None))
