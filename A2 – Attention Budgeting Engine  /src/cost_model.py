from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict


class Operation(str, Enum):
    RENDER_CONTEXT = "RENDER_CONTEXT"
    REASON_STEP = "REASON_STEP"
    MEMORY_RETRIEVAL = "MEMORY_RETRIEVAL"
    TOOL_CALL = "TOOL_CALL"
    PLAN_STEP = "PLAN_STEP"
    WRITE_MEMORY = "WRITE_MEMORY"


@dataclass(frozen=True)
class CostModel:
    """
    Maps operations to costs in attention units.
    Keep this small and explicit: you can tune later.
    """
    costs: Dict[Operation, int]

    def cost_of(self, op: Operation) -> int:
        if op not in self.costs:
            raise KeyError(f"Missing cost for operation: {op}")
        c = self.costs[op]
        if c < 0:
            raise ValueError("Cost values must be >= 0")
        return c

    @staticmethod
    def default() -> "CostModel":
        return CostModel(
            costs={
                Operation.RENDER_CONTEXT: 3,
                Operation.REASON_STEP: 6,
                Operation.MEMORY_RETRIEVAL: 7,
                Operation.TOOL_CALL: 10,
                Operation.PLAN_STEP: 8,
                Operation.WRITE_MEMORY: 4,
            }
        )

    def with_override(self, op: Operation, new_cost: int) -> "CostModel":
        if new_cost < 0:
            raise ValueError("new_cost must be >= 0")
        new_costs = dict(self.costs)
        new_costs[op] = new_cost
        return CostModel(costs=new_costs)
