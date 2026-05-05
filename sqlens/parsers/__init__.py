"""Parser registry for sqlens."""

from sqlens.parsers.base import BasePlanParser
from sqlens.parsers.postgres import PostgresPlanParser
from sqlens.parsers.mysql import MySQLPlanParser

_REGISTRY: dict[str, BasePlanParser] = {
    "postgres": PostgresPlanParser(),
    "mysql": MySQLPlanParser(),
}


def get_parser(dialect: str) -> BasePlanParser:
    """Return a parser instance for the given *dialect* name.

    Raises
    ------
    ValueError
        If *dialect* is not recognised.
    """
    try:
        return _REGISTRY[dialect.lower()]
    except KeyError:
        supported = ", ".join(sorted(_REGISTRY))
        raise ValueError(
            f"Unknown dialect {dialect!r}. Supported dialects: {supported}."
        ) from None


__all__ = [
    "BasePlanParser",
    "PostgresPlanParser",
    "MySQLPlanParser",
    "get_parser",
]
