from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

from src.ops import Op
from src.sandbox import SimulationSandbox


class TemporalMode(str, Enum):
    RECALL = "RECALL"
    EXECUTION = "EXECUTION"
    SIMULATION = "SIMULATION"


class TemporalViolation(Exception):
    pass


@dataclass
class TemporalController:
    """
    Enforces explicit temporal modes and prevents temporal contamination.

    - RECALL: read-only. No world mutation, no tool calls, no memory writes.
    - SIMULATION: writes go to sandbox only. No real world mutation.
    - EXECUTION: real world mutation allowed, tool calls allowed, memory writes allowed.
    """
    mode: TemporalMode = TemporalMode.EXECUTION
    reason: str = "default"
    world_state: Dict[str, Any] = field(default_factory=dict)
    memory_log: List[str] = field(default_factory=list)
    event_log: List[str] = field(default_factory=list)
    sandbox: SimulationSandbox = field(default_factory=SimulationSandbox)

    def set_mode(self, mode: TemporalMode, reason: str = "") -> None:
        self.mode = mode
        self.reason = reason or "mode switch"
        self.event_log.append(f"MODE -> {mode.value} | reason={self.reason}")

    def log_event(self, text: str) -> None:
        self.event_log.append(text)

    def apply(self, op: Op, payload: Optional[Dict[str, Any]] = None) -> None:
        payload = payload or {}

        # Validate operation against mode
        self._validate(op)

        if op == Op.READ:
            # no-op: reads are allowed everywhere
            self.event_log.append("READ")
            return

        if op == Op.WORLD_MUTATION:
            updates = payload.get("set", {})
            if not isinstance(updates, dict):
                raise ValueError("WORLD_MUTATION expects payload['set'] to be a dict")
            for k, v in updates.items():
                self.world_state[k] = v
            self.event_log.append(f"WORLD_MUTATION set={list(updates.keys())}")
            return

        if op == Op.TOOL_CALL:
            tool = payload.get("tool", "tool")
            self.event_log.append(f"TOOL_CALL tool={tool}")
            return

        if op == Op.MEMORY_WRITE:
            text = payload.get("append", "")
            if not isinstance(text, str) or not text.strip():
                raise ValueError("MEMORY_WRITE expects payload['append'] to be a non-empty string")
            self.memory_log.append(text.strip())
            self.event_log.append("MEMORY_WRITE append=1")
            return

        if op == Op.SIM_WRITE:
            updates = payload.get("set", {})
            if not isinstance(updates, dict):
                raise ValueError("SIM_WRITE expects payload['set'] to be a dict")
            self.sandbox.write(updates)
            self.event_log.append(f"SIM_WRITE set={list(updates.keys())}")
            return

        raise ValueError(f"Unhandled op: {op}")

    def commit_simulation(self, keys: Optional[List[str]] = None) -> None:
        """
        Explicitly promote simulation outputs into real world state.
        Only allowed in EXECUTION or SIMULATION, but promotion is always explicit.

        keys=None means commit everything.
        """
        if self.mode == TemporalMode.RECALL:
            raise TemporalViolation("Cannot commit simulation while in RECALL mode (read-only).")

        snap = self.sandbox.snapshot()
        if keys is None:
            keys = list(snap.keys())

        committed = []
        for k in keys:
            if k in snap:
                self.world_state[k] = snap[k]
                committed.append(k)

        self.event_log.append(f"COMMIT_SIM keys={committed}")

    def clear_simulation(self) -> None:
        self.sandbox.clear()
        self.event_log.append("SIM_CLEAR")

    def _validate(self, op: Op) -> None:
        if self.mode == TemporalMode.RECALL:
            if op in (Op.WORLD_MUTATION, Op.TOOL_CALL, Op.MEMORY_WRITE, Op.SIM_WRITE):
                raise TemporalViolation(f"{op.value} not allowed in RECALL mode (read-only).")
            return

        if self.mode == TemporalMode.SIMULATION:
            if op in (Op.WORLD_MUTATION, Op.MEMORY_WRITE):
                raise TemporalViolation(f"{op.value} not allowed in SIMULATION mode (sandbox-only).")
            # TOOL_CALL allowed? In pure temporal isolation, keep it off unless you want it.
            if op == Op.TOOL_CALL:
                raise TemporalViolation("TOOL_CALL not allowed in SIMULATION mode (keep sim pure).")
            return

        if self.mode == TemporalMode.EXECUTION:
            # Everything except SIM_WRITE is allowed; SIM_WRITE is allowed too (but stays sandboxed).
            return
