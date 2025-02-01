from sqlalchemy.orm import Session
from database_setup import User, Session

def authenticate_user(username: str, password: str):
    session = Session()
    user = session.query(User).filter(User.username == username).first()
    session.close()
    if user and user.password == password:
        return user
    return None
