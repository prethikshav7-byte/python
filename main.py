import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import mysql.connector
from datetime import datetime
import csv

# ---------- Database Setup ----------
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",         # Change as needed
            password="",         # Change as needed
            database="expense_tracker"
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None

def setup_database():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",         # Change as needed
        password=""
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS expense_tracker")
    cursor.execute("USE expense_tracker")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE,
            password VARCHAR(50),
            fullname VARCHAR(100),
            email VARCHAR(100)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            amount FLOAT,
            category VARCHAR(50),
            description VARCHAR(255),
            date DATE,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    conn.close()

setup_database()

# ---------- Main Application Class ----------
class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.current_user = None
        self.categories = ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Health", "Other"]
        self.show_login_window()

    # ---------- Window Functions ----------
    def show_login_window(self):
        self.clear_window()
        self.root.geometry("350x250")
        tk.Label(self.root, text="Login", font=("Arial", 18, "bold")).pack(pady=10)
        tk.Label(self.root, text="Username").pack()
        self.login_username = tk.Entry(self.root)
        self.login_username.pack()
        tk.Label(self.root, text="Password").pack()
        self.login_password = tk.Entry(self.root, show="*")
        self.login_password.pack()
        tk.Button(self.root, text="Login", command=self.login_user, width=15, bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(self.root, text="Register", command=self.show_register_window, width=15).pack()

    def show_register_window(self):
        reg_win = tk.Toplevel(self.root)
        reg_win.title("Register")
        reg_win.geometry("350x350")
        tk.Label(reg_win, text="Register", font=("Arial", 18, "bold")).pack(pady=10)
        tk.Label(reg_win, text="Full Name").pack()
        fullname = tk.Entry(reg_win)
        fullname.pack()
        tk.Label(reg_win, text="Email").pack()
        email = tk.Entry(reg_win)
        email.pack()
        tk.Label(reg_win, text="Username").pack()
        username = tk.Entry(reg_win)
        username.pack()
        tk.Label(reg_win, text="Password").pack()
        password = tk.Entry(reg_win, show="*")
        password.pack()
        def register():
            fn = fullname.get().strip()
            em = email.get().strip()
            un = username.get().strip()
            pw = password.get().strip()
            if not (fn and em and un and pw):
                messagebox.showerror("Error", "All fields are required!", parent=reg_win)
                return
            conn = get_db_connection()
            if not conn: return
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO users (fullname, email, username, password) VALUES (%s,%s,%s,%s)",
                               (fn, em, un, pw))
                conn.commit()
                messagebox.showinfo("Success", "Registration successful!", parent=reg_win)
                reg_win.destroy()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Username already exists!", parent=reg_win)
            finally:
                conn.close()
        tk.Button(reg_win, text="Register", command=register, width=15, bg="#4CAF50", fg="white").pack(pady=10)

    def show_dashboard(self):
        self.clear_window()
        self.root.geometry("400x400")
        tk.Label(self.root, text=f"Welcome, {self.current_user['fullname']}", font=("Arial", 16, "bold")).pack(pady=10)
        btns = [
            ("Add Expense", self.show_add_expense_window),
            ("View Expenses", self.show_view_expenses_window),
            ("Summary Report", self.show_summary_window),
            ("Search/Filter Expenses", self.show_search_window),
            ("Settings/Profile", self.show_settings_window),
            ("Logout", self.logout)
        ]
        for text, cmd in btns:
            tk.Button(self.root, text=text, command=cmd, width=25, height=2, font=("Arial", 12)).pack(pady=5)

    def show_add_expense_window(self):
        add_win = tk.Toplevel(self.root)
        add_win.title("Add Expense")
        add_win.geometry("350x350")
        tk.Label(add_win, text="Add Expense", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(add_win, text="Amount").pack()
        amount = tk.Entry(add_win)
        amount.pack()
        tk.Label(add_win, text="Category").pack()
        category = ttk.Combobox(add_win, values=self.categories, state="readonly")
        category.current(0)
        category.pack()
        tk.Label(add_win, text="Description").pack()
        description = tk.Entry(add_win)
        description.pack()
        tk.Label(add_win, text="Date (YYYY-MM-DD)").pack()
        date = tk.Entry(add_win)
        date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        date.pack()
        def add_expense():
            try:
                amt = float(amount.get())
                cat = category.get()
                desc = description.get().strip()
                dt = date.get().strip()
                if not (amt and cat and dt):
                    raise ValueError
                conn = get_db_connection()
                if not conn: return
                cursor = conn.cursor()
                cursor.execute("INSERT INTO expenses (user_id, amount, category, description, date) VALUES (%s,%s,%s,%s,%s)",
                               (self.current_user['id'], amt, cat, desc, dt))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Expense added!", parent=add_win)
                add_win.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid data!", parent=add_win)
        tk.Button(add_win, text="Add", command=add_expense, width=15, bg="#4CAF50", fg="white").pack(pady=10)

    def show_view_expenses_window(self):
        view_win = tk.Toplevel(self.root)
        view_win.title("View Expenses")
        view_win.geometry("700x400")
        tk.Label(view_win, text="Your Expenses", font=("Arial", 16, "bold")).pack(pady=10)
        columns = ("id", "amount", "category", "description", "date")
        tree = ttk.Treeview(view_win, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col.capitalize())
            tree.column(col, width=100)
        tree.pack(fill=tk.BOTH, expand=True)
        def load_expenses():
            conn = get_db_connection()
            if not conn: return
            cursor = conn.cursor()
            cursor.execute("SELECT id, amount, category, description, date FROM expenses WHERE user_id=%s", (self.current_user['id'],))
            for row in cursor.fetchall():
                tree.insert("", tk.END, values=row)
            conn.close()
        load_expenses()
        def on_select(event):
            selected = tree.focus()
            if not selected: return
            values = tree.item(selected, "values")
            self.show_edit_expense_window(values, view_win, tree)
        tree.bind("<Double-1>", on_select)
        tk.Button(view_win, text="Export to CSV", command=lambda: self.export_to_csv(tree), width=15).pack(pady=5)

    def show_edit_expense_window(self, values, parent, tree):
        edit_win = tk.Toplevel(parent)
        edit_win.title("Edit Expense")
        edit_win.geometry("350x350")
        tk.Label(edit_win, text="Edit Expense", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(edit_win, text="Amount").pack()
        amount = tk.Entry(edit_win)
        amount.insert(0, values[1])
        amount.pack()
        tk.Label(edit_win, text="Category").pack()
        category = ttk.Combobox(edit_win, values=self.categories, state="readonly")
        category.set(values[2])
        category.pack()
        tk.Label(edit_win, text="Description").pack()
        description = tk.Entry(edit_win)
        description.insert(0, values[3])
        description.pack()
        tk.Label(edit_win, text="Date (YYYY-MM-DD)").pack()
        date = tk.Entry(edit_win)
        date.insert(0, values[4])
        date.pack()
        def update_expense():
            try:
                amt = float(amount.get())
                cat = category.get()
                desc = description.get().strip()
                dt = date.get().strip()
                if not (amt and cat and dt):
                    raise ValueError
                conn = get_db_connection()
                if not conn: return
                cursor = conn.cursor()
                cursor.execute("UPDATE expenses SET amount=%s, category=%s, description=%s, date=%s WHERE id=%s",
                               (amt, cat, desc, dt, values[0]))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Expense updated!", parent=edit_win)
                edit_win.destroy()
                tree.delete(*tree.get_children())
                parent.destroy()
                self.show_view_expenses_window()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid data!", parent=edit_win)
        def delete_expense():
            if messagebox.askyesno("Confirm", "Delete this expense?", parent=edit_win):
                conn = get_db_connection()
                if not conn: return
                cursor = conn.cursor()
                cursor.execute("DELETE FROM expenses WHERE id=%s", (values[0],))
                conn.commit()
                conn.close()
                messagebox.showinfo("Deleted", "Expense deleted!", parent=edit_win)
                edit_win.destroy()
                tree.delete(*tree.get_children())
                parent.destroy()
                self.show_view_expenses_window()
        tk.Button(edit_win, text="Update", command=update_expense, width=15, bg="#4CAF50", fg="white").pack(pady=5)
        tk.Button(edit_win, text="Delete", command=delete_expense, width=15, bg="#f44336", fg="white").pack(pady=5)

    def show_summary_window(self):
        sum_win = tk.Toplevel(self.root)
        sum_win.title("Summary Report")
        sum_win.geometry("400x400")
        tk.Label(sum_win, text="Summary Report", font=("Arial", 16, "bold")).pack(pady=10)
        conn = get_db_connection()
        if not conn: return
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(amount) FROM expenses WHERE user_id=%s", (self.current_user['id'],))
        total = cursor.fetchone()[0] or 0
        tk.Label(sum_win, text=f"Total Expenses: Rs. {total:.2f}", font=("Arial", 14)).pack(pady=10)
        tk.Label(sum_win, text="Category-wise Breakdown:", font=("Arial", 12, "bold")).pack(pady=5)
        for cat in self.categories:
            cursor.execute("SELECT SUM(amount) FROM expenses WHERE user_id=%s AND category=%s", (self.current_user['id'], cat))
            cat_total = cursor.fetchone()[0] or 0
            tk.Label(sum_win, text=f"{cat}: Rs. {cat_total:.2f}", font=("Arial", 11)).pack()
        conn.close()

    def show_search_window(self):
        search_win = tk.Toplevel(self.root)
        search_win.title("Search/Filter Expenses")
        search_win.geometry("700x400")
        tk.Label(search_win, text="Search/Filter Expenses", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(search_win, text="Category").pack()
        category = ttk.Combobox(search_win, values=["All"] + self.categories, state="readonly")
        category.current(0)
        category.pack()
        tk.Label(search_win, text="Date (YYYY-MM-DD or leave blank)").pack()
        date = tk.Entry(search_win)
        date.pack()
        columns = ("id", "amount", "category", "description", "date")
        tree = ttk.Treeview(search_win, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col.capitalize())
            tree.column(col, width=100)
        tree.pack(fill=tk.BOTH, expand=True)
        def search():
            cat = category.get()
            dt = date.get().strip()
            conn = get_db_connection()
            if not conn: return
            cursor = conn.cursor()
            query = "SELECT id, amount, category, description, date FROM expenses WHERE user_id=%s"
            params = [self.current_user['id']]
            if cat != "All":
                query += " AND category=%s"
                params.append(cat)
            if dt:
                query += " AND date=%s"
                params.append(dt)
            cursor.execute(query, tuple(params))
            tree.delete(*tree.get_children())
            for row in cursor.fetchall():
                tree.insert("", tk.END, values=row)
            conn.close()
        tk.Button(search_win, text="Search", command=search, width=15, bg="#2196F3", fg="white").pack(pady=5)

    def show_settings_window(self):
        set_win = tk.Toplevel(self.root)
        set_win.title("Settings / Profile")
        set_win.geometry("350x350")
        tk.Label(set_win, text="Profile", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(set_win, text=f"Full Name: {self.current_user['fullname']}").pack(pady=5)
        tk.Label(set_win, text=f"Email: {self.current_user['email']}").pack(pady=5)
        tk.Label(set_win, text=f"Username: {self.current_user['username']}").pack(pady=5)
        tk.Label(set_win, text="Change Password").pack(pady=10)
        old_pw = tk.Entry(set_win, show="*")
        old_pw.pack()
        tk.Label(set_win, text="New Password").pack()
        new_pw = tk.Entry(set_win, show="*")
        new_pw.pack()
        def change_password():
            old = old_pw.get().strip()
            new = new_pw.get().strip()
            if not (old and new):
                messagebox.showerror("Error", "Both fields required!", parent=set_win)
                return
            if old != self.current_user['password']:
                messagebox.showerror("Error", "Old password incorrect!", parent=set_win)
                return
            conn = get_db_connection()
            if not conn: return
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET password=%s WHERE id=%s", (new, self.current_user['id']))
            conn.commit()
            conn.close()
            self.current_user['password'] = new
            messagebox.showinfo("Success", "Password changed!", parent=set_win)
            set_win.destroy()
        tk.Button(set_win, text="Change Password", command=change_password, width=15, bg="#4CAF50", fg="white").pack(pady=10)

    # ---------- Helper Functions ----------
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login_user(self):
        un = self.login_username.get().strip()
        pw = self.login_password.get().strip()
        if not (un and pw):
            messagebox.showerror("Error", "All fields required!")
            return
        conn = get_db_connection()
        if not conn: return
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (un, pw))
        user = cursor.fetchone()
        conn.close()
        if user:
            self.current_user = user
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid credentials!")

    def logout(self):
        self.current_user = None
        self.show_login_window()

    def export_to_csv(self, tree):
        rows = [tree.item(child)["values"] for child in tree.get_children()]
        if not rows:
            messagebox.showerror("Error", "No data to export!")
            return
        file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not file:
            return
        with open(file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Amount", "Category", "Description", "Date"])
            writer.writerows(rows)
        messagebox.showinfo("Success", "Exported to CSV!")

# ---------- Run Application ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
