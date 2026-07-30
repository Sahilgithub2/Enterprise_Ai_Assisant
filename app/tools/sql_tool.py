from sqlalchemy.orm import Session

from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import GEMINI_API_KEY
import os
from app.prompts.sql_prompt import sql_prompt
from langchain_openai import AzureChatOpenAI
from app.services.sql_service import execute_sql


llm = AzureChatOpenAI(
    azure_endpoint=os.environ["AZURE_API_BASE"],
    api_key=os.environ["AZURE_API_KEY"],
    api_version=os.environ["AZURE_API_VERSION"],
    azure_deployment="gpt-5"
)



def generate_sql(
    question: str,
    previous_context: str = "",
):
    prompt = sql_prompt.invoke(
        {
            "question": question,
        }
    )

    response = llm.invoke(prompt)

    sql = response.content.strip()

    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")
    sql = sql.strip()

    return sql


def get_sql_context(
    db: Session,
    question: str,
):
    print("\n========== SQL AGENT ==========\n")

    sql = generate_sql(question)

    print("Generated SQL\n")
    print(sql)

    rows = execute_sql(
        db,
        sql,
    )

    if not rows:
        context = "The query returned no records."

    else:
        formatted_rows = []

        for row in rows:
            formatted_rows.append(str(row))

        context = "\n".join(formatted_rows)

    return {
        "context": context,
        "sql": sql,
        "rows": rows,
        "source": "Application Database",
    }