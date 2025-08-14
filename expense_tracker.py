import sqlite3
import datetime

# Database setup
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        category TEXT,
        description TEXT,
        amount REAL
    )
''')
conn.commit()

def add_expense():
    date = input("Enter date (YYYY-MM-DD) or leave blank for today: ")
    if not date:
        date = datetime.date.today().strftime("%Y-%m-%d")
    category = input("Enter category (Food, Travel, etc.): ")
    description = input("Enter description: ")
    
    try:
        amount = float(input("Enter amount: "))
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return
    
    cursor.execute("INSERT INTO expenses (date, category, description, amount) VALUES (?, ?, ?, ?)",
                   (date, category, description, amount))
    conn.commit()
    print("✅ Expense added successfully!")

def view_expenses():
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()
    print("\n--- All Expenses ---")
    print("{:<5} {:<12} {:<12} {:<20} {:<10}".format("ID", "Date", "Category", "Description", "Amount"))
    print("-" * 60)
    for row in rows:
        print("{:<5} {:<12} {:<12} {:<20} {:<10.2f}".format(row[0], row[1], row[2], row[3], row[4]))

def delete_expense():
    try:
        expense_id = int(input("Enter expense ID to delete: "))
    except ValueError:
        print("Invalid ID.")
        return
    
    cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    conn.commit()
    print("🗑 Expense deleted successfully!")

def monthly_summary():
    month = input("Enter month (MM): ")
    cursor.execute("SELECT category, SUM(amount) FROM expenses WHERE strftime('%m', date) = ? GROUP BY category", (month,))
    rows = cursor.fetchall()
    
    if not rows:
        print("No expenses found for this month.")
        return
    
    print(f"\n--- Monthly Summary for {month} ---")
    print("{:<12} {:<10}".format("Category", "Total"))
    print("-" * 30)
    total_all = 0
    for row in rows:
        print("{:<12} {:<10.2f}".format(row[0], row[1]))
        total_all += row[1]
    print("-" * 30)
    print(f"Total: ₹{total_all:.2f}")

# Main Menu
while True:
    print("\n--- Personal Expense Tracker ---")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Delete Expense")
    print("4. Monthly Summary")
    print("5. Exit")
    
    choice = input("Choose an option: ")
    
    if choice == "1":
        add_expense()
    elif choice == "2":
        view_expenses()
    elif choice == "3":
        delete_expense()
    elif choice == "4":
        monthly_summary()
    elif choice == "5":
        print("Goodbye! 👋")
        break
    else:
        print("❌ Invalid choice. Try again.")

conn.close()
