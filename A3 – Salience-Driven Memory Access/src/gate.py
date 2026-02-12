from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

from src.budget_adapter import BudgetMode, k_from_budget_mode
from src.memory import MemoryItem
from src.salience import SalienceScorer


@dataclass
class ScoredMemory:
    item: MemoryItem
    score: float


class MemoryGate:
    """
    Selects which memories are allowed into reasoning.
    Light integration with A2: budget_mode controls top-k.
    """

    def __init__(self, scorer: SalienceScorer) -> None:
        self.scorer = scorer

    def select(
        self,
        candidates: List[MemoryItem],
        task_query: str,
        foreground_frame: str,
        budget_mode: BudgetMode,
    ) -> List[ScoredMemory]:
        k = k_from_budget_mode(budget_mode)

        scored: List[ScoredMemory] = []
        for c in candidates:
            s = self.scorer.score(c, task_query=task_query, foreground_frame=foreground_frame)
            scored.append(ScoredMemory(item=c, score=s))

        scored.sort(key=lambda x: x.score, reverse=True)
        return scored[:k]
