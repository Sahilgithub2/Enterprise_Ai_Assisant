from app.core.config import JIRA_PROJECT_KEY
from app.core.jira_client import JiraClient


client = JiraClient()


def create_issue(
    summary: str,
    description: str,
):
    payload = {
        "fields": {
            "project": {
                "key": JIRA_PROJECT_KEY,
            },
            "summary": summary,
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": description,
                            }
                        ],
                    }
                ],
            },
            "issuetype": {
                "name": "Task",
            },
        }
    }

    return client.post(
        "/rest/api/3/issue",
        payload,
    )


def get_issue(
    issue_key: str,
):
    return client.get(
        f"/rest/api/3/issue/{issue_key}"
    )


def search_issues(
    jql: str,
):
    return client.get(
        "/rest/api/3/search",
        {
            "jql": jql,
        },
    )


def assign_issue(
    issue_key: str,
    account_id: str,
):
    payload = {
        "accountId": account_id,
    }

    client.put(
        f"/rest/api/3/issue/{issue_key}/assignee",
        payload,
    )

    return {
        "message": "Issue assigned successfully."
    }


def get_transitions(
    issue_key: str,
):
    return client.get(
        f"/rest/api/3/issue/{issue_key}/transitions"
    )


def update_issue_status(
    issue_key: str,
    transition_id: str,
):
    payload = {
        "transition": {
            "id": transition_id,
        }
    }

    client.post(
        f"/rest/api/3/issue/{issue_key}/transitions",
        payload,
    )

    return {
        "message": "Issue status updated successfully."
    }

def search_users(
    query: str,
):
    users = client.get(
        "/rest/api/3/user/search",
        {
            "query": query,
        },
    )

    return users

def resolve_account_id(
    assignee: str,
):
    users = search_users(
        assignee,
    )

    if not users:
        raise ValueError(
            f"No Jira user found for '{assignee}'."
        )

    if len(users) > 1:

        print("\n========== MATCHING USERS ==========")

        for user in users:

            print(
                f"{user['displayName']} -> {user['accountId']}"
            )

    return users[0]["accountId"]