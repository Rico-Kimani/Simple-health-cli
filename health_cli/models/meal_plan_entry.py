from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from health_cli.db.database import Base
from health_cli.models.users_entry import User

class MealPlan(Base):
    __tablename__ = "mealplans"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    week_number = Column(Integer)
    meals = Column(String)  # You can store JSON-encoded strings or comma-separated for simplicity

    user = relationship("User", back_populates="mealplans")


# --- CRUD-like Helpers ---

def create_meal_plan(session, user_name, week_number, meals):
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        raise ValueError("User not found.")

    plan = MealPlan(user_id=user.id, week_number=week_number, meals=meals)
    session.add(plan)
    session.commit()
    return plan

def update_meal_plan(session, plan_id, week_number=None, meals=None):
    plan = session.query(MealPlan).filter_by(id=plan_id).first()
    if not plan:
        raise ValueError("Meal plan not found.")

    if week_number:
        plan.week_number = week_number
    if meals:
        plan.meals = meals

    session.commit()
    return plan

def list_meal_plans(session, user_name):
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        raise ValueError("User not found.")
    
    return session.query(MealPlan).filter_by(user_id=user.id).all()

def get_meal_plan(session, plan_id):
    return session.query(MealPlan).filter_by(id=plan_id).first()
