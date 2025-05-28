import typer
from datetime import date
from myapp.db import SessionLocal
from myapp.models import User, FoodEntry, Goal

app = typer.Typer()
user_app = typer.Typer()
entry_app = typer.Typer()
goal_app = typer.Typer()

app.add_typer(user_app, name="user")
app.add_typer(entry_app, name="entry")
app.add_typer(goal_app, name="goal")

# --- USER COMMANDS ---

@user_app.command("create")
def create_user(name: str):
    """Create a new user."""
    session = SessionLocal()
    user = User(name=name)
    session.add(user)
    session.commit()
    typer.echo(f"✅ Created user: {user.name} (id: {user.id})")
    session.close()

@user_app.command("list")
def list_users():
    """List all users."""
    session = SessionLocal()
    users = session.query(User).all()
    for user in users:
        typer.echo(f"{user.id}: {user.name}")
    session.close()

# --- ENTRY COMMANDS ---

@entry_app.command("add")
def add_entry(
    user: str,
    food: str,
    calories: int,
    entry_date: str = typer.Option(str(date.today()), "--date", help="Date in YYYY-MM-DD")

):
    """Add a food entry for a user."""
    session = SessionLocal()
    user_obj = session.query(User).filter_by(name=user).first()
    if not user_obj:
        typer.echo(f"User '{user}' not found.")
        return

    try:
        entry_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        typer.echo("❌ Date must be in YYYY-MM-DD format.")
        return

    new_entry = FoodEntry(
        food=food,
        calories=calories,
        date=entry_date,
        user_id=user_obj.id
    )
    session.add(new_entry)
    session.commit()
    typer.echo(f"✅ Added {food} with {calories} calories for {user} on {date}.")
  

@entry_app.command("list")
def list_entries(
    user: str = typer.Option(None, "--user", "-u", help="User's name"),
    entry_date: str = typer.Option(None, "--date", "-d", help="Date in YYYY-MM-DD")
):
    """List food entries. Can filter by user and/or date."""
    session = SessionLocal()
    query = session.query(FoodEntry)

    if user:
        user_obj = session.query(User).filter(User.name == user).first()
        if not user_obj:
            typer.echo(f"❌ User '{user}' not found.")
            return
        query = query.filter(FoodEntry.user_id == user_obj.id)

    if entry_date:
        query = query.filter(FoodEntry.date == entry_date)

    entries = query.all()
    if not entries:
        typer.echo("ℹ️ No entries found.")
    else:
        for e in entries:
            typer.echo(f"{e.id}: {e.food} - {e.calories} cal on {e.date} (user_id: {e.user_id})")
    session.close()

@entry_app.command("update")
def update_entry(
    id: int,
    food: str = typer.Option(None, "--food", "-f"),
    calories: int = typer.Option(None, "--calories", "-c"),
    entry_date: str = typer.Option(None, "--date", "-d")
):
    """Update a food entry by ID."""
    session = SessionLocal()
    entry = session.query(FoodEntry).get(id)
    if not entry:
        typer.echo(f"❌ Entry ID {id} not found.")
        return

    if food: entry.food = food
    if calories: entry.calories = calories
    if entry_date: entry.date = entry_date

    session.commit()
    typer.echo(f"✅ Updated entry {id}")
    session.close()

@entry_app.command("delete")
def delete_entry(id: int):
    """Delete a food entry by ID."""
    session = SessionLocal()
    entry = session.query(FoodEntry).get(id)
    if not entry:
        typer.echo(f"❌ Entry ID {id} not found.")
        return
    session.delete(entry)
    session.commit()
    typer.echo(f"🗑️ Deleted entry {id}")
    session.close()
    

@goal_app.command("set")
def set_goal(user: str, target_calories: int, start_date: str, end_date: str):
    """Set a calorie goal for a user."""
    session = SessionLocal()
    user_obj = session.query(User).filter_by(name=user).first()

    if not user_obj:
        typer.echo(f"❌ User '{user}' not found.")
        return

    from datetime import datetime
    goal = Goal(
        user_id=user_obj.id,
        target_calories=target_calories,
        start_date=datetime.strptime(start_date, "%Y-%m-%d").date(),
        end_date=datetime.strptime(end_date, "%Y-%m-%d").date()
    )
    session.add(goal)
    session.commit()
    typer.echo(f"🎯 Set goal for {user}: {target_calories} cal/day from {start_date} to {end_date}")
    session.close()

# cli.py

from myapp.db import SessionLocal
from myapp.models import User, Goal
import typer
from datetime import datetime

goal_app = typer.Typer()
app.add_typer(goal_app, name="goal")

@goal_app.command("create")
def create_goal(
    user: str,
    target_calories: int,
    start_date: str,
    end_date: str
):
    """Create a new calorie goal for a user."""
    session = SessionLocal()
    user_obj = session.query(User).filter(User.name == user).first()
    if not user_obj:
        typer.echo(f"❌ User '{user}' not found.")
        return
    goal = Goal(
        user_id=user_obj.id,
        target_calories=target_calories,
        start_date=datetime.strptime(start_date, "%Y-%m-%d").date(),
        end_date=datetime.strptime(end_date, "%Y-%m-%d").date()
    )
    session.add(goal)
    session.commit()
    typer.echo(f"✅ Goal created for {user} from {start_date} to {end_date}")
    session.close()

@goal_app.command("list")
def list_goals(user: str = None):
    """List all goals, optionally filtered by user."""
    session = SessionLocal()
    query = session.query(Goal)

    if user:
        user_obj = session.query(User).filter(User.name == user).first()
        if not user_obj:
            typer.echo(f"❌ User '{user}' not found.")
            return
        query = query.filter(Goal.user_id == user_obj.id)

    goals = query.all()
    for g in goals:
        typer.echo(f"{g.id}: {g.target_calories} cal from {g.start_date} to {g.end_date} (user_id: {g.user_id})")
    session.close()

