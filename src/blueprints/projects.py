from dataclasses import dataclass
from src.models.issues import (
    Issue,
    ProjectIssue,
    select_issues_from_project,
)
from src.lib.jwt_required import User, jwt_required
from quart.typing import ResponseReturnValue

from quart_schema import validate_request, hide_route
from src.lib.api_error import APIError
from typing import List, Tuple
from src.models.projects import (
    Project,
    ProjectData,
    delete_project,
    insert_project,
    select_project,
    select_projects,
)
from quart import Blueprint, current_app, g
from quart_schema import validate_response, tag

blueprint = Blueprint("projects", __name__, url_prefix="/api")


@dataclass
class Projects:
    projects: List[Project]


@dataclass
class Issues:
    issues: List[ProjectIssue]
    project: Project


@blueprint.get("/projects/")
@validate_response(Projects, 200)
@tag(["Projects"])
async def get_projects() -> Projects:
    """Get all Projects.
    Retrieve all projects from the database.
    """
    projects = await select_projects(current_app.db)
    return Projects(projects=projects)


@blueprint.get("/projects/<int:id>/")
@validate_response(Project, 200)
@tag(["Projects"])
async def get_project(id: int) -> Project:
    """Get a project.
    Retrieve a Project by its ID.
    """
    project = await select_project(current_app.db, id)
    if project is None:
        raise APIError(404, "The project was not found.")
    return project


@blueprint.post("/projects/")
@validate_response(Project, 201)
@validate_request(ProjectData)
@tag(["Projects"])
async def post_project(data: ProjectData) -> Tuple[Project, int]:
    """Create a new Project.
    This allows projects to be created and stored.
    """
    project = await insert_project(current_app.db, data)
    return project, 201


@blueprint.delete("/projects/<int:id>")
@tag(["Projects"])
async def project_delete(id: int) -> ResponseReturnValue:
    """Delete a project.

    This will delete the project.
    """
    await delete_project(current_app.db, id)
    return {"message": "Project successfully deleted."}, 202


@blueprint.route("/projects/<int:id>/issues/")
@validate_response(Issues)
@tag(["Projects"])
async def get_project_issues(id: int) -> Issues:
    """Get issues

    Get all issues associated with a project.
    """
    issues = await select_issues_from_project(current_app.db, id)
    project = await select_project(current_app.db, id)
    if project is None:
        raise APIError(404, "Project not found")
    return Issues(issues, project)


@blueprint.get("/projects/<string:key>/issues/gen/")
@hide_route
@tag(["Projects"])
async def gen_issue(key: str):
    """Generate sample error for project"""
    current_app.monitor.set_api_key(key)
    arr = [3, 3]
    arr[5]
    return "hello world"
