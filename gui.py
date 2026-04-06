from datetime import date
from db import get_connection

_current_user_id = None


def set_current_user(user_id: int):
    global _current_user_id
    _current_user_id = user_id


def get_current_user():
    return _current_user_id


def add_expense(title, amount, category, currency="₹", expense_type="Expense", expense_date=None):
    if _current_user_id is None:
        return False, "Please login first."

    title = title.strip()
    category = category.strip() or "Other"
    expense_type = expense_type.strip() or "Expense"

    if not title:
        return False, "Title is required."

    try:
        amount_value = float(amount)
    except ValueError:
        return False, "Amount must be a number."

    if expense_date is None:
        expense_date = date.today().isoformat()

    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO expenses (user_id, title, amount, category, currency, expense_type, expense_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (_current_user_id, title, amount_value, category, currency, expense_type, expense_date),
        )

    return True, "Entry saved."


def view_expenses(search_text=""):
    if _current_user_id is None:
        return []

    query = (
        "SELECT id, title, amount, category, currency, expense_type, expense_date "
        "FROM expenses WHERE user_id = ?"
    )
    params = [_current_user_id]

    if search_text.strip():
        query += " AND (title LIKE ? OR category LIKE ? OR expense_type LIKE ?)"
        token = f"%{search_text.strip()}%"
        params.extend([token, token, token])

    query += " ORDER BY expense_date DESC, id DESC"

    with get_connection() as conn:
        rows = conn.execute(query, params).fetchall()

    return [dict(row) for row in rows]


def delete_expense(expense_id):
    if _current_user_id is None:
        return False

    with get_connection() as conn:
        cur = conn.execute(
            "DELETE FROM expenses WHERE id = ? AND user_id = ?",
            (expense_id, _current_user_id),
        )
    return cur.rowcount > 0


def get_summary():
    if _current_user_id is None:
        return {"income": 0.0, "expense": 0.0, "balance": 0.0}

    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT expense_type, COALESCE(SUM(amount), 0) AS total
            FROM expenses
            WHERE user_id = ?
            GROUP BY expense_type
            """,
            (_current_user_id,),
        ).fetchall()

    income = 0.0
    expense = 0.0
    for row in rows:
        if row["expense_type"].lower() == "income":
            income += float(row["total"])
        else:
            expense += float(row["total"])

    return {
        "income": income,
        "expense": expense,
        "balance": income - expense,
    }