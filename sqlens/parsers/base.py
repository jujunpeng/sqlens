"""Base classes for query plan parsing."""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class PlanNode:
    """Represents a single node in a query execution plan tree."""

    node_type: str
    cost: Optional[float] = None
    actual_time: Optional[float] = None
    rows: Optional[int] = None
    width: Optional[int] = None
    relation: Optional[str] = None
    index_name: Optional[str] = None
    join_type: Optional[str] = None
    extra: dict[str, Any] = field(default_factory=dict)
    children: list["PlanNode"] = field(default_factory=list)

    def is_leaf(self) -> bool:
        return len(self.children) == 0

    def total_nodes(self) -> int:
        return 1 + sum(child.total_nodes() for child in self.children)


class BasePlanParser(ABC):
    """Abstract base class for database-specific plan parsers."""

    @abstractmethod
    def parse(self, raw: Any) -> PlanNode:
        """Parse raw plan data into a PlanNode tree."""
        ...

    @property
    @abstractmethod
    def dialect(self) -> str:
        """Return the database dialect name."""
        ...
