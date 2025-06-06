import typer
from sqlalchemy.orm import Session
from datetime import date
from health_cli.db.database import get_db
from health_cli.models.food_entry import (
    add_food_entry,
    list_food_entries,
    update_food_entry,
    delete_food_entry,
)

entry_app = typer.Typer()

@entry_app.command("add")
def add_entry(
    user_name: str,
    food: str,
    calories: int,
    entry_date: date = typer.Option(default_factory=date.today)
):
    """Add a new food entry."""
    db: Session = next(get_db())
    try:
        entry = add_food_entry(db, user_name, food, calories, entry_date)
        typer.echo(f"✅ Added entry: {entry.food} ({entry.calories} kcal) on {entry.date} for user {user_name}.")
    except ValueError as e:
        typer.echo(f"❌ Error: {e}")

@entry_app.command("list")
def list_entries(
    user_name: str = typer.Option(None),
    entry_date: date = typer.Option(None)
):
    """List food entries, optionally filtered by user or date."""
    db: Session = next(get_db())
    try:
        entries = list_food_entries(db, user_name=user_name, date=entry_date)
        if not entries:
            typer.echo("ℹ️ No entries found.")
            return
        for entry in entries:
            typer.echo(f"📌 ID: {entry.id} | {entry.food} | {entry.calories} kcal | {entry.date} | User ID: {entry.user_id}")
    except ValueError as e:
        typer.echo(f"❌ Error: {e}")

@entry_app.command("update")
def update_entry(
    entry_id: int,
    food: str = typer.Option(None),
    calories: int = typer.Option(None),
    entry_date: date = typer.Option(None)
):
    """Update an existing food entry."""
    db: Session = next(get_db())
    try:
        entry = update_food_entry(db, entry_id, food=food, calories=calories, date=entry_date)
        typer.echo(f"✅ Updated entry ID {entry.id}.")
    except ValueError as e:
        typer.echo(f"❌ Error: {e}")

@entry_app.command("delete")
def delete_entry(entry_id: int):
    """Delete a food entry by ID."""
    db: Session = next(get_db())
    try:
        delete_food_entry(db, entry_id)
        typer.echo(f"🗑️ Deleted entry ID {entry_id}.")
    except ValueError as e:
        typer.echo(f"❌ Error: {e}")
