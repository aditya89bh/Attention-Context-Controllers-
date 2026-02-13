from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class SimulationSandbox:
    """
    Holds hypothetical state during SIMULATION mode.
    This must never directly mutate real-world state.
    """
    sim_state: Dict[str, Any] = field(default_factory=dict)

    def write(self, updates: Dict[str, Any]) -> None:
        for k, v in updates.items():
            self.sim_state[k] = v

    def get(self, key: str, default: Any = None) -> Any:
        return self.sim_state.get(key, default)

    def snapshot(self) -> Dict[str, Any]:
        return dict(self.sim_state)

    def clear(self) -> None:
        self.sim_state.clear()
