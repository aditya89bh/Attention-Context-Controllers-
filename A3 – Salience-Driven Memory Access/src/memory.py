from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class MemoryItem:
    """
    Minimal memory representation for A3.

    base_relevance:
        Pretend this came from vector similarity or metadata match (0..1).
    age_steps:
        Proxy for recency (smaller = newer). In real system, use timestamps.
    risk:
        How safety-sensitive this memory is (0..1).
    """
    text: str
    tags: Tuple[str, ...] = ()
    base_relevance: float = 0.5
    age_steps: int = 10
    risk: float = 0.0


class MemoryStore:
    def __init__(self) -> None:
        self._items: List[MemoryItem] = []

    def add(self, item: MemoryItem) -> None:
        self._items.append(item)

    def all(self) -> List[MemoryItem]:
        return list(self._items)
