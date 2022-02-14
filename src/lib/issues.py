import aiohttp
from src.models.projects import Project
from src.models.issues import Issue
from quart import url_for
from discord import Colour
from discord import Webhook, AsyncWebhookAdapter, Embed

async def send_wh(issue: Issue, project: Project):
    URL = "https://discord.com/api/webhooks/918019440161980416/w64-urend4C74dxTKeQ_hVqjhqBFw9uK0hYYUABB8-0Th0M3ey9ua4E6ENnKujbnXgml"
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(URL, adapter=AsyncWebhookAdapter(session))
        e = Embed(
            title=f"Error on {project.name}",
            url=url_for("projects.get_project_issue", issue_id=issue.id, project_id=project.id, _external=True),
            description=issue.error_name,
            colour=Colour.red(),
        )
        e.add_field(name="Project", value=project.name)
        e.add_field(name="Date", value=issue.created_at)
        e.add_field(name="Status", value=issue.current_status)
        e.add_field(name="File", value=issue.frames[len(issue.frames) - 1].file_name)
        e.add_field(
            name="Method", value=issue.frames[len(issue.frames) - 1].method_name
        )
        if issue.request != {}:
            e.add_field(name="Request Path", value=issue.request["path"])
            e.add_field(name="Request Method", value=issue.request["method"])
            e.add_field(name="User Agent", value=issue.request["headers"]["User-Agent"])
        await webhook.send(embed=e)