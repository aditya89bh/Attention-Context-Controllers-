from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from src.events import Event, EventType
from src.frames import FrameType, ContextFrame, make_item


@dataclass
class ForegroundDecision:
    frame: FrameType
    reason: str


class ContextWindowManager:
    """
    Maintains multiple context frames and produces a bounded context window.
    """

    def __init__(self) -> None:
        self.frames: Dict[FrameType, ContextFrame] = {ft: ContextFrame(ft) for ft in FrameType}

        self._render_step = 0
        self._goal: Optional[str] = None
        self._constraints: List[str] = []

        # Signals (simple state)
        self._risk_hot: bool = False
        self._urgent_deadline: Optional[str] = None
        self._last_tool: Optional[str] = None
        self._last_sender: Optional[str] = None

    # -----------------------------
    # Public API
    # -----------------------------

    def set_goal(self, goal: str, constraints: Optional[List[str]] = None) -> None:
        self._goal = goal.strip()
        self._constraints = [c.strip() for c in (constraints or []) if c.strip()]
        self.update(Event(EventType.GOAL_SET, {"goal": self._goal, "constraints": self._constraints}))

    def update(self, event: Event) -> None:
        et = event.event_type
        p = event.payload

        if et == EventType.GOAL_SET:
            goal = p.get("goal", "")
            constraints = p.get("constraints", [])
            txt = f"Goal: {goal}"
            if constraints:
                txt += "\nConstraints:\n" + "\n".join([f"- {c}" for c in constraints])
            self._add(FrameType.TASK, txt, salience=0.95, tags=("goal",))

        elif et == EventType.MESSAGE:
            sender = p.get("from", "unknown")
            msg = p.get("text", "")
            self._last_sender = sender
            txt = f"Message from {sender}: {msg}"
            self._add(FrameType.SOCIAL, txt, salience=0.75, ttl_steps=8, tags=("message", sender))
            self._add(FrameType.TEMPORAL, f"Received message from {sender}.", salience=0.4, ttl_steps=6)

        elif et == EventType.OBSERVATION:
            obs = p.get("text", "")
            urgency = float(p.get("urgency", 0.3))
            txt = f"Observation: {obs}"
            self._add(FrameType.STATE, txt, salience=min(1.0, 0.55 + urgency * 0.4), ttl_steps=10, tags=("obs",))

            low = obs.lower()
            if "deadline" in low or "due" in low or "by " in low:
                self._urgent_deadline = obs
                self._add(FrameType.TEMPORAL, f"Deadline signal: {obs}", salience=0.8, ttl_steps=12, tags=("deadline",))

        elif et == EventType.STATE_UPDATE:
            state = p.get("text", "")
            txt = f"State update: {state}"
            self._add(FrameType.STATE, txt, salience=0.6, ttl_steps=12, tags=("state",))

        elif et == EventType.TOOL_RESULT:
            tool = p.get("tool", "tool")
            result = p.get("result", "")
            self._last_tool = tool
            txt = f"Tool result ({tool}): {result}"
            self._add(FrameType.TOOLS, txt, salience=0.7, ttl_steps=10, tags=("tool", tool))
            self._add(FrameType.TEMPORAL, f"Used tool: {tool}.", salience=0.45, ttl_steps=6, tags=("tool_use",))

        elif et == EventType.RISK_FLAG:
            reason = p.get("reason", "risk flagged")
            level = float(p.get("level", 0.8))
            if level >= 0.6:
                self._risk_hot = True
            txt = f"RISK: {reason} (level={level:.2f})"
            self._add(FrameType.RISK, txt, salience=min(1.0, 0.7 + level * 0.3), ttl_steps=20, tags=("risk",))

        elif et == EventType.NOTE:
            note = p.get("text", "")
            self._add(FrameType.TEMPORAL, f"Note: {note}", salience=0.35, ttl_steps=8, tags=("note",))

        else:
            self._add(FrameType.TEMPORAL, f"Unhandled event: {et}", salience=0.2, ttl_steps=3)

    def choose_foreground(self) -> ForegroundDecision:
        """
        Heuristic framing rules.
        Later, A10 can replace this with learned routing.
        """
        if self._risk_hot and len(self.frames[FrameType.RISK].items) > 0:
            return ForegroundDecision(FrameType.RISK, "Risk hot: safety/policy framing takes priority.")

        if self._urgent_deadline is not None:
            return ForegroundDecision(FrameType.TEMPORAL, "Deadline/urgency detected: temporal framing prioritized.")

        if self._last_tool is not None and len(self.frames[FrameType.TOOLS].items) > 0:
            return ForegroundDecision(FrameType.TOOLS, "Tool result present: focus on interpreting tool output.")

        if self._last_sender is not None and len(self.frames[FrameType.SOCIAL].items) > 0:
            return ForegroundDecision(FrameType.SOCIAL, "Recent message: social framing prioritized.")

        if self._goal:
            return ForegroundDecision(FrameType.TASK, "Default: maintain goal/constraints as primary frame.")

        return ForegroundDecision(FrameType.STATE, "No explicit goal: fall back to state framing.")

    def render_context(self, budget_chars: int = 2000) -> Dict[str, Any]:
        self._render_step += 1

        for fr in self.frames.values():
            fr.decay_ttls()
            fr.prune_expired()

        decision = self.choose_foreground()

        context_text = self._compose_context_window(decision.frame, budget_chars)

        snapshot: Dict[str, Any] = {
            "foreground_frame": decision.frame.value,
            "foreground_reason": decision.reason,
            "context_window": context_text,
            "debug": {
                "render_step": self._render_step,
                "frames_count": {ft.value: len(fr.items) for ft, fr in self.frames.items()},
                "signals": {
                    "risk_hot": self._risk_hot,
                    "urgent_deadline": self._urgent_deadline,
                    "last_tool": self._last_tool,
                    "last_sender": self._last_sender,
                },
            },
        }

        # Reset one-step signals
        self._last_tool = None
        self._urgent_deadline = None

        # Risk stays hot until risk frame empties (simple rule)
        if len(self.frames[FrameType.RISK].items) == 0:
            self._risk_hot = False

        return snapshot

    # -----------------------------
    # Internal helpers
    # -----------------------------

    def _add(
        self,
        frame: FrameType,
        text: str,
        salience: float = 0.5,
        ttl_steps: Optional[int] = None,
        tags: Tuple[str, ...] = (),
    ) -> None:
        self.frames[frame].add(make_item(text=text, salience=salience, ttl_steps=ttl_steps, tags=tags))

    def _compose_context_window(self, foreground: FrameType, budget_chars: int) -> str:
        blocks: List[str] = []
        used = 0

        def add_block(title: str, lines: List[str]) -> None:
            nonlocal used
            if not lines:
                return
            block = f"[{title}]\n" + "\n".join(lines) + "\n"
            if used + len(block) <= budget_chars:
                blocks.append(block)
                used += len(block)

        # Always include TASK if available
        task_items = self.frames[FrameType.TASK].topk(3)
        add_block("TASK", [f"- {it.short(400)}" for it in task_items])

        # Foreground frame
        fg_items = self.frames[foreground].topk(6)
        add_block(foreground.value, [f"- {it.short(500)}" for it in fg_items])

        # Supporting frames
        for sf in self._support_frames(foreground):
            if sf == foreground:
                continue
            items = self.frames[sf].topk(3)
            add_block(sf.value, [f"- {it.short(350)}" for it in items])
            if used >= budget_chars * 0.92:
                break

        if not blocks:
            return "[EMPTY]\nNo context available.\n"

        return "\n".join(blocks).strip()

    def _support_frames(self, foreground: FrameType) -> List[FrameType]:
        if foreground == FrameType.RISK:
            return [FrameType.TASK, FrameType.STATE, FrameType.TEMPORAL, FrameType.SOCIAL, FrameType.TOOLS]
        if foreground == FrameType.TEMPORAL:
            return [FrameType.TASK, FrameType.STATE, FrameType.SOCIAL, FrameType.TOOLS, FrameType.RISK]
        if foreground == FrameType.TOOLS:
            return [FrameType.TASK, FrameType.STATE, FrameType.TEMPORAL, FrameType.RISK, FrameType.SOCIAL]
        if foreground == FrameType.SOCIAL:
            return [FrameType.TASK, FrameType.STATE, FrameType.TEMPORAL, FrameType.RISK, FrameType.TOOLS]
        if foreground == FrameType.TASK:
            return [FrameType.STATE, FrameType.TEMPORAL, FrameType.SOCIAL, FrameType.TOOLS, FrameType.RISK]
        return [FrameType.TASK, FrameType.TEMPORAL, FrameType.SOCIAL, FrameType.TOOLS, FrameType.RISK]
