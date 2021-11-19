from os import abort
from quart import Blueprint, request, current_app
from quart_schema.validation import validate_request, validate_response

from src.models.issues import Issue, IssueData, insert_issue
from src.models.projects import select_project_from_api_key


blueprint = Blueprint("issues", __name__, url_prefix="/api")


@blueprint.post("/issues/")
@validate_request(IssueData)
@validate_response(Issue, 200)
async def add_issue(data: IssueData):
    print((await request.data))
    api_key = request.headers.get('Api-Key', None)
    print(request.headers)
    if api_key:
        project = await select_project_from_api_key(current_app.db, api_key)
        if project:
            issue = await insert_issue(current_app.db, project.id, data)
            return issue
        else:
            return {'error': 'API Key not valid.'}
    else:
        return abort(400)

