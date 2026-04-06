# ================================
# TEST FILE: test_super_features.py
# ================================

import sqlite3
from datetime import datetime
import tkinter as tk

# Import your functions
from features import *

# --------------------------------
# 1. SETUP TEST DATABASE
# --------------------------------
def setup_test_db():
    conn = sqlite3.connect('exp.db')
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        amt REAL,
        cat TEXT,
        desc TEXT
    )
    """)

    # Insert sample data
    sample_data = [
        ("2026-03-01", 500, "Food", "Lunch"),
        ("2026-03-02", 1200, "Travel", "Bus pass"),
        ("2026-03-05", 800, "Food", "Dinner"),
        ("2026-03-10", 1500, "Entertainment", "Movies"),
        ("2026-04-01", 2000, "Food", "Groceries"),
        ("2026-04-02", 1000, "Travel", "Taxi"),
    ]

    cursor.executemany(
        "INSERT INTO expenses (date, amt, cat, desc) VALUES (?, ?, ?, ?)",
        sample_data
    )

    conn.commit()
    conn.close()

    print("✅ Test DB ready with sample data")

# --------------------------------
# 2. TEST PASSWORD HASH
# --------------------------------
def test_hash():
    print("\n🔐 Testing Password Hash")
    pwd = "mypassword"
    print("Original:", pwd)
    print("Hashed :", hash_password(pwd))

# --------------------------------
# 3. TEST DASHBOARD
# --------------------------------
def test_dashboard():
    print("\n📊 Testing Dashboard Stats")
    stats = dashboard_stats()
    print("Total Spent:", stats['total_spent'])
    print(stats['monthly'])

# --------------------------------
# 4. TEST TREND GRAPH (GUI)
# --------------------------------
def test_trend_graph():
    root = tk.Tk()
    root.title("Trend Graph Test")
    trend_line_graph(root)
    root.mainloop()

# --------------------------------
# 5. TEST PIE CHART
# --------------------------------
def test_pie_chart():
    root = tk.Tk()
    root.title("Pie Chart Test")
    pie_chart_analysis(root)
    root.mainloop()

# --------------------------------
# 6. TEST BUDGET ALERT
# --------------------------------
def test_budget():
    print("\n🚨 Testing Budget Alerts")
    print(budget_alert("Food"))
    print(budget_alert("Travel"))
    print(budget_alert("All"))

# --------------------------------
# 7. TEST FILTER
# --------------------------------
def test_filter():
    print("\n🔍 Testing Advanced Filter")
    df = advanced_filter(date_from="2026-03-01", min_amount=700)
    print(df)

# --------------------------------
# 8. TEST EXPORT
# --------------------------------
def test_export():
    print("\n📤 Testing Export")
    print(export_report())

# --------------------------------
# 9. TEST CURRENCY
# --------------------------------
def test_currency():
    print("\n💱 Testing Currency Conversion")
    print("₹1000 in USD:", convert_currency(1000, "INR", "USD"))

# --------------------------------
# 10. TEST GOALS
# --------------------------------
def test_goals():
    print("\n🎯 Testing Goals")
    print(goal_progress("Vacation"))

# --------------------------------
# MAIN RUNNER
# --------------------------------
if __name__ == "__main__":
    setup_test_db()
    test_hash()
    test_dashboard()
    test_budget()
    test_filter()
    test_export()
    test_currency()
    test_goals()

    # Uncomment these to test GUI graphs
    # test_trend_graph()
    # test_pie_chart()