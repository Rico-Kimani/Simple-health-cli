import typer
from health_cli.commands import user_commands 
from commands.meal_planning import meal_app
from commands.goals import goal_app
from health_cli.commands import (
    user_commands,
    entry,
    goals,
    reporting,
    meal_planning
)

app = typer.Typer(help="Health Simplified CLI App")

# Sub-apps (modular command groups)
entry_app = entry.entry_app
goal_app = goals.goal_app
report_app = reporting.report_app
meal_app = meal_planning.meal_app

# Mount subcommands to main app
app.add_typer(entry_app, name="entry", help="Log daily health data like water, sleep, etc.")
app.add_typer(goal_app, name="goal", help="Set and manage your health goals")
app.add_typer(report_app, name="report", help="Generate reports and insights")
app.add_typer(meal_app, name="meal", help="Plan and track meals")


# User Commands
@app.command("create")
def create_user(name: str, email: str, age: int):
    """
    Create a new user.
    """
    user_commands.create_user(name, email, age)

@app.command("list")
def list_users():
    """
    List all registered users.
    """
    user_commands.list_users()

@app.command("get")
def get_user(user_id: int):
    """
    Retrieve a user's details by ID.
    """
    user_commands.get_user(user_id)

@app.command("delete")
def delete_user(user_id: int):
    """
    Delete a user by ID.
    """
    user_commands.delete_user(user_id)

@app.command("update")
def update_user(user_id: int, name: str = None, email: str = None, age: int = None):
    user_commands.update_user(user_id, name, email, age)



if __name__ == "__main__":
    app()
