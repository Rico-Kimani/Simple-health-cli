import typer
from health_cli.models import session
from health_cli.models.users_entry import User
from health_cli.commands import (
    user_commands,
    entry,
    goals,
    reporting,
    meal_planning
)

app = typer.Typer()

# Sub-apps (modular command groups)
entry_app = entry.entry_app
goal_app = goals.goal_app
report_app = reporting.report_app
meal_app = meal_planning.meal_app

# Mount subcommands to main app
app.add_typer(entry_app, name="entry")
app.add_typer(goal_app, name="goal")
app.add_typer(report_app, name="report")
app.add_typer(meal_app, name="plan-meal")

# User Commands
@app.command("create")
def create_user(name: str, email: str, age: int):
    user_commands.create_user(name, email, age)

@app.command("list")
def list_users():
    user_commands.list_users()

@app.command("get")
def get_user(user_id: int):
    #user_commands.get_user(user_id)#
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        typer.echo(f"User {user.id}: {user.name}, Age: {user.age}")
    else:
        typer.echo(f"No user found with ID {user_id}")

@app.command("delete")
def delete_user(user_id: int):
    user_commands.delete_user(user_id)

if __name__ == "__main__":
    app()
