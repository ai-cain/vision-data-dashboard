from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar


T = TypeVar("T")


@dataclass(slots=True)
class PaginatedResult(Generic[T]):
    items: list[T]
    page: int
    per_page: int
    total: int
