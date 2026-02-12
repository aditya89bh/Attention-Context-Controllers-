from __future__ import annotations

from typing import List

from src.gate import ScoredMemory


def print_header(title: str) -> None:
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def print_selected(title: str, selected: List[ScoredMemory]) -> None:
    print("\n" + "-" * 80)
    print(title)
    print("-" * 80)
    if not selected:
        print("(no memories selected)")
        return
    for i, sm in enumerate(selected, 1):
        tags = ",".join(sm.item.tags) if sm.item.tags else "-"
        print(f"{i:02d}. score={sm.score:.3f} | risk={sm.item.risk:.2f} | age={sm.item.age_steps:>2d} | tags={tags}")
        print(f"    {sm.item.text}")
