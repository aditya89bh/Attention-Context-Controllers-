from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class BudgetMode(str, Enum):
    FULL = "FULL"
    CONSERVATIVE = "CONSERVATIVE"
    CRITICAL = "CRITICAL"
    EXHAUSTED = "EXHAUSTED"


@dataclass
class AttentionBudget:
    """
    Tracks a finite attention budget for an episode.
    Units are abstract "cognitive cost units".
    """
    total_units: int
    remaining_units: Optional[int] = None

    def __post_init__(self) -> None:
        if self.total_units <= 0:
            raise ValueError("total_units must be > 0")
        if self.remaining_units is None:
            self.remaining_units = self.total_units
        if self.remaining_units < 0:
            self.remaining_units = 0
        if self.remaining_units > self.total_units:
            self.remaining_units = self.total_units

    @property
    def depletion_ratio(self) -> float:
        # 0.0 means fresh; 1.0 means fully depleted
        used = self.total_units - self.remaining_units
        return used / self.total_units

    @property
    def remaining_ratio(self) -> float:
        return self.remaining_units / self.total_units

    @property
    def mode(self) -> BudgetMode:
        if self.remaining_units <= 0:
            return BudgetMode.EXHAUSTED
        r = self.remaining_ratio
        if r >= 0.60:
            return BudgetMode.FULL
        if r >= 0.25:
            return BudgetMode.CONSERVATIVE
        return BudgetMode.CRITICAL

    def can_spend(self, cost: int) -> bool:
        if cost < 0:
            raise ValueError("cost must be >= 0")
        return self.remaining_units >= cost

    def spend(self, cost: int) -> None:
        if cost < 0:
            raise ValueError("cost must be >= 0")
        self.remaining_units -= cost
        if self.remaining_units < 0:
            self.remaining_units = 0
