from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

from src.memory import MemoryItem


def _clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def _tokenize(s: str) -> List[str]:
    return [t for t in "".join(ch.lower() if ch.isalnum() else " " for ch in s).split() if t]


def _jaccard(a: List[str], b: List[str]) -> float:
    sa, sb = set(a), set(b)
    if not sa and not sb:
        return 0.0
    return len(sa & sb) / max(1, len(sa | sb))


@dataclass(frozen=True)
class SalienceConfig:
    w_base: float = 0.45
    w_recency: float = 0.25
    w_task: float = 0.20
    w_risk: float = 0.10
    recency_half_life_steps: int = 12

    def replace(self, **kwargs) -> "SalienceConfig":
        data = {
            "w_base": self.w_base,
            "w_recency": self.w_recency,
            "w_task": self.w_task,
            "w_risk": self.w_risk,
            "recency_half_life_steps": self.recency_half_life_steps,
        }
        data.update(kwargs)
        return SalienceConfig(**data)


class SalienceScorer:
    """
    Produces a salience score (0..1) for a memory candidate.
    """

    def __init__(self, cfg: SalienceConfig) -> None:
        self.cfg = cfg

    def score(self, item: MemoryItem, task_query: str, foreground_frame: str) -> float:
        # 1) base relevance (e.g., embedding similarity)
        base = _clamp(item.base_relevance)

        # 2) recency decay -> newer = higher
        # A simple half-life curve using steps instead of timestamps
        hl = max(1, self.cfg.recency_half_life_steps)
        recency = 0.5 ** (item.age_steps / hl)
        recency = _clamp(recency)

        # 3) task alignment using a cheap token overlap
        tq = _tokenize(task_query)
        ti = _tokenize(item.text) + list(item.tags)
        task_align = _jaccard(tq, ti)
        task_align = _clamp(task_align)

        # 4) risk signal
        risk = _clamp(item.risk)

        # 5) mild frame conditioning (optional)
        # If foreground frame is TASK, boost items tagged "goal"/"task"
        frame_boost = 0.0
        if foreground_frame.upper() == "TASK" and any(t in ("goal", "task") for t in item.tags):
            frame_boost = 0.08
        if foreground_frame.upper() == "RISK" and any(t in ("risk", "privacy") for t in item.tags):
            frame_boost = 0.12

        s = (
            self.cfg.w_base * base
            + self.cfg.w_recency * recency
            + self.cfg.w_task * task_align
            + self.cfg.w_risk * risk
            + frame_boost
        )

        return _clamp(s)
