from quart import Blueprint, request, current_app, abort
from quart_schema import validate_request, validate_response, tag
from src.lib.api_error import APIError
from src.models.issues import Issue, IssueData, insert_issue
from src.models.projects import select_project_from_api_key

blueprint = Blueprint("issues", __name__, url_prefix="/api")


@blueprint.post("/issues/")
@validate_request(IssueData)
@validate_response(Issue, 200)
@tag(["Issues"])
async def add_issue(data: IssueData):
    api_key = request.headers.get("Api-Key", None)
    if api_key:
        project = await select_project_from_api_key(current_app.db, api_key)
        if project:
            issue = await insert_issue(current_app.db, project.id, data)
            return issue
        else:
            raise APIError(404, "Project not found")
    else:
        return abort(400)

