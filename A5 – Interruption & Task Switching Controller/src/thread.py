from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid
import time


class ThreadStatus(str, Enum):
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    DONE = "DONE"


@dataclass
class ThreadSnapshot:
    """
    Minimal resume state.
    Keep this small: just enough to continue without drift.
    """
    goal: str
    last_step: str
    notes_tail: List[str]


@dataclass
class TaskThread:
    goal: str
    thread_id: str = field(default_factory=lambda: uuid.uuid4().hex[:10])
    status: ThreadStatus = ThreadStatus.ACTIVE
    created_at: float = field(default_factory=lambda: time.time())
    notes: List[str] = field(default_factory=list)

    def add_note(self, text: str) -> None:
        t = text.strip()
        if t:
            self.notes.append(t)

    def snapshot(self, tail_n: int = 4) -> ThreadSnapshot:
        last = self.notes[-1] if self.notes else "(no progress yet)"
        tail = self.notes[-tail_n:] if self.notes else []
        return ThreadSnapshot(goal=self.goal, last_step=last, notes_tail=tail)
