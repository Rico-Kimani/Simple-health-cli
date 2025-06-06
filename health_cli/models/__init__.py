from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from health_cli.db.database import get_session
from health_cli.db.database import Base

engine = create_engine('sqlite:///health.db')  
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a session instance
session = get_session()
