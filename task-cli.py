#!/usr/bin/env python3
import os
import json
import sys
from datetime import datetime

DB_FILE = "tasks.json"

def load_tasks() -> list:
    """Helper to safely read and parse tasks from the database file."""
    if not os.path.exists(DB_FILE) or os.path.getsize(DB_FILE) == 0:
        return []
    try:
        with open(DB_FILE, "r") as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        print(f"Error reading JSON file: {e}")
        return []

def save_tasks(tasks: list) -> bool:
    """Helper to safely write tasks back to the database file."""
    try:
        with open(DB_FILE, "w") as file:
            json.dump(tasks, file, indent=4)
        return True
    except Exception as e:
        print(f"Error writing to JSON file: {e}")
        return False

def generate_task_id() -> int:
    """Generate a unique task ID by finding the current maximum ID."""
    tasks = load_tasks()
    return max([t["id"] for t in tasks], default=0) + 1

def add_task(task_name: str) -> None:
    """Add a new task to the JSON file with a unique ID."""
    tasks = load_tasks()
    new_task_id = generate_task_id()
    
    task = {
        "id": new_task_id,
        "description": task_name,
        "status": "to do",
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat()
    }
    
    tasks.append(task)
    if save_tasks(tasks):
        print(f"Task '{task_name}' added successfully with ID {new_task_id}.")

def update_task(task_id: int, new_description: str) -> None:
    """Update the description of an existing task."""
    if task_id <= 0:
        print("Invalid task ID. Task ID must be a positive integer.")
        return
        
    tasks = load_tasks()
    task_found = False
    
    for task in tasks:
        if task["id"] == task_id:
            task["description"] = new_description
            task["updatedAt"] = datetime.now().isoformat()
            task_found = True
            break
            
    if not task_found:
        print(f"Error: Task with ID {task_id} not found.")
        return

    if save_tasks(tasks):
        print(f"Task with ID {task_id} updated successfully.")

def delete_task(task_id: int) -> None:
    """Delete an existing task from the JSON file."""
    if task_id <= 0:
        print("Invalid task ID. Task ID must be a positive integer.")
        return
        
    tasks = load_tasks()
    # Filter out the matching ID completely
    updated_tasks = [t for t in tasks if t["id"] != task_id]
    
    if len(tasks) == len(updated_tasks):
        print(f"Error: Task with ID {task_id} not found.")
        return
        
    if save_tasks(updated_tasks):
        print(f"Task with ID {task_id} deleted successfully.")

def change_status(status: str, task_id: int) -> None:
    """Change the status of an existing task."""
    if task_id <= 0:
        print("Invalid task ID. Task ID must be a positive integer.")
        return
        
    valid_statuses = ["to do", "in progress", "done"]
    if status not in valid_statuses:
        print(f"Invalid status. Status must be one of {valid_statuses}.")
        return
        
    tasks = load_tasks()
    task_found = False
    
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status
            task["updatedAt"] = datetime.now().isoformat()
            task_found = True
            break
            
    if not task_found:
        print(f"Error: Task with ID {task_id} not found.")
        return
        
    if save_tasks(tasks):
        print(f"Status of task with ID {task_id} updated successfully to '{status}'.")

def list_all_tasks() -> None:
    """List all the tasks in the JSON file with their details."""
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
        
    for task in tasks:
        print(f"ID: {task['id']} | [{task['status'].upper()}]")
        print(f"Description: {task['description']}")
        print(f"Created At: {task['createdAt']} | Updated At: {task['updatedAt']}")
        print("-" * 40)

def list_specific_status(status: str) -> None:
    """List all the tasks matching a specified status."""
    valid_statuses = ["to do", "in progress", "done"]
    if status not in valid_statuses:
        print(f"Invalid status. Status must be one of {valid_statuses}.")
        return
        
    tasks = load_tasks()
    filtered_tasks = [t for t in tasks if t["status"] == status]
    
    if not filtered_tasks:
        print(f"No tasks found with status '{status}'.")
        return
        
    for task in filtered_tasks:
        print(f"ID: {task['id']}")
        print(f"Description: {task['description']}")
        print(f"Created At: {task['createdAt']} | Updated At: {task['updatedAt']}")
        print("-" * 40)
        
        
operation = sys.argv[1] if len(sys.argv) > 1 else None
if operation == "add":
    if len(sys.argv) < 3:
        print("Error: Task description is required for 'add' operation.")
    else:
        add_task(sys.argv[2])
elif operation == "update":
    if len(sys.argv) < 4:
        print("Error: Task ID and new description are required for 'update' operation.")
    else:
        try:
            task_id = int(sys.argv[2])
            new_description = sys.argv[3]
            update_task(task_id, new_description)
        except ValueError:
            print("Error: Task ID must be a valid integer.")
elif operation == "delete":
    if len(sys.argv) < 3:
        print("Error: Task ID is required for 'delete' operation.")
    else:
        try:
            task_id = int(sys.argv[2])
            delete_task(task_id)
        except ValueError:
            print("Error: Task ID must be a valid integer.")
elif "mark-" in operation:
    if len(sys.argv) < 3:
        print("Error: Status and Task ID are required for 'status' operation.")
    else:
        try:
            status = sys.argv[1]
            status = status.replace("mark-", "").replace("-", " ")
            task_id = int(sys.argv[2])
            change_status(status, task_id)
        except ValueError:
            print("Error: Task ID must be a valid integer.")
elif operation == "list":
    if len(sys.argv) == 2:
        list_all_tasks()
    elif len(sys.argv) == 3:
        status = sys.argv[2]
        status = status.replace("mark-", "").replace("-", " ")
        list_specific_status(status)
    else:
        print("Error: Too many arguments for 'list' operation.")
else:
    print("Invalid operation. Available operations: add, update, delete, mark-<status>, list [<status>].")