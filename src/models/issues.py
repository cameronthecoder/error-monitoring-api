from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, Optional, List
from src.models.projects import Project

class StatusEnum(Enum):
    UNRESOLVED = "unresolved"
    RESOLVED = "resolved"
    IGNORED = "ignored"


@dataclass
class Frame:
    line_number: int
    file_name: str
    code: str
    method_name: Optional[str] = None


@dataclass
class Issue:
    id: int
    project: Project
    frames: List[Frame]
    environment: Dict
    request: Dict
    error_name: str
    created_at: datetime
    updated_at: datetime
    status: StatusEnum = StatusEnum.UNRESOLVED