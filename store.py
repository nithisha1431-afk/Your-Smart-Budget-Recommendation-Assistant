import json

from app.database import get_connection


def create_user(
    name,
    email,
    password_hash
):
    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO users
        (name, email, password_hash)
        VALUES (?, ?, ?)
        """,
        (
            name,
            email.lower(),
            password_hash,
        )
    )

    connection.commit()

    user_id = cursor.lastrowid

    connection.close()

    return user_id


def get_user_by_email(email):
    connection = get_connection()

    row = connection.execute(
        """
        SELECT *
        FROM users
        WHERE email = ?
        """,
        (email.lower(),)
    ).fetchone()

    connection.close()

    return dict(row) if row else None


def save_recommendation(
    user_id,
    planner,
    budget,
    request_data,
    result
):
    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO recommendations
        (
            user_id,
            planner,
            budget,
            request_json,
            result_json
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            user_id,
            planner,
            budget,
            json.dumps(request_data),
            json.dumps(result),
        )
    )

    connection.commit()

    recommendation_id = cursor.lastrowid

    connection.close()

    return recommendation_id


def history(user_id, limit=20):
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT *
        FROM recommendations
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (user_id, limit)
    ).fetchall()

    connection.close()

    return [
        dict(row)
        for row in rows
    ]