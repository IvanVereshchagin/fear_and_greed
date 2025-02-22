from models.user import User 
from typing import List, Optional

def get_all_users(session) -> List[User]:
    return session.query(User).all()

def get_user_by_id(id: int, session) -> Optional[User]:
    return session.get(User, id)
    

def get_user_by_email(email: str, session) -> Optional[User]:
    user = session.query(User).filter(User.email == email).first()
    if user:
        return user
    return None

def insert_user(new_user: User, session) -> None:
    session.add(new_user)
    session.commit()
    session.refresh(new_user)


def update_balance(user: User, new_balance: float, session) -> Optional[User]:
   
    try:
        user.balance = new_balance
       
        session.add(user)
        session.commit()
        session.refresh(user)  
        return user
    except Exception as e:
        session.rollback()
   
        return None