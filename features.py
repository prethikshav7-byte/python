# 🔥 SUPER FEATURES - Person 4
# Copy EXACTLY ra!

import sqlite3
import pandas as pd
import hashlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

# DB Connection (P1 creates exp.db)
def get_db():
    return sqlite3.connect('exp.db')

# =====================================
# 1. SECURE LOGIN HELP (P2 uses this)
# =====================================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# =====================================
# 2. DASHBOARD STATS + TREND LINE GRAPH
# =====================================
def dashboard_stats():
    conn = get_db()
    total = pd.read_sql("SELECT COALESCE(SUM(amt),0) as total FROM expenses", conn).iloc[0,0]
    monthly = pd.read_sql("""
        SELECT strftime('%Y-%m', date) as month, 
               COALESCE(SUM(amt),0) as total 
        FROM expenses GROUP BY month ORDER BY month
    """, conn)
    conn.close()
    return {"total_spent": total, "monthly": monthly}

def trend_line_graph(parent_window):
    stats = dashboard_stats()
    if stats['monthly'].empty:
        tk.Label(parent_window, text="No data for trend").pack()
        return
    
    fig, ax = plt.subplots(figsize=(10, 6))
    months = stats['monthly']['month'].tolist()
    amounts = stats['monthly']['total'].tolist()
    
    ax.plot(months, amounts, marker='o', linewidth=3, markersize=8, color='#3498db')
    ax.fill_between(months, amounts, alpha=0.3, color='#3498db')
    ax.set_title("📈 Monthly Spending Trend", fontsize=16, fontweight='bold')
    ax.set_xlabel("Month")
    ax.set_ylabel("Amount (₹)")
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True, alpha=0.3)
    
    canvas = FigureCanvasTkAgg(fig, parent_window)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=20)

# =====================================
# 3. PIE CHART CATEGORY ANALYSIS
# =====================================
def pie_chart_analysis(parent_window):
    conn = get_db()
    df = pd.read_sql("""
        SELECT cat, COALESCE(SUM(amt),0) as total 
        FROM expenses GROUP BY cat
    """, conn)
    conn.close()
    
    if df.empty:
        tk.Label(parent_window, text="No category data").pack()
        return
    
    fig, ax = plt.subplots(figsize=(8, 8))
    colors = plt.cm.Set3(range(len(df)))
    wedges, texts, autotexts = ax.pie(df['total'], 
                                     labels=df['cat'], 
                                     autopct='%1.1f%%',
                                     colors=colors,
                                     startangle=90)
    ax.set_title("📊 Category-wise Spending Analysis", fontsize=16, fontweight='bold')
    
    canvas = FigureCanvasTkAgg(fig, parent_window)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=20)

# =====================================
# 4. BUDGET ALERT SYSTEM
# =====================================
budget_limits = {"Food": 5000, "Travel": 3000, "Entertainment": 2000, "All": 15000}
def budget_alert(category="All"):
    conn = get_db()
    total = pd.read_sql(f"SELECT COALESCE(SUM(amt),0) FROM expenses WHERE cat='{category}' OR '{category}'='All'", conn).iloc[0,0]
    conn.close()
    
    limit = budget_limits.get(category, 5000)
    if total > limit:
        return f"🚨 ALERT: {category}\nSpent: ₹{total:.0f}\nLimit: ₹{limit}\nEXCEEDED BY ₹{total-limit:.0f}"
    return f"✅ {category} Budget OK\nSpent: ₹{total:.0f} / ₹{limit}"

# =====================================
# 5. ADVANCED FILTERS
# =====================================
def advanced_filter(date_from="", date_to="", min_amount=0, keyword=""):
    conn = get_db()
    query = "SELECT * FROM expenses WHERE 1=1"
    params = []
    
    if date_from: 
        query += " AND date >= ?"
        params.append(date_from)
    if date_to: 
        query += " AND date <= ?"
        params.append(date_to)
    if min_amount > 0:
        query += " AND amt >= ?"
        params.append(min_amount)
    if keyword:
        query += " AND (cat LIKE ? OR desc LIKE ?)"
        params.extend([f"%{keyword}%", f"%{keyword}%"])
    
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df

# =====================================
# 6. EXPORT CSV REPORT
# =====================================
def export_report():
    conn = get_db()
    df = pd.read_sql("""
        SELECT date, amt, cat, desc FROM expenses 
        ORDER BY date DESC
    """, conn)
    filename = f'expense_report_{datetime.now().strftime("%Y%m%d")}.csv'
    df.to_csv(filename, index=False)
    conn.close()
    return f"📤 {filename} exported successfully!"

# =====================================
# 3. MULTI-CURRENCY SUPPORT
# =====================================
CURRENCY_RATES = {"INR": 1.0, "USD": 0.012, "EUR": 0.011}
def convert_currency(amount, from_curr="INR", to_curr="INR"):
    return amount * CURRENCY_RATES[to_curr] / CURRENCY_RATES[from_curr]

# =====================================
# 9. DARK/LIGHT MODE
# =====================================
def toggle_dark_mode(root, dark_mode=True):
    if dark_mode:
        root.configure(bg='#2c3e50')
        style = ttk.Style(root)
        style.configure("TButton", background="#34495e", foreground="white")
        style.configure("TLabel", background="#2c3e50", foreground="white")
    else:
        root.configure(bg='white')
        style.configure("TButton", background="#3498db")
        style.configure("TLabel", foreground="black")

# =====================================
# SAVINGS GOAL TRACKER (Bonus)
# =====================================
savings_goals = {"Emergency Fund": 50000, "Vacation": 25000, "New Phone": 30000}
def goal_progress(goal_name):
    total_saved = dashboard_stats()['total_spent'] * 0.1  # Assume 10% auto-save
    target = savings_goals.get(goal_name, 0)
    progress = (total_saved / target) * 100 if target else 0
    return f"{goal_name}: ₹{total_saved:.0f}/{target} ({progress:.1f}%)"

print("🚀 SUPER FEATURES LOADED! Ready for integration.")
