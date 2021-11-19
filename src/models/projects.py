from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, Tuple
from databases import Database
from datetime import datetime

from pydantic.types import UUID4


@dataclass
class ProjectData:
    name: str


@dataclass
class Project(ProjectData):
    id: int
    created_at: datetime
    updated_at: datetime
    api_key: Optional[UUID4] = None
    user_id: Optional[int] = None


async def insert_project(db: Database, data: ProjectData) -> Project:
    result = await db.fetch_one(
        """INSERT INTO projects (name)
                    VALUES (:name)
            RETURNING id, api_key, created_at, updated_at, name""",
        values=asdict(data),
    )
    return Project(**result)


async def select_project_from_api_key(db: Database, api_key: str) -> Optional[Project]:
    result = await db.fetch_one(
        """SELECT *
            FROM projects
        WHERE api_key = :api_key""",
        values={"api_key": api_key},
    )
    return None if not result else Project(**result)


async def select_project(db: Database, id: int) -> Optional[Project]:
    result = await db.fetch_one(
        """SELECT *
            FROM projects
        WHERE id = :id""",
        values={"id": id},
    )
    return None if result is None else Project(**result)


async def select_projects(db: Database) -> List[Project]:
    query = """SELECT *
            FROM projects"""
    return [Project(**row) async for row in db.iterate(query)]


async def delete_project(db: Database, id: int) -> None:
    await db.execute(
        """DELETE FROM projects
        WHERE id = :id""",
        values={"id": id},
    )
