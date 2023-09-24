import sqlite3
from datetime import datetime

# Connect to SQLite database (or create if not exists)
conn = sqlite3.connect('tasks.db')
cursor = conn.cursor()

# Create tasks table if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    due_date DATE,
                    completed BOOLEAN
                )''')
conn.commit()

# Function to add a new task
def add_task():
    title = input("Enter task title: ")
    priority = input("Enter task priority (high, medium, low): ")
    due_date_str = input("Enter due date (YYYY-MM-DD, or leave blank if none): ")
    due_date = None
    if due_date_str:
        try:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return

    cursor.execute('''INSERT INTO tasks (title, priority, due_date, completed)
                      VALUES (?, ?, ?, ?)''', (title, priority, due_date, False))
    conn.commit()
    print("Task added successfully!")

# Function to remove a task
def remove_task():
    display_tasks()
    task_id = input("Enter the ID of the task to remove: ")
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    print(f"Task with ID {task_id} removed.")

# Function to mark a task as completed
def mark_task_completed():
    display_tasks()
    task_id = input("Enter the ID of the task to mark as completed: ")
    cursor.execute('UPDATE tasks SET completed = 1 WHERE id = ?', (task_id,))
    conn.commit()
    print(f"Task with ID {task_id} marked as completed.")

# Function to display tasks
def display_tasks():
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    print("\nTasks:")
    for task in tasks:
        task_id, title, priority, due_date, completed = task
        status = "Completed" if completed else "Pending"
        due_date_str = due_date.strftime("%Y-%m-%d") if due_date else "None"
        print(f"ID: {task_id} | Title: {title} | Priority: {priority} | Due Date: {due_date_str} | Status: {status}")

while True:
    print("\nOptions:")
    print("1. Add Task")
    print("2. Remove Task")
    print("3. Mark Task as Completed")
    print("4. List Tasks")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        add_task()
    elif choice == '2':
        remove_task()
    elif choice == '3':
        mark_task_completed()
    elif choice == '4':
        display_tasks()
    elif choice == '5':
        conn.close()
        break
    else:
        print("Invalid choice. Please try again.")
