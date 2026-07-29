import json

from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import GEMINI_API_KEY

from app.prompts.jira_prompt import jira_prompt

from app.models.jira_models import JiraIntent

from app.services.jira_service import (
    create_issue,
    search_issues,
    get_issue,
    assign_issue,
    get_transitions,
    update_issue_status,
    resolve_account_id,
)


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0,
)


def parse_intent(
    question: str,
    previous_context: str = "",
) -> JiraIntent:

    prompt = jira_prompt.invoke(
        {
            "question": question,
            "context": previous_context,
        }
    )

    response = llm.invoke(prompt)

    content = (
        response.content.strip()
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    return JiraIntent.model_validate(
        json.loads(content)
    )


def format_search_results(result):

    issues = result.get("issues", [])

    if not issues:
        return "No Jira issues found."

    lines = []

    for issue in issues:

        fields = issue["fields"]

        assignee = "Unassigned"

        if fields.get("assignee"):
            assignee = fields["assignee"]["displayName"]

        lines.append(
            f"""
Issue Key : {issue['key']}
Summary   : {fields['summary']}
Status    : {fields['status']['name']}
Priority  : {fields['priority']['name']}
Assignee  : {assignee}
""".strip()
        )

    return "\n\n".join(lines)


def format_issue(result):

    fields = result["fields"]

    assignee = "Unassigned"

    if fields.get("assignee"):
        assignee = fields["assignee"]["displayName"]

    return f"""
Issue Key : {result['key']}
Summary   : {fields['summary']}
Description :
{fields.get('description')}

Status    : {fields['status']['name']}
Priority  : {fields['priority']['name']}
Assignee  : {assignee}
""".strip()


def get_jira_context(
    question: str,
    previous_context: str = "",
):

    print("\n========== JIRA AGENT ==========\n")
    print("\n========== PREVIOUS CONTEXT ==========\n")
    print(previous_context)
    intent = parse_intent(
        question,
        previous_context,
    )

    print(intent)

    action = intent.action.upper()

    if action == "CREATE_ISSUE":

        result = create_issue(
            intent.summary,
            intent.description,
        )

        context = (
            f"Issue created successfully.\n"
            f"Issue Key : {result['key']}"
        )

    elif action == "SEARCH_ISSUES":

        result = search_issues(
            intent.query,
        )

        context = format_search_results(result)

    elif action == "GET_ISSUE":

        result = get_issue(
            intent.issue_key,
        )

        context = format_issue(result)

    elif action == "ASSIGN_ISSUE":

        account_id = resolve_account_id(
            intent.assignee,
        )

        assign_issue(
            intent.issue_key,
            account_id,
        )

        context = (
            f"{intent.issue_key} assigned to "
            f"{intent.assignee} successfully."
        )

    elif action == "UPDATE_STATUS":

        transitions = get_transitions(
            intent.issue_key,
        )

        transition_id = None

        for transition in transitions["transitions"]:

            if transition["name"].lower() == intent.status.lower():

                transition_id = transition["id"]
                break

        if transition_id is None:

            available = ", ".join(
                t["name"]
                for t in transitions["transitions"]
            )

            raise ValueError(
                f"'{intent.status}' is not available.\n"
                f"Available transitions: {available}"
            )

        update_issue_status(
            intent.issue_key,
            transition_id,
        )

        context = (
            f"{intent.issue_key} moved to "
            f"{intent.status} successfully."
        )

    else:

        raise ValueError(
            f"Unsupported action: {intent.action}"
        )

    return {
        "context": context,
        "source": "Jira Cloud",
    }
