import json
import click

# File to store the to-do list
TODO_FILE = "todo_list.json"


# Load tasks from JSON file
def load_tasks():
    try:
        with open(TODO_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


# Save tasks to JSON file
def save_tasks(todo_list):
    with open(TODO_FILE, 'w') as file:
        json.dump(todo_list, file, indent=4)


# Command to display the to-do list
@click.command()
def view():
    """View the current to-do list."""
    todo_list = load_tasks()
    if not todo_list:
        click.echo("Your to-do list is empty!")
    else:
        click.echo("\nYour to-do list:")
        for idx, task in enumerate(todo_list, 1):
            status = "✓" if task['completed'] else "✗"
            click.echo(f"{idx}. {task['task']} [{status}]")


# Command to add a new task
@click.command()
@click.argument('tasks', nargs=-1) # accept multiple tasks
def add(tasks):
    """Add one or more tasks to the to-do list."""
    todo_list = load_tasks()
    for task in tasks:
        todo_list.append({'task': task, 'completed': False})
        click.echo(f"Task '{task}' added to the list.")
    save_tasks(todo_list)


# Command to remove a task
@click.command()
@click.argument('task_num', type=int)
def remove(task_num):
    """Remove a task from the to-do list by number."""
    todo_list = load_tasks()
    if 0 < task_num <= len(todo_list):
        removed_task = todo_list.pop(task_num - 1)
        save_tasks(todo_list)
        click.echo(f"Task '{removed_task['task']}' removed.")
    else:
        click.echo("Invalid task number.")


# Command to mark a task as completed
@click.command()
@click.argument('task_num', type=int)
def complete(task_num):
    """Mark a task as completed by number."""
    todo_list = load_tasks()
    if 0 < task_num <= len(todo_list):
        todo_list[task_num - 1]['completed'] = True
        save_tasks(todo_list)
        click.echo(f"Task '{todo_list[task_num - 1]['task']}' marked as completed.")
    else:
        click.echo("Invalid task number.")


# Define the main group of commands
@click.group()
def cli():
    """Simple To-Do List CLI."""
    pass


# Add commands to the CLI group
cli.add_command(view)
cli.add_command(add)
cli.add_command(remove)
cli.add_command(complete)


if __name__ == "__main__":
    cli()

