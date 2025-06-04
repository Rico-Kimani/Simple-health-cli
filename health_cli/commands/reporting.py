import typer
from datetime import datetime
from health_cli.db.database import get_session
from health_cli.models import food_entry, goals_entry

report_app = typer.Typer()

@report_app.command("daily")
def daily_report(user: str, date: str):
    """
    View a summary report for a specific date for a user.
    """
    try:
        parsed_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        typer.echo("❌ Invalid date format. Use YYYY-MM-DD.")
        raise typer.Exit()

    session = get_session()
    try:
        entries = food_entry.list_food_entries(session, user, parsed_date)
        total_calories = sum(entry.calories for entry in entries)
        goal = goals_entry.get_user_goals(session, user)

        typer.echo(f"📅 {user}'s Report for {parsed_date}")
        typer.echo(f"🍽️  Total Calories: {total_calories}")

        if goal:
            status = "✅ On track!" if total_calories <= goal.daily_goal else "⚠️ Over goal!"
            typer.echo(f"🎯 Daily Goal: {goal.daily_goal} → {status}")
        else:
            typer.echo("⚠️ No goals set for this user.")
    finally:
        session.close()
