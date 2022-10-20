import os
import typer
import pandas as pd
from datetime import datetime
from pathlib import Path

PATH = str(Path(__file__).parent)
PATH_TO_DATA = f"{PATH}/data/"


app = typer.Typer(add_completion=False)

### CLI METHODS ###


@app.command("create")
def create(name: str = typer.Option("Unnamed", "-ln", "--listname")):

    """Create a new todo list"""

    if check_list_exists(name):
        print("There is already a todo list with this name.")
        return

    create_list(name)
    print(f"Todo list {name} successfully created!")


@app.command("list")
def list_lists():
    
    """Lists all existing todo lists"""

    existing_lists = get_existing_lists()
    for ls in existing_lists:
        print(ls)


@app.command("show")
def show_list(list_name: str = typer.Option(..., "-ln", "--listname")):
    """Shows Task in one list"""
    if not check_list_exists(list_name):
        print("The list does not exist. Use create list first.")
        return
    df = load_list(list_name)
    print(df.to_markdown())


@app.command("add")
def add_task(
    list_name: str = typer.Option(..., "-ln", "--listname"),
    task_name: str = typer.Option(..., "-tn", "--taskame"),
    summary: str = typer.Option(None, "-d", "--description"),
    owner: str = typer.Option(..., "-o", "--owner"),
):
    """Add a task to a given todo list"""

    if not check_list_exists(list_name):
        print("The list does not exist. Use create list first.")
        return

    new_row = {
        "created": datetime.now().strftime("%Y-%m-%d %H-%M-%S"),
        "task": task_name,
        "summary": summary if summary else None,
        "status": "todo",
        "owner": owner,
    }

    add_to_list(list_name, new_row)
    print("Task successfully added")


@app.command("update")
def update_task(
    list_name: str = typer.Option(..., "-ln", "--listname"),
    task_id: int = typer.Option(..., "-i", "--taskid"),
    field: str = typer.Option(..., "-f", "--field"),
    change: str = typer.Option(..., "-c", "--change"),
):

    """Update a task in a given todo list"""
    if not check_list_exists(list_name):
        print("The list does not exist. Use create list first.")
        return
    update_task_in_list(list_name, task_id, field, change)
    print("Task successfully updated")


### LIST METHODS TO BE REFACTORED ###


def update_task_in_list(list_name, task_id, field, change):
    df = load_list(list_name)
    df.loc[task_id, field] = change
    store_list(df, list_name)


def create_list(name):
    df = pd.DataFrame(columns=["created", "task", "summary", "status", "owner"])
    store_list(df, name)


def get_existing_lists():
    return os.listdir(PATH_TO_DATA)


def check_list_exists(name):
    return get_list_filename(name) in get_existing_lists()


def get_list_filename(name):
    return f"{name}.csv"


def load_list(name):
    return pd.read_csv(get_list_path(name))


def store_list(df, name):
    df.to_csv(get_list_path(name), index=False)


def get_list_path(name):
    return f"{PATH_TO_DATA}{get_list_filename(name)}"


def add_to_list(list_name, new_row):
    df = load_list(list_name)
    df.loc[len(df.index)] = new_row
    store_list(df, list_name)


if __name__ == "__main__":
    app()
