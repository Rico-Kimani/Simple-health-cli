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


# ---------------- CRUD FUNCTIONS ---------------- #

def add_food_entry(session, user_name, food, calories, date):
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        raise ValueError(f"User '{user_name}' does not exist.")

    entry = FoodEntry(user=user, food=food, calories=calories, date=date)
    session.add(entry)
    session.commit()
    return entry


def list_food_entries(session, user_name=None, date=None):
    query = session.query(FoodEntry)

    if user_name:
        user = session.query(User).filter_by(name=user_name).first()
        if not user:
            raise ValueError(f"User '{user_name}' not found.")
        query = query.filter_by(user_id=user.id)

    if date:
        query = query.filter_by(date=date)

    return query.all()


def update_food_entry(session, entry_id, food=None, calories=None, date=None):
    entry = session.query(FoodEntry).filter_by(id=entry_id).first()
    if not entry:
        raise ValueError(f"Entry ID {entry_id} not found.")

    if food:
        entry.food = food
    if calories:
        entry.calories = calories
    if date:
        entry.date = date

    session.commit()
    return entry


def delete_food_entry(session, entry_id):
    entry = session.query(FoodEntry).filter_by(id=entry_id).first()
    if not entry:
        raise ValueError(f"Entry ID {entry_id} not found.")

    session.delete(entry)
    session.commit()
    return True
