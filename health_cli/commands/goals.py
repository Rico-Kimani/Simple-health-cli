import typer
from health_cli.db.database import get_session
from health_cli.models.goals_entry import set_user_goals, get_user_goals

goal_app = typer.Typer()

@goal_app.command("set")
def set_goal(user: str, daily: int, weekly: int):
    """Set daily and weekly calorie goals for a user."""
    session = get_session()
    try:
        set_user_goals(session, user, daily, weekly)
        typer.echo(f"Goals set for {user}: Daily = {daily}, Weekly = {weekly}")
    except ValueError as e:
        typer.echo(f"Error: {e}")
    finally:
        session.close()

@goal_app.command("list")
def list_goals(user: str):
    """List a user's calorie goals."""
    session = get_session()
    try:
        goal = get_user_goals(session, user)
        if goal:
            typer.echo(f"{user}'s goals - Daily: {goal.daily_goal} kcal, Weekly: {goal.weekly_goal} kcal")
        else:
            typer.echo(f"No goals found for {user}")
    finally:
        session.close()
