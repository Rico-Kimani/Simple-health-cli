from datetime import datetime
from health_cli.models.users_entry import User

def parse_date(date_str: str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Invalid date format. Please use YYYY-MM-DD.")

def user_exists(session, user_name: str) -> bool:
    return session.query(User).filter(User.name == user_name).first() is not None
