from pydantic import BaseModel


class JiraIntent(BaseModel):
    action: str
    summary: str = ""
    description: str = ""
    issue_key: str = ""
    assignee: str = ""
    account_id: str = ""
    status: str = ""
    query: str = ""