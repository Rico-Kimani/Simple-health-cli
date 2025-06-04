import typer
from datetime import datetime
from health_cli.db.database import get_session
from health_cli.models import food_entry

entry_app = typer.Typer()

@entry_app.command("add")
def add_entry(user: str, food: str, calories: int, date: str):
    """
    Add a new food entry for a user.
    """
    try:
        parsed_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        typer.echo("❌ Invalid date format. Use YYYY-MM-DD.")
        raise typer.Exit()

    session = get_session()
    try:
        food_entry.add_food_entry(session, user, food, calories, parsed_date)
        typer.echo(f"✅ Added '{food}' ({calories} cal) for {user} on {date}.")
    except Exception as e:
        typer.echo(f"❌ Failed to add entry: {e}")
    finally:
        session.close()

@entry_app.command("list")
def list_entries(user: str = None, date: str = None):
    """
    List food entries. You can filter by user or date.
    """
    parsed_date = None
    if date:
        try:
            parsed_date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            typer.echo("❌ Invalid date format. Use YYYY-MM-DD.")
            raise typer.Exit()

    session = get_session()
    try:
        entries = food_entry.list_food_entries(session, user, parsed_date)
        if not entries:
            typer.echo("No entries found.")
        for entry in entries:
            typer.echo(f"[{entry.id}] {entry.user.name} - {entry.food_name} - {entry.calories} cal on {entry.date}")
    finally:
        session.close()

@entry_app.command("update")
def update_entry(id: int, food: str = None, calories: int = None, date: str = None):
    """
    Update a food entry by ID. You can update food name, calories, or date.
    """
    parsed_date = None
    if date:
        try:
            parsed_date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            typer.echo("❌ Invalid date format. Use YYYY-MM-DD.")
            raise typer.Exit()

    session = get_session()
    try:
        success = food_entry.update_food_entry(session, id, food, calories, parsed_date)
        if success:
            typer.echo("✅ Entry updated successfully.")
        else:
            typer.echo("❌ Entry not found.")
    finally:
        session.close()

@entry_app.command("delete")
def delete_entry(id: int):
    """
    Delete a food entry by ID.
    """
    session = get_session()
    try:
        success = food_entry.delete_food_entry(session, id)
        if success:
            typer.echo("🗑️ Entry deleted.")
        else:
            typer.echo("❌ Entry not found.")
    finally:
        session.close()
