from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from src.budget import AttentionBudget, BudgetMode
from src.cost_model import CostModel, Operation


@dataclass
class SpendResult:
    op: Operation
    cost: int
    remaining: int
    mode: BudgetMode
    allowed: bool
    meta: Dict[str, Any]


class BudgetController:
    """
    Applies a CostModel to an AttentionBudget and exposes budget-aware policy knobs.
    Standalone by design; later A1/A3/A10 can query these policy knobs.
    """

    def __init__(self, budget: AttentionBudget, cost_model: CostModel) -> None:
        self.budget = budget
        self.cost_model = cost_model
        self.history: list[SpendResult] = []

    def spend(self, op: Operation, meta: Optional[Dict[str, Any]] = None) -> SpendResult:
        meta = dict(meta or {})
        cost = self.cost_model.cost_of(op)

        allowed = self.budget.can_spend(cost)
        if allowed:
            self.budget.spend(cost)

        result = SpendResult(
            op=op,
            cost=cost,
            remaining=self.budget.remaining_units,  # type: ignore[arg-type]
            mode=self.budget.mode,
            allowed=allowed,
            meta=meta,
        )
        self.history.append(result)
        return result

    # -----------------------------
    # Budget-aware policy controls
    # -----------------------------

    def max_memory_k(self) -> int:
        mode = self.budget.mode
        if mode == BudgetMode.FULL:
            return 8
        if mode == BudgetMode.CONSERVATIVE:
            return 4
        if mode == BudgetMode.CRITICAL:
            return 2
        return 0

    def allow_tool_calls(self) -> bool:
        mode = self.budget.mode
        if mode in (BudgetMode.FULL, BudgetMode.CONSERVATIVE):
            return True
        return False

    def max_reason_steps(self) -> int:
        mode = self.budget.mode
        if mode == BudgetMode.FULL:
            return 6
        if mode == BudgetMode.CONSERVATIVE:
            return 3
        if mode == BudgetMode.CRITICAL:
            return 1
        return 0

    def should_exit_early(self) -> bool:
        return self.budget.mode in (BudgetMode.CRITICAL, BudgetMode.EXHAUSTED)
