
import csv
import os
from datetime import date, datetime

FILE = "expenses.csv"
FIELDS = ["date", "category", "amount", "note"]


def load_expenses():
    """Load expense records from CSV."""
    if not os.path.exists(FILE) or os.path.getsize(FILE) == 0:
        return []

    with open(FILE, "r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def add_expense(category, amount, note):
    """Validate and save an expense."""
    if not category.strip():
        raise ValueError("Category cannot be empty.")

    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")

    with open(FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)

        if file.tell() == 0:
            writer.writeheader()

        writer.writerow({
            "date": date.today().isoformat(),
            "category": category.strip().title(),
            "amount": f"{amount:.2f}",
            "note": note.strip()
        })


def show_expenses(expenses=None):
    """Display all expenses or a filtered list."""
    if expenses is None:
        expenses = load_expenses()

    if not expenses:
        print("\nNo expenses found.")
        return

    print("\n--- Expense History ---")
    for item in expenses:
        print(
            f"{item['date']} | {item['category']} | "
            f"Rs. {float(item['amount']):.2f} | {item['note']}"
        )


def show_summary():
    """Display spending totals and category breakdown."""
    expenses = load_expenses()

    if not expenses:
        print("\nNo expenses available for summary.")
        return

    total = sum(float(item["amount"]) for item in expenses)
    categories = {}

    for item in expenses:
        category = item["category"]
        categories[category] = (
            categories.get(category, 0) + float(item["amount"])
        )

    highest = max(expenses, key=lambda item: float(item["amount"]))

    print("\n--- Spending Summary ---")
    print(f"Total spending: Rs. {total:.2f}")
    print(f"Number of expenses: {len(expenses)}")
    print(f"Highest expense: Rs. {float(highest['amount']):.2f}")
    print(f"Category: {highest['category']}")
    print("\nSpending by category:")

    for category, amount in sorted(categories.items()):
        print(f"{category}: Rs. {amount:.2f}")


def filter_by_category():
    """Filter expense history by category."""
    category = input("Enter category to search: ").strip().casefold()

    if not category:
        print("Category cannot be empty.")
        return

    expenses = [
        item for item in load_expenses()
        if item["category"].casefold() == category
    ]

    show_expenses(expenses)


def monthly_summary():
    """Display total expenses for a selected month."""
    month = input("Enter month (YYYY-MM): ").strip()

    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        print("Invalid month. Use YYYY-MM, for example 2026-10.")
        return

    expenses = [
        item for item in load_expenses()
        if item["date"].startswith(month)
    ]

    total = sum(float(item["amount"]) for item in expenses)

    print(f"\n--- Summary for {month} ---")
    print(f"Number of expenses: {len(expenses)}")
    print(f"Total spending: Rs. {total:.2f}")

    if not expenses:
        print("No expenses found for this month.")


def main():
    while True:
        print("\n===== Daily Expense Tracker =====")
        print("1. Add expense")
        print("2. View all expenses")
        print("3. View spending summary")
        print("4. Filter by category")
        print("5. Monthly summary")
        print("6. Exit")

        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            category = input("Category (Food/Travel/Bills/Other): ").strip()
            note = input("Description: ").strip()

            try:
                amount = float(input("Amount in Rs.: "))
                add_expense(category, amount, note)
                print("Expense saved successfully!")
            except ValueError as error:
                print(f"Invalid input: {error}")

        elif choice == "2":
            show_expenses()

        elif choice == "3":
            show_summary()

        elif choice == "4":
            filter_by_category()

        elif choice == "5":
            monthly_summary()

        elif choice == "6":
            print("Thank you for using Daily Expense Tracker!")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()

