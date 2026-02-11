from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict
import time


class EventType(str, Enum):
    GOAL_SET = "GOAL_SET"
    OBSERVATION = "OBSERVATION"
    MESSAGE = "MESSAGE"
    TOOL_RESULT = "TOOL_RESULT"
    RISK_FLAG = "RISK_FLAG"
    STATE_UPDATE = "STATE_UPDATE"
    NOTE = "NOTE"


@dataclass
class Event:
    event_type: EventType
    payload: Dict[str, Any]
    ts: float = field(default_factory=lambda: time.time())
