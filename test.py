from functions import *

# Register
register_user("lakshitha", "1234")

# Login
user = login_user("lakshitha", "1234")
print("User:", user)

user_id = user[0]

# Add expense
add_expense(user_id, "Food", 200, "Food", "2026-04-06", "INR")

# View
print(view_expenses(user_id))

# Summary
print("Total:", get_total_expense(user_id))

# Budget
set_budget(user_id, 5000)
print(check_budget(user_id))

# Export
export_to_csv(user_id)