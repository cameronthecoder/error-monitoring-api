from quart import Blueprint, request, current_app, abort
from quart_schema import validate_request, validate_response, tag, hide_route
from src.lib.api_error import APIError
from src.models.issues import Issue, IssueData, insert_issue, select_issue
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
            return {"error": "API Key not valid."}
    else:
        return abort(400)


@blueprint.get("/issues/<int:id>/")
@validate_response(Issue, 200)
@tag(["Issues"])
async def get_issue(id: int):
    issue = await select_issue(current_app.db, id)
    if issue is None:
        raise APIError(404, "The issue was not found.")
    return issue
