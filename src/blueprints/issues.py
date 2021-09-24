from dataclasses import dataclass
from datetime import datetime
from quart import Blueprint
from quart_schema import validate_response
from enum import Enum
from typing import Dict, Optional, List
from src.models.projects import Project

blueprint = Blueprint("issues", __name__, url_prefix="/api")


class StatusEnum(Enum):
    UNRESOLVED = "unresolved"
    RESOLVED = "resolved"
    IGNORED = "ignored"


@dataclass
class Error:
    name: str
    cause: str
    handled: bool


@dataclass
class Frame:
    line_number: int
    file_name: str
    code_window: str
    method_name: Optional[str] = None


@dataclass
class Stacktrace:
    frames: List[Frame]


@dataclass
class Request:
    method: str
    path: str
    host: str
    protocol: str
    params: Dict


@dataclass
class Issue:
    id: int
    project: Project
    stack_trace: Stacktrace
    environment: Dict
    request: Request
    error: Error
    created_at: datetime
    updated_at: datetime
    status: StatusEnum = StatusEnum.UNRESOLVED


@validate_response(Issue)
@blueprint.route("/issues/")
async def testing():
    return "Hello WORLD"
