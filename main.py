from datetime import datetime
import json
import os



counter = 0


def main():
    print("""Welcome to Task manager! Kindly choose the following options:
        * List
        * Add
        * Delete
        * Update
        * End""")

    choice = (input("Choice: ").lower())


    match choice:
        case "add":
            desc = input("Description: ")
            addTask(desc)
            return True
        case "delete":
            if task_list:
                try:
                    task_id = int(input("Task ID: "))
                except ValueError:
                    print("Please enter a valid numeric Task ID.")
                    return True
                deleteTask(task_id)
            else:
                print("There are no tasks to delete")

            return True
        case "list":
            status = input("| ALL | In progress | Done |: ").lower()
            if status in ["all", "in progress", "done"]:
                print(f"Listing {status} tasks...")
                listTasksByStatus(None if status == "all" else status)
            else:
                print("Invalid input")
            return True
        case "update":
            option = input("Toggle Status( + ) or Update task ( > ): ")
            try:
                taskId = int(input("Task ID: "))
            except ValueError:
                print("Please enter a valid numeric Task ID.")
                return True

            if option == "+":
                toggleStatus(taskId)
            elif option == ">":
                updateTask(taskId, input("New description: "))
            else:
                print("Invalid option")
            return True
        case "end":
            print("Closing task Manager...")
            return False
        case _:
            print("Invalid Option")
            return True


def addTask(description):
    global counter
    counter += 1
    if not description.strip():
        print("Description cannot be empty.")
        return

    task = create_task(counter, description)
    task_list.append(task)
    print(f"Task {counter} added.")
    save_tasks()


def deleteTask(task_id):
    for i, task in enumerate(task_list):
        if task['id'] == task_id:
            task_list.pop(i)
            print(f"Task {task_id} deleted.")
            save_tasks()
            return
    print(f"No task with ID {task_id} found.")


def updateTask(task_id, new_description):
    updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if not new_description.strip():
        print("Description cannot be empty.")
        return

    for i, task in enumerate(task_list):
        if task['id'] == task_id:
            task["description"] = new_description
            task["updatedAt"] = updated_at
            print("Updated Task")
            save_tasks()
            return
    print(f"No task with ID {task_id} found.")


def toggleStatus(task_id):
    for i, task in enumerate(task_list):
        if task['id'] == task_id:
            if task["status"] == "done":
                task["status"] = "in progress"
            elif task["status"] == "in progress":
                task["status"] = "done"
            print("Status Updated!")
            save_tasks()
            return
        else:
            print(f"Task {task_id} has an unknown status: {task['status']}")

    print(f"No task with ID {task_id} found.")


def listTasksByStatus(status=None):
    if status:
        tasks = [task for task in task_list if task["status"] == status]
    else:
        tasks = task_list

    print("\n".join(
        f"Task {task['id']}: {task['description']}, [{task['status']}]" for task in tasks
    ))


def create_task(task_id, description):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {
        "id": task_id,
        "description": description,
        "status": "in progress",
        "createdAt": timestamp,
        "updatedAt": timestamp
    }
def load_tasks():
    filename = "tasks.json"
    # If the file exists, load its content
    if os.path.exists(filename):
        with open(filename, "r") as file:
            try:
                tasks = json.load(file)
                return tasks
            except json.JSONDecodeError:
                # If the file is empty or has invalid JSON, return an empty list
                return []

    # If file doesn't exist, create it and return an empty list
    with open(filename, "w") as file:
        json.dump([], file)
    return []


def save_tasks():
    with open("tasks.json", "w") as file:
        json.dump(task_list, file, indent=4)

task_list = load_tasks()
# Sync counter to avoid ID collision
if task_list:
    counter = max(task["id"] for task in task_list)


while True:
    if not main():
        break
