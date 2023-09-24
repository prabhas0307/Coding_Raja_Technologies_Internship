import json
from datetime import datetime

# Title: Personal Budget Tracker

# Initialize an empty list to store transactions
transactions = []

# Load transactions from a file if it exists
try:
    with open('transactions.json', 'r') as file:
        transactions = json.load(file)
except FileNotFoundError:
    pass


# Function to save transactions to a file
def save_transactions():
    with open('transactions.json', 'w') as file:
        json.dump(transactions, file)


# Function to record a new transaction (income or expense)
def record_transaction():
    transaction = {}
    transaction['type'] = input("Enter transaction type (income/expense): ").lower()
    if transaction['type'] not in ('income', 'expense'):
        print("Invalid transaction type. Use 'income' or 'expense'.")
        return

    transaction['category'] = input("Enter transaction category: ")
    transaction['amount'] = float(input("Enter transaction amount: "))
    transaction['date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    transactions.append(transaction)
    save_transactions()
    print("Transaction recorded successfully!")


# Function to calculate the remaining budget
def calculate_budget():
    income = sum(transaction['amount'] for transaction in transactions if transaction['type'] == 'income')
    expenses = sum(transaction['amount'] for transaction in transactions if transaction['type'] == 'expense')
    budget = income - expenses
    return budget


# Function to analyze expenses by category
def analyze_expenses():
    expense_categories = {}
    for transaction in transactions:
        if transaction['type'] == 'expense':
            category = transaction['category']
            amount = transaction['amount']
            if category in expense_categories:
                expense_categories[category] += amount
            else:
                expense_categories[category] = amount

    print("\nExpense Analysis:")
    for category, amount in expense_categories.items():
        print(f"{category}: ${amount:.2f}")


# Main loop
while True:
    print("\nOptions:")
    print("1. Record Transaction")
    print("2. Calculate Budget")
    print("3. Expense Analysis")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        record_transaction()
    elif choice == '2':
        budget = calculate_budget()
        print(f"Remaining Budget: ${budget:.2f}")
    elif choice == '3':
        analyze_expenses()
    elif choice == '4':
        break
    else:
        print("Invalid choice. Please try again.")
