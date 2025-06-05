# health_cli/models/food_entry.py

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from health_cli.db.database import Base
from health_cli.models.users_entry import User

class FoodEntry(Base):
    __tablename__ = "food_entries"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    food = Column(String, nullable=False)
    calories = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)

    user = relationship("User", back_populates="food_entries")


# food_entries = relationship("FoodEntry", back_populates="user")


# ---------------- CRUD FUNCTIONS ---------------- #

def add_food_entry(session, user_name, food, calories, date):
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        print(f"User '{user_name}' not found.")
        return

    entry = FoodEntry(user_id=user.id, food=food, calories=calories, date=date)
    session.add(entry)
    session.commit()
    print(f"Added food entry: {food} ({calories} kcal) on {date} for {user_name}.")


def list_food_entries(session, user_name=None, date=None):
    query = session.query(FoodEntry)

    if user_name:
        user = session.query(User).filter_by(name=user_name).first()
        if not user:
            print(f"User '{user_name}' not found.")
            return
        query = query.filter_by(user_id=user.id)

    if date:
        query = query.filter_by(date=date)

    entries = query.all()
    if not entries:
        print("No entries found.")
        return

    for entry in entries:
        print(f"ID: {entry.id} | {entry.food} | {entry.calories} kcal | {entry.date} | User ID: {entry.user_id}")


def update_food_entry(session, entry_id, food=None, calories=None, date=None):
    entry = session.query(FoodEntry).filter_by(id=entry_id).first()
    if not entry:
        print(f"Entry ID {entry_id} not found.")
        return

    if food:
        entry.food = food
    if calories:
        entry.calories = calories
    if date:
        entry.date = date

    session.commit()
    print(f"Updated entry ID {entry_id}.")


def delete_food_entry(session, entry_id):
    entry = session.query(FoodEntry).filter_by(id=entry_id).first()
    if not entry:
        print(f"Entry ID {entry_id} not found.")
        return

    session.delete(entry)
    session.commit()
    print(f"Deleted entry ID {entry_id}.")
