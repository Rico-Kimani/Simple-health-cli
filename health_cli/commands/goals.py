# health_cli/commands/goals.py
import typer
from health_cli.db.database import get_session
from health_cli.models.goals_entry import Goal, set_user_goals, get_user_goals, get_calorie_progress
from health_cli.utils.validation import user_exists  # ✅

goal_app = typer.Typer()

@goal_app.command("set")
def set_goal(user: str, daily: int, weekly: int):
    """Set daily and weekly calorie goals for a user."""
    session = get_session()
    try:
        if not user_exists(session, user):
            typer.echo(f"❌ User '{user}' does not exist.")
            raise typer.Exit()
        set_user_goals(session, user, daily, weekly)
        typer.echo(f"✅ Goals set for {user}: Daily = {daily}, Weekly = {weekly}")
    except ValueError as e:
        typer.echo(f"❌ Error: {e}")
    finally:
        session.close()

@goal_app.command("list")
def list_goals(user: str):
    """List a user's calorie goals."""
    session = get_session()
    try:
        if not user_exists(session, user):
            typer.echo(f"❌ User '{user}' does not exist.")
            raise typer.Exit()
        goal = get_user_goals(session, user)
        if goal:
            typer.echo(f"📊 {user}'s Goals — Daily: {goal.daily_goal} kcal, Weekly: {goal.weekly_goal} kcal")
        else:
            typer.echo(f"⚠️ No goals found for {user}")
    finally:
        session.close()

@goal_app.command("add")
def add_goal(user_id: int, description: str):
    """Add a new goal for a user."""
    db = get_session()
    goal = Goal(user_id=user_id, description=description)
    db.add(goal)
    db.commit()
    db.refresh(goal)
    typer.echo(f"✅ Goal added for User {user_id}: {goal.description}")
    db.close()

@goal_app.command("view")
def view_goal(user_name: str):
    """View calorie goals."""
    session = get_session()
    try:
        if not user_exists(session, user_name):
            typer.echo(f"❌ User '{user_name}' does not exist.")
            raise typer.Exit()
        goal = get_user_goals(session, user_name)
        if not goal:
            typer.echo("No goals set.")
        else:
            typer.echo(f"{user_name}'s Goals → Daily: {goal.daily_goal} | Weekly: {goal.weekly_goal}")
    finally:
        session.close()

@goal_app.command("update")
def update_goal(goal_id: int, description: str):
    """Update a goal's description."""
    db = get_session()
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if not goal:
        typer.echo("❌ Goal not found.")
    else:
        goal.description = description
        db.commit()
        typer.echo(f"✅ Goal updated: {goal.description}")
    db.close()

@goal_app.command("delete")
def delete_goal(goal_id: int):
    """Delete a goal by ID."""
    db = get_session()
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if not goal:
        typer.echo("❌ Goal not found.")
    else:
        db.delete(goal)
        db.commit()
        typer.echo("🗑 Goal deleted.")
    db.close()

@goal_app.command("progress")
def calorie_progress(user_name: str):
    """View today's and this week's calorie intake compared to goals."""
    session = get_session()
    try:
        if not user_exists(session, user_name):
            typer.echo(f"❌ User '{user_name}' does not exist.")
            raise typer.Exit()
        data = get_calorie_progress(session, user_name)
        typer.echo(f"\n📊 {user_name}'s Calorie Progress")
        typer.echo(f"Today: {data['daily_total']} / {data['daily_goal']} kcal")
        typer.echo(f"This Week: {data['weekly_total']} / {data['weekly_goal']} kcal\n")

        if data['daily_total'] > data['daily_goal']:
            typer.echo("⚠️ You've exceeded your **daily** goal!")
        if data['weekly_total'] > data['weekly_goal']:
            typer.echo("⚠️ You've exceeded your **weekly** goal!")
    except ValueError as e:
        typer.echo(f"Error: {e}")
    finally:
        session.close()
