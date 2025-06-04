from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from health_cli.db.database import Base
from health_cli.models.users_entry import User

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

def get_user_goals(session, user_name):
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        return None

    return session.query(Goal).filter_by(user_id=user.id).first()
