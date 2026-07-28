import requests

from requests.auth import HTTPBasicAuth

from app.core.config import (
    JIRA_BASE_URL,
    JIRA_EMAIL,
    JIRA_API_TOKEN,
)


class JiraClient:

    def __init__(self):
        self.base_url = JIRA_BASE_URL.rstrip("/")

        self.auth = HTTPBasicAuth(
            JIRA_EMAIL,
            JIRA_API_TOKEN,
        )

        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def get(
        self,
        endpoint,
        params=None,
    ):
        response = requests.get(
            f"{self.base_url}{endpoint}",
            headers=self.headers,
            auth=self.auth,
            params=params,
        )

        response.raise_for_status()

        return response.json()

    def post(
        self,
        endpoint,
        payload,
    ):
        response = requests.post(
            f"{self.base_url}{endpoint}",
            headers=self.headers,
            auth=self.auth,
            json=payload,
        )

        response.raise_for_status()

        return response.json()

    def put(
        self,
        endpoint,
        payload=None,
    ):
        response = requests.put(
            f"{self.base_url}{endpoint}",
            headers=self.headers,
            auth=self.auth,
            json=payload,
        )

        response.raise_for_status()

        if response.text:
            return response.json()

        return {}