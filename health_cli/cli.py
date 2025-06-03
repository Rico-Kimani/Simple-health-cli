import typer
from health_cli.commands import user_commands

app = typer.Typer()
user_app = typer.Typer()

# Mount `user` command group
app.add_typer(user_app, name="user")

# Define commands under `user`
@user_app.command("create")
def create_user(name: str, email: str, age: int):
    user_commands.create_user(name, email, age)

@user_app.command("list")
def list_users():
    user_commands.list_users()

@user_app.command("get")
def get_user(user_id: int):
    user_commands.get_user(user_id)

@user_app.command("delete")
def delete_user(user_id: int):
    user_commands.delete_user(user_id)

if __name__ == "__main__":
    app()
