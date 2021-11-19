from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, Optional, List, Tuple

from databases.core import Database
from src.models.projects import Project




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
    frames: List[FrameData]
    error_name: str

@dataclass
class Issue(IssueData):
    id: int
    created_at: datetime
    updated_at: datetime
    project_id: int
    current_status: str 

@dataclass
class ProjectIssue:
    id: int
    created_at: datetime
    updated_at: datetime
    project_id: int
    current_status: str 

async def select_frames(db: Database, issue_id: int) -> List[Frame]:
    query = """SELECT *
                FROM issues_frames
            WHERE issue_id = :id
    """
    return [Frame(**row) async for row in db.iterate(query, values={'id': issue_id})]

async def select_issues_from_project(db: Database, project_id: int) -> List[ProjectIssue]:
    query = """SELECT id,created_at,updated_at,project_id,current_status FROM issues 
            WHERE project_id = :project_id  
    """
    return [ProjectIssue(**row) async for row in db.iterate(query, values={'project_id': project_id})]

async def insert_frames(db: Database, data: List[FrameData], issue_id: int) -> List[Frame]:
    query = """INSERT INTO frames(code, file_name, line, line_number, method_name) 
                    VALUES (:code, :file_name, :line, :line_number, :method_name)
                RETURNING (:id, :code, :file_name, :line, :line_number, :method_name)
    """
    frames = [Frame(**row) async for row in db.iterate(query, asdict(data))]
    async for frame in frames:
        # Add each frame to the issue
        await db.execute(
            """
            INSERT INTO issues_frames (issue_id, frame_id) 
                VALUES (:issue_id, :frame_id)
            """,
            values={'issue_id': issue_id, 'frame_id': frame.id}
        )
    return frames

async def insert_issue(db: Database, project_id: int, data: IssueData) -> Issue:
    result = await db.fetch_one(
        """INSERT INTO issues(environment, request, project_id, error_name)
                        VALUES (:environment, ":request", :project_id, :error_name)
        RETURNING (id, current_status, project_id, error_name, environment, request, created_at, updated_at)""",
        values={'project_id': project_id, 'environment': data.environment, 'error_name': data.error_name, 'request': data.request},
    )
    issue = Issue(**result)
    frames = await insert_frames(db, data.frames, issue.id)
    return Issue(**result, frames=frames)

    


