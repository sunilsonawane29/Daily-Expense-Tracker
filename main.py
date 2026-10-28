
import csv
import os
from datetime import date

FILE = "expenses.csv"
FIELDS = ["date", "category", "amount", "note"]


def load_expenses():
    """Load expense records from the CSV file."""
    """Save a new expense to the CSV file."""
    """Display all recorded expenses."""
    """Calculate and display spending totals."""

def add_expense(category, amount, note):
    if amount <= 0:
        raise ValueError("Amount must be positive")

    exists = os.path.exists(FILE)
    with open(FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        if not exists or os.path.getsize(FILE) == 0:
            writer.writeheader()
        writer.writerow({
            "date": date.today().isoformat(),
            "category": category,
            "amount": f"{amount:.2f}",
            "note": note
        })


def show_expenses():
    expenses = load_expenses()
    if not expenses:
        print("No expenses recorded yet.")
        return

    print("\n--- Your Expenses ---")
    for item in expenses:
        print(
            f"{item['date']} | {item['category']} | "
            f"Rs. {float(item['amount']):.2f} | {item['note']}"
        )


def show_summary():
    expenses = load_expenses()
    total = sum(float(e["amount"]) for e in expenses)
    categories = {}

    for expense in expenses:
        category = expense["category"]
        categories[category] = (
            categories.get(category, 0) + float(expense["amount"])
        )

    print(f"\nTotal spending: Rs. {total:.2f}")
    print(f"Number of expenses: {len(expenses)}")
    print("\nSpending by category:")
    for category, amount in sorted(categories.items()):
        print(f"{category}: Rs. {amount:.2f}")


def main():
    while True:
        print("\n=== Daily Expense Tracker ===")
        print("1. Add expense")
        print("2. View expenses")
        print("3. View summary")
        print("4. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            category = input("Category (Food/Travel/Bills/Other): ").strip()
            if not category:
                print("Category cannot be empty.")
                continue
            try:
                amount = float(input("Amount in Rs.: "))
                note = input("Description: ").strip()
                add_expense(category, amount, note)
                print("Expense saved successfully!")
            except ValueError as error:
                print("Invalid amount:", error)

        elif choice == "2":
            show_expenses()

        elif choice == "3":
            show_summary()

        elif choice == "4":
            print("Thank you for using Expense Tracker!")
            break

        else:
            print("Invalid choice. Please select 1-4.")


if __name__ == "__main__":
    main()
