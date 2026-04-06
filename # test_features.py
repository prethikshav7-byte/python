# test_features.py - RUN THIS!
import sqlite3
import tkinter as tk
from feature import *  # Your super_features

# STEP 1: Create test database
print("🔄 Creating test database...")
conn = sqlite3.connect('exp.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS expenses 
             (id INTEGER PRIMARY KEY, date TEXT, amt REAL, cat TEXT)''')
c.execute("INSERT OR REPLACE INTO expenses VALUES 
          (1,'2026-04-01',2500,'Food'),
          (2,'2026-04-02',1500,'Travel'),
          (3,'2026-04-03',800,'Snacks'),
          (4,'2026-04-04',1200,'Food'),
          (5,'2026-04-05',900,'Travel')")
conn.commit()
conn.close()
print("✅ Database ready with 5 records!")

# STEP 2: Test window
root = tk.Tk()
root.title("🚀 SUPER FEATURES TEST")
root.geometry("1100x800")
root.configure(bg="#1e1e1e")

# Title
tk.Label(root, text="10 SUPER FEATURES WORKING LIVE!", fg="#ecf0f1", bg="#1e1e1e", 
         font=("Arial", 22, "bold")).pack(pady=30)

# Budget alert
alert_text = budget_alert("Food")
tk.Label(root, text=alert_text, fg="#e74c3c" if "ALERT" in alert_text else "#2ecc71", 
         bg="#1e1e1e", font=("Arial", 16, "bold")).pack(pady=20)

# Test buttons
tk.Button(root, text="📈 TREND GRAPH", font=("Arial", 16, "bold"), bg="#3498db", fg="white",
          height=2, width=20, command=lambda: trend_line_graph(root)).pack(pady=15)

tk.Button(root, text="📊 PIE CHART", font=("Arial", 16, "bold"), bg="#e74c3c", fg="white",
          height=2, width=20, command=lambda: pie_chart_analysis(root)).pack(pady=15)

tk.Button(root, text="📤 EXPORT REPORT", font=("Arial", 16, "bold"), bg="#27ae60", fg="white",
          height=2, width=20, command=lambda: print(export_report())).pack(pady=15)

tk.Button(root, text="🌙 DARK MODE", font=("Arial", 16, "bold"), bg="#9b59b6", fg="white",
          height=2, width=20, command=lambda: toggle_dark_mode(root, True)).pack(pady=15)

print("✅ Window opening... Click buttons to test!")
root.mainloop()
