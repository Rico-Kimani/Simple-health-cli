# commands/user_commands.py

from health_cli.db.config import SessionLocal
from health_cli.models.users_entry import User
import typer

def create_user(name: str, email: str, age: int):
    db = SessionLocal()
    user = User(name=name, email=email, age=age)
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    typer.echo(f"✅ User created: {user.name} (ID: {user.id})")

def list_users():
    db = SessionLocal()
    users = db.query(User).all()
    if not users:
        typer.echo("No users found.")
    for user in users:
        typer.echo(f"[{user.id}] {user.name} - {user.email} - Age {user.age}")
    db.close()

def get_user(user_id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        typer.echo(f"User found:\nName: {user.name}\nEmail: {user.email}\nAge: {user.age}")
    else:
        typer.echo("❌ User not found.")
    db.close()

def update_user(user_id: int, name: str = None, email: str = None, age: int = None):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        typer.echo("❌ User not found.")
        db.close()
        return

    if name:
        user.name = name
    if email:
        user.email = email
    if age:
        user.age = age

    db.commit()
    typer.echo(f"✅ Updated user {user.name} (ID: {user.id})")
    db.close()

def delete_user(user_id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        typer.echo("❌ User not found.")
    else:
        db.delete(user)
        db.commit()
        typer.echo(f"🗑 Deleted user {user.name} (ID: {user.id})")
    db.close()
