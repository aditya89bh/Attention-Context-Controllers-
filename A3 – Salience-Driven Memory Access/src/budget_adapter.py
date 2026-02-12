from __future__ import annotations

from enum import Enum


class BudgetMode(str, Enum):
    FULL = "FULL"
    CONSERVATIVE = "CONSERVATIVE"
    CRITICAL = "CRITICAL"
    EXHAUSTED = "EXHAUSTED"


def k_from_budget_mode(mode: BudgetMode) -> int:
    """
    Light integration point with A2.
    In real integration: pass A2's budget.mode into A3.
    """
    if mode == BudgetMode.FULL:
        return 8
    if mode == BudgetMode.CONSERVATIVE:
        return 4
    if mode == BudgetMode.CRITICAL:
        return 2
    return 0
