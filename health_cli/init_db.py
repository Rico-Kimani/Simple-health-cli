import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from health_cli.db.database import Base
from health_cli.db.config import engine
from health_cli.models.users_entry import User

def init():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Done.")

if __name__ == "__main__":
    init()
