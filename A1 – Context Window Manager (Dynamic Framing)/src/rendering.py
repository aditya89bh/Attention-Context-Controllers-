from __future__ import annotations

from typing import Any, Dict


def pretty_print_snapshot(s: Dict[str, Any]) -> None:
    print("\n" + "=" * 80)
    print(f"FOREGROUND: {s['foreground_frame']}")
    print(f"REASON:     {s['foreground_reason']}")
    print("-" * 80)
    print(s["context_window"])
    print("-" * 80)
    print("DEBUG:", s["debug"])
