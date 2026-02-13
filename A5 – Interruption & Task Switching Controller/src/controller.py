from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from src.events import Event, EventType, Priority
from src.thread import TaskThread, ThreadStatus, ThreadSnapshot


@dataclass
class SwitchLog:
    msg: str


class TaskSwitchController:
    """
    Manages interruption-safe task switching.

    Core behaviors:
    - Maintain a foreground active thread
    - Pause/resume threads explicitly
    - Critical interrupts override everything
    - Keep minimal resume snapshots to prevent drift
    """

    def __init__(self) -> None:
        self.threads: Dict[str, TaskThread] = {}
        self.active_id: Optional[str] = None
        self.stack: List[str] = []  # paused thread stack for resume
        self.resume_snapshots: Dict[str, ThreadSnapshot] = {}
        self.log: List[str] = []

    # -----------------------------
    # Public API
    # -----------------------------

    def handle(self, event: Event) -> None:
        et = event.event_type

        if et == EventType.NEW_TASK:
            goal = str(event.payload.get("goal", "")).strip()
            if not goal:
                raise ValueError("NEW_TASK requires payload['goal']")
            self._start_thread(goal, note="Started new task thread.")
            self._log(f"NEW_TASK -> active={self.active_id}")
            return

        if et == EventType.INTERRUPT:
            goal = str(event.payload.get("goal", "")).strip()
            if not goal:
                raise ValueError("INTERRUPT requires payload['goal']")
            self._interrupt(goal, priority=event.priority)
            self._log(f"INTERRUPT({event.priority.value}) -> active={self.active_id}")
            return

        if et == EventType.RISK_FLAG:
            reason = str(event.payload.get("reason", "")).strip() or "risk flagged"
            # Always treat as CRITICAL thread
            self._interrupt(f"Handle risk: {reason}", priority=Priority.CRITICAL)
            self._note_active(f"RISK_FLAG: {reason}")
            self._log(f"RISK_FLAG -> active={self.active_id}")
            return

        if et == EventType.MESSAGE:
            # Simple policy:
            # - LOW/NORMAL messages attach to current active thread
            # - HIGH/CRITICAL messages create interrupt thread
            text = str(event.payload.get("text", "")).strip()
            sender = str(event.payload.get("from", "user")).strip()
            if event.priority in (Priority.HIGH, Priority.CRITICAL):
                self._interrupt(f"Respond to urgent message from {sender}", priority=event.priority)
                self._note_active(f"Message from {sender}: {text}")
                self._log(f"MESSAGE({event.priority.value}) -> interrupt active={self.active_id}")
            else:
                self._note_active(f"Message from {sender}: {text}")
                self._log(f"MESSAGE({event.priority.value}) -> appended to active={self.active_id}")
            return

        if et == EventType.PROGRESS:
            note = str(event.payload.get("note", "")).strip()
            self._note_active(note)
            self._log(f"PROGRESS -> active={self.active_id}")
            return

        if et == EventType.DONE:
            summary = str(event.payload.get("summary", "")).strip() or "done"
            self._done_active(summary)
            self._log(f"DONE -> active={self.active_id}")
            return

        raise ValueError(f"Unhandled event_type: {et}")

    def resume_previous(self) -> None:
        """
        Resume the most recently paused thread (LIFO).
        """
        if not self.stack:
            self._log("RESUME: stack empty (nothing to resume)")
            return

        prev = self.stack.pop()
        self._set_active(prev)
        self.threads[prev].status = ThreadStatus.ACTIVE
        snap = self.resume_snapshots.get(prev)
        if snap:
            self._note_active(f"RESUME SNAPSHOT: last_step={snap.last_step}")
        self._log(f"RESUME -> active={self.active_id}")

    # -----------------------------
    # Internal helpers
    # -----------------------------

    def _start_thread(self, goal: str, note: str = "") -> str:
        t = TaskThread(goal=goal)
        if note:
            t.add_note(note)
        self.threads[t.thread_id] = t
        self._set_active(t.thread_id)
        return t.thread_id

    def _interrupt(self, goal: str, priority: Priority) -> None:
        # Pause current thread if exists
        if self.active_id is not None:
            self._pause_active(reason=f"Interrupted by {priority.value}")

        # Start new interrupt thread
        tid = self._start_thread(goal, note=f"Interrupt thread created ({priority.value}).")
        # Critical threads should go to top, but we already pause+start so it's active now
        return

    def _pause_active(self, reason: str = "paused") -> None:
        if self.active_id is None:
            return
        tid = self.active_id
        t = self.threads[tid]
        t.status = ThreadStatus.PAUSED
        t.add_note(f"PAUSE: {reason}")

        # Create minimal snapshot for resumption
        self.resume_snapshots[tid] = t.snapshot(tail_n=4)

        # Push to stack for later resume
        self.stack.append(tid)

    def _done_active(self, summary: str) -> None:
        if self.active_id is None:
            return
        t = self.threads[self.active_id]
        t.add_note(f"DONE: {summary}")
        t.status = ThreadStatus.DONE

        # After completing active thread, keep it active_id as None.
        self.active_id = None

    def _note_active(self, text: str) -> None:
        if self.active_id is None:
            # If nothing active, start a default thread
            self._start_thread("Default thread", note="Auto-created because an event arrived with no active thread.")
        self.threads[self.active_id].add_note(text)

    def _set_active(self, thread_id: str) -> None:
        self.active_id = thread_id

    def _log(self, msg: str) -> None:
        self.log.append(msg)
