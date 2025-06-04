from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from health_cli.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    age = Column(Integer)

    # Relationships
    food_entries = relationship("FoodEntry", back_populates="user", cascade="all, delete-orphan")
    goal = relationship("Goal", back_populates="user", uselist=False)
    mealplans = relationship("MealPlan", back_populates="user", cascade="all, delete-orphan")
