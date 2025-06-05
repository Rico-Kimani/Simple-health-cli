from sqlalchemy import Column, Integer, ForeignKey, func
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from health_cli.db.database import Base
from health_cli.models.users_entry import User
from health_cli.models.food_entry import FoodEntry


class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    daily_goal = Column(Integer)
    weekly_goal = Column(Integer)

    user = relationship("User", back_populates="goal")


# --- CRUD-Like Helpers ---

def set_user_goals(session, user_name, daily, weekly):
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        raise ValueError("User not found.")

    goal = session.query(Goal).filter_by(user_id=user.id).first()
    if goal:
        goal.daily_goal = daily
        goal.weekly_goal = weekly
    else:
        goal = Goal(user_id=user.id, daily_goal=daily, weekly_goal=weekly)
        session.add(goal)
    
    session.commit()
    return goal


def get_user_goals(session, user_name):
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        raise ValueError ("None")

    return session.query(Goal).filter_by(user_id=user.id).first()


# --- Calorie Tracking Helper ---

def get_calorie_progress(session, user_name):
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        raise ValueError("User not found.")
    
    goal = get_user_goals(session, user_name)
    if not goal:
        raise ValueError("No goals set for this user.")

    today = datetime.utcnow().date()
    week_start = today - timedelta(days=today.weekday())  # Monday
    week_end = week_start + timedelta(days=6)

    daily_total = session.query(func.sum(FoodEntry.calories)).filter(
        FoodEntry.user_id == user.id,
        func.date(FoodEntry.date) == today
    ).scalar() or 0

    weekly_total = session.query(func.sum(FoodEntry.calories)).filter(
        FoodEntry.user_id == user.id,
        func.date(FoodEntry.date) >= week_start,
        func.date(FoodEntry.date) <= week_end
    ).scalar() or 0

    return {
        "daily_total": daily_total,
        "weekly_total": weekly_total,
        "daily_goal": goal.daily_goal,
        "weekly_goal": goal.weekly_goal
    }
