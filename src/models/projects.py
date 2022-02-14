from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, Tuple
from databases import Database
from datetime import date, datetime

from pydantic.types import UUID4


@dataclass
class ProjectData:
    name: str

@dataclass
class Stat:
    day: date
    ct: int

@dataclass
class Project(ProjectData):
    id: int
    created_at: datetime
    updated_at: datetime
    stats: List[Stat]
    api_key: Optional[UUID4] = None
    user_id: Optional[int] = None

async def get_stats(db: Database, id: int):
    query = """SELECT day, COALESCE(ct, 0) AS ct
FROM  (SELECT now()::date - d AS day FROM generate_series (0, 6) d) d  -- 6, not 7
LEFT   JOIN (
   SELECT created_at::date AS day, count(*) AS ct 
   FROM   issues
   WHERE  created_at >= date_trunc('day', now()) - interval '6d' AND project_id = 1
   GROUP  BY 1
   ) e USING (day);"""
    return [Stat(**row) async for row in db.iterate(query)]


async def insert_project(db: Database, data: ProjectData) -> Project:
    result = await db.fetch_one(
        """INSERT INTO projects (name)
                    VALUES (:name)
            RETURNING id, api_key, created_at, updated_at, name""",
        values=asdict(data),
    )
    stats = await get_stats(db, result['id'])
    return Project(**result, stats=stats)


async def select_project_from_api_key(db: Database, api_key: str) -> Optional[Project]:
    result = await db.fetch_one(
        """SELECT *
            FROM projects
        WHERE api_key = :api_key""",
        values={"api_key": api_key},
    )
    stats = await get_stats(db, result['id'])
    return None if not result else Project(**result, stats=stats)

async def select_project(db: Database, id: int) -> Optional[Project]:
    result = await db.fetch_one(
        """SELECT *
            FROM projects
        WHERE id = :id""",
        values={"id": id},
    )
    stats = await get_stats(db, id)
    return None if result is None else Project(**result, stats=stats)


async def select_projects(db: Database) -> List[Project]:
    query = """SELECT *
            FROM projects"""
    return [Project(**row, stats=[]) async for row in db.iterate(query)]


async def delete_project(db: Database, id: int) -> None:
    await db.execute(
        """DELETE FROM projects
        WHERE id = :id""",
        values={"id": id},
    )
