from sqlalchemy import text

from sqlalchemy.orm import Session


FORBIDDEN_KEYWORDS = [
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "TRUNCATE",
    "CREATE",
]


def validate_sql(
    sql: str,
):

    upper_sql = sql.upper().strip()

    if not upper_sql.startswith("SELECT"):
        raise ValueError(
            "Only SELECT queries are allowed."
        )

    for keyword in FORBIDDEN_KEYWORDS:

        if keyword in upper_sql:

            raise ValueError(
                f"{keyword} statements are not allowed."
            )


def execute_sql(
    db: Session,
    sql: str,
):

    validate_sql(sql)

    result = db.execute(
        text(sql)
    )

    rows = result.fetchall()

    columns = result.keys()

    formatted_rows = []

    for row in rows:

        formatted_rows.append(
            dict(zip(columns, row))
        )

    return formatted_rows