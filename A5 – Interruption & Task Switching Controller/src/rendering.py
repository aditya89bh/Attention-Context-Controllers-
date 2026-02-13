from __future__ import annotations

from src.controller import TaskSwitchController
from src.thread import ThreadStatus


def print_header(title: str) -> None:
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def print_state(label: str, ctrl: TaskSwitchController) -> None:
    print("\n" + "-" * 80)
    print(label)
    print("-" * 80)
    print(f"Active thread: {ctrl.active_id}")
    print(f"Paused stack:  {ctrl.stack}")

    # Show compact thread summary
    for tid, t in ctrl.threads.items():
        head = f"{tid} [{t.status.value}]"
        tail = t.notes[-1] if t.notes else "(no notes)"
        prefix = "->" if tid == ctrl.active_id else "  "
        print(f"{prefix} {head} | goal={t.goal}")
        print(f"     last: {tail}")


def print_log(ctrl: TaskSwitchController, last_n: int = 20) -> None:
    print("\n" + "-" * 80)
    print("Controller log (last events)")
    print("-" * 80)
    for line in ctrl.log[-last_n:]:
        print(f"- {line}")
