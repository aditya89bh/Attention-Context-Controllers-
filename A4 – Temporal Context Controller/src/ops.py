from __future__ import annotations

from enum import Enum


class Op(str, Enum):
    # Reads
    READ = "READ"

    # Real-world side effects
    WORLD_MUTATION = "WORLD_MUTATION"
    TOOL_CALL = "TOOL_CALL"

    # Memory side effects (allowed only in EXECUTION)
    MEMORY_WRITE = "MEMORY_WRITE"

    # Simulation side effects (allowed only in SIMULATION)
    SIM_WRITE = "SIM_WRITE"
