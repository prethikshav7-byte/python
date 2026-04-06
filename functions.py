import hashlib
import csv
from db import get_connection

# =========================
# 🔐 AUTHENTICATION
# =========================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    hashed = hash_password(password)

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, hashed)
        )
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()


def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    hashed = hash_password(password)

    cursor.execute(
        "SELECT id, username FROM users WHERE username=%s AND password=%s",
        (username, hashed)
    )

    user = cursor.fetchone()
    conn.close()

    return user  # returns (id, username) or None


# =========================
# 💰 CRUD OPERATIONS
# =========================

def add_expense(user_id, title, amount, category, date, currency):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO expenses (user_id, title, amount, category, date, currency)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (user_id, title, amount, category, date, currency))

    conn.commit()
    conn.close()


def view_expenses(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM expenses WHERE user_id=%s ORDER BY date DESC",
        (user_id,)
    )

    data = cursor.fetchall()
    conn.close()

    return data


def delete_expense(expense_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM expenses WHERE id=%s",
        (expense_id,)
    )

    conn.commit()
    conn.close()


def edit_expense(expense_id, title, amount, category, date, currency):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE expenses
        SET title=%s, amount=%s, category=%s, date=%s, currency=%s
        WHERE id=%s
    """, (title, amount, category, date, currency, expense_id))

    conn.commit()
    conn.close()


# =========================
# 🔍 ADVANCED FILTERS
# =========================

def filter_expenses(user_id, start_date=None, end_date=None, min_amount=None, keyword=None):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM expenses WHERE user_id=%s"
    params = [user_id]

    if start_date and end_date:
        query += " AND date BETWEEN %s AND %s"
        params.extend([start_date, end_date])

    if min_amount:
        query += " AND amount >= %s"
        params.append(min_amount)

    if keyword:
        query += " AND title LIKE %s"
        params.append(f"%{keyword}%")

    query += " ORDER BY date DESC"

    cursor.execute(query, tuple(params))
    data = cursor.fetchall()

    conn.close()
    return data


# =========================
# 📊 DASHBOARD / SUMMARY
# =========================

def get_total_expense(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT SUM(amount) FROM expenses WHERE user_id=%s",
        (user_id,)
    )

    total = cursor.fetchone()[0]
    conn.close()

    return total if total else 0


def get_total_transactions(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM expenses WHERE user_id=%s",
        (user_id,)
    )

    count = cursor.fetchone()[0]
    conn.close()

    return count


def category_summary(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        WHERE user_id=%s
        GROUP BY category
    """, (user_id,))

    data = cursor.fetchall()
    conn.close()

    return data


def monthly_trend(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DATE(date), SUM(amount)
        FROM expenses
        WHERE user_id=%s
        GROUP BY DATE(date)
        ORDER BY DATE(date)
    """, (user_id,))

    data = cursor.fetchall()
    conn.close()

    return data


# =========================
# 🎯 BUDGET SYSTEM
# =========================

def set_budget(user_id, limit):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM budget WHERE user_id=%s", (user_id,))
    cursor.execute(
        "INSERT INTO budget (user_id, monthly_limit) VALUES (%s, %s)",
        (user_id, limit)
    )

    conn.commit()
    conn.close()


def check_budget(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT monthly_limit FROM budget WHERE user_id=%s",
        (user_id,)
    )
    budget = cursor.fetchone()

    cursor.execute(
        "SELECT SUM(amount) FROM expenses WHERE user_id=%s",
        (user_id,)
    )
    total = cursor.fetchone()[0] or 0

    conn.close()

    if budget:
        if total > budget[0]:
            return f"⚠️ Budget Exceeded! ({total} / {budget[0]})"
        else:
            return f"✅ Within Budget ({total} / {budget[0]})"
    else:
        return "No budget set"


# =========================
# 📤 EXPORT CSV
# =========================

def export_to_csv(user_id, filename="expenses.csv"):
    data = view_expenses(user_id)

    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "ID", "User ID", "Title", "Amount",
            "Category", "Date", "Currency"
        ])

        writer.writerows(data)

    return filename