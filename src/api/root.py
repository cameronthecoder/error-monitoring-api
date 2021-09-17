from datetime import datetime
from quart import Blueprint
from dataclasses import dataclass, asdict
from quart_schema import validate_request
from quart_schema.extension import tag
from quart_schema.validation import validate_response
root = Blueprint("root", __name__)

#@dataclass
#class User:
#    id: int
#    username: str
#   email: str

@dataclass
class ProjectData:
    title: str
    description: str
    created_at: datetime
    #user: User

@dataclass
class Project(ProjectData):
    id: int


@root.post("/")
@validate_request(ProjectData)
@validate_response(Project)
@tag(['Projects'])
async def index(data: ProjectData) -> Project:
    """
    Root index
    """
    return Project(id=3, **asdict(data))
