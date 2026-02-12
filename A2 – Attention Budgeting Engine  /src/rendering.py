from __future__ import annotations

from src.budget import AttentionBudget
from src.controller import BudgetController


def print_header(title: str) -> None:
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def print_event(kind: str, msg: str) -> None:
    print(f"{kind:>6s} | {msg}")


def print_summary(budget: AttentionBudget, ctrl: BudgetController) -> None:
    print("\n" + "-" * 80)
    print("SUMMARY")
    print("-" * 80)
    print(f"Total units:     {budget.total_units}")
    print(f"Remaining units: {budget.remaining_units}")
    print(f"Depletion ratio: {budget.depletion_ratio:.2f}")
    print(f"Final mode:      {budget.mode.value}")
    print("-" * 80)
    print("Policy knobs at end:")
    print(f"- max_memory_k:     {ctrl.max_memory_k()}")
    print(f"- allow_tool_calls: {ctrl.allow_tool_calls()}")
    print(f"- max_reason_steps: {ctrl.max_reason_steps()}")
    print(f"- should_exit_early:{ctrl.should_exit_early()}")
    print("-" * 80)
    print(f"Events logged: {len(ctrl.history)}")
