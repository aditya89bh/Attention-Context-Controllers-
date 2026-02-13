from __future__ import annotations

from src.temporal import TemporalController


def print_header(title: str) -> None:
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def print_state(label: str, ctrl: TemporalController) -> None:
    print("\n" + "-" * 80)
    print(label)
    print("-" * 80)
    print(f"Mode:   {ctrl.mode.value} | reason: {ctrl.reason}")
    print(f"World:  {ctrl.world_state}")
    print(f"Sim:    {ctrl.sandbox.snapshot()}")
    print(f"Memory: {len(ctrl.memory_log)} entries")


def print_log(ctrl: TemporalController, last_n: int = 12) -> None:
    print("\n" + "-" * 80)
    print("Event log (last events)")
    print("-" * 80)
    for e in ctrl.event_log[-last_n:]:
        print(f"- {e}")
