from dataclasses import asdict, dataclass, field
from datetime import datetime
from quart import current_app
from enum import Enum
from typing import Dict, Optional, List
from databases import Database
import json


class StatusEnum(Enum):
    resolved = "resolved"
    unresolved = "unresolved"
    ignored = "ignored"


@dataclass
class FrameData:
    line_number: int
    file_name: str
    code: str
    line: str
    method_name: str


@dataclass
class Frame(FrameData):
    id: int


@dataclass
class IssueData:
    environment: Dict
    request: Dict
    error_name: str
    frames: List[FrameData]

    def __post_init__(self):
        if type(self.environment) == str and type(self.request) == str:
            # convert strings to dictionaries after initialization
            self.environment = json.loads(self.environment)
            self.request = json.loads(self.request)

@dataclass
class Issue(IssueData):
    id: int
    created_at: datetime
    updated_at: datetime
    frames: List[Frame]
    error_name: Optional[str]
    project_id: int
    current_status: StatusEnum = StatusEnum.unresolved


@dataclass
class ProjectIssue:
    id: int
    created_at: datetime
    updated_at: datetime
    project_id: int
    error_name: Optional[str]
    current_status: StatusEnum = StatusEnum.unresolved



async def select_frames(db: Database, issue_id: int) -> List[Frame]:
    query = """SELECT frames.* 
                FROM issues_frames 
                INNER JOIN frames ON frames.id = frame_id 
            AND issue_id = :id
    """
    return [Frame(**row) async for row in db.iterate(query, values={"id": issue_id})]


async def select_issue_from_project(db: Database, project_id: int, issue_id: int) -> Optional[Issue]:
    query = """SELECT *
                FROM issues
            WHERE id = :issue_id AND project_id = :project_id
            """
    result = await db.fetch_one(query, values={"project_id": project_id, "issue_id": issue_id})
    if result:
        frames = await select_frames(db, issue_id)
    else:
        frames = []
    return None if result is None else Issue(**result, frames=frames)

async def group_issues(db: Database, project_id) -> List[Issue]:
    pass

async def select_issues_from_project(
    db: Database, project_id: int
) -> List[ProjectIssue]:
    query = """SELECT id,created_at,error_name,updated_at,project_id,current_status FROM issues 
            WHERE project_id = :project_id
    """
    return [
        ProjectIssue(**row)
        async for row in db.iterate(query, values={"project_id": project_id})
    ]


async def insert_frame_into_issue(db: Database, frames: List[Frame], issue_id: int):
    query = """INSERT INTO issues_frames(issue_id, frame_id)
                VALUES(:issue_id, :frame_id)
    """
    for frame in frames:
        await db.execute(query, {"issue_id": issue_id, "frame_id": frame.id})


async def insert_frames(db: Database, data: List[FrameData]) -> List[Frame]:
    query = """INSERT INTO frames(code, file_name, line, line_number, method_name) 
                    VALUES (:code, :file_name, :line, :line_number, :method_name)
                RETURNING id, code, file_name, line, line_number, method_name
    """
    frames = []
    # Insert frames into db from data
    for _frame in data:
        result = await db.fetch_one(query, values=asdict(_frame))
        frame = Frame(**result)
        frames.append(frame)

    return frames


async def insert_issue(db: Database, project_id: int, data: IssueData) -> Issue:
    values = {
        "project_id": project_id,
        "error_name": data.error_name,
        "request": json.dumps(data.request),
        "environment": json.dumps(data.environment),
    }
    result = await db.fetch_one(
        """INSERT INTO issues(project_id, request, environment, error_name)
                        VALUES (:project_id, :request, :environment, :error_name)
        RETURNING id, current_status, project_id, request, error_name, environment, created_at, updated_at""",
        values=values,
    )
    issue = Issue(**result, frames=[])
    frames = await insert_frames(db, data.frames)
    await insert_frame_into_issue(db, frames, issue.id)
    return Issue(**result, frames=frames)
