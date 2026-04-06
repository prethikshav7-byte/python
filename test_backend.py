from functions import *

print("---- TESTING BACKEND ----")

# 1. Register User
print("\nRegistering user...")
register_user("testuser", "1234")

# 2. Login User
print("\nLogging in...")
user = login_user("testuser", "1234")

if user:
    print("Login Successful:", user)
    user_id = user[0]
else:
    print("Login Failed")
    exit()

# 3. Add Expenses
print("\nAdding expenses...")
add_expense(user_id, "Food", 200, "Food", "2026-04-06", "INR")
add_expense(user_id, "Transport", 100, "Travel", "2026-04-05", "INR")

# 4. View Expenses
print("\nAll Expenses:")
expenses = view_expenses(user_id)
for e in expenses:
    print(e)

# 5. Edit Expense
print("\nEditing first expense...")
if expenses:
    first_id = expenses[0][0]
    edit_expense(first_id, "Food Updated", 250, "Food", "2026-04-06", "INR")

# 6. Delete Expense
print("\nDeleting second expense...")
if len(expenses) > 1:
    delete_expense(expenses[1][0])

# 7. Filter Test
print("\nFiltered Expenses (amount >= 200):")
filtered = filter_expenses(user_id, min_amount=200)
for f in filtered:
    print(f)

# 8. Summary
print("\nTotal Expense:", get_total_expense(user_id))
print("Total Transactions:", get_total_transactions(user_id))

# 9. Category Summary
print("\nCategory Summary:")
print(category_summary(user_id))

# 10. Budget Test
print("\nSetting budget...")
set_budget(user_id, 300)

print("Budget Status:", check_budget(user_id))

# 11. Export CSV
print("\nExporting CSV...")
file = export_to_csv(user_id)
print("Saved as:", file)

print("\n---- ALL TESTS COMPLETED ----")