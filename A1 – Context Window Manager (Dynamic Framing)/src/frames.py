from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Tuple
import time


class FrameType(str, Enum):
    TASK = "TASK"
    STATE = "STATE"
    SOCIAL = "SOCIAL"
    TEMPORAL = "TEMPORAL"
    RISK = "RISK"
    TOOLS = "TOOLS"


@dataclass
class ContextItem:
    ts: float
    text: str
    salience: float = 0.5             # 0..1
    ttl_steps: Optional[int] = None   # expires after N render steps
    tags: Tuple[str, ...] = ()

    def short(self, width: int = 140) -> str:
        t = self.text.replace("\n", " ").strip()
        return (t[: width - 1] + "…") if len(t) > width else t


@dataclass
class ContextFrame:
    frame_type: FrameType
    items: List[ContextItem] = field(default_factory=list)
    max_items: int = 50

    def add(self, item: ContextItem) -> None:
        self.items.append(item)

        # Guardrail: if too many, drop lowest-salience items
        if len(self.items) > self.max_items:
            self.items.sort(key=lambda x: (x.salience, x.ts))
            drop_n = max(1, len(self.items) // 5)  # drop ~20%
            self.items = self.items[drop_n:]
            self.items.sort(key=lambda x: x.ts)

    def decay_ttls(self) -> None:
        for it in self.items:
            if it.ttl_steps is not None:
                it.ttl_steps -= 1

    def prune_expired(self) -> None:
        kept: List[ContextItem] = []
        for it in self.items:
            if it.ttl_steps is None:
                kept.append(it)
            elif it.ttl_steps > 0:
                kept.append(it)
        self.items = kept

    def topk(self, k: int) -> List[ContextItem]:
        ranked = sorted(self.items, key=lambda x: (x.salience, x.ts), reverse=True)
        return ranked[:k]


def make_item(
    text: str,
    salience: float = 0.5,
    ttl_steps: Optional[int] = None,
    tags: Tuple[str, ...] = (),
) -> ContextItem:
    return ContextItem(ts=time.time(), text=text.strip(), salience=salience, ttl_steps=ttl_steps, tags=tags)
