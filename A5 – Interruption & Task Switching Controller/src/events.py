from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict
import time


class Priority(str, Enum):
    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class EventType(str, Enum):
    NEW_TASK = "NEW_TASK"
    MESSAGE = "MESSAGE"
    PROGRESS = "PROGRESS"
    INTERRUPT = "INTERRUPT"
    RISK_FLAG = "RISK_FLAG"
    DONE = "DONE"


@dataclass
class Event:
    event_type: EventType
    payload: Dict[str, Any]
    priority: Priority = Priority.NORMAL
    ts: float = field(default_factory=lambda: time.time())
