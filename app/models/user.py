from enum import Enum
from sqlmodel import SQLModel, Field
from typing import Optional, List


class UserRole(str , Enum):
    ADMIN = "admin"
    USER = "user"



class User(SQLModel, table=True):

    __table_args__ = {'extend_existing': True}

    password: str
    user_id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str = Field( unique= True , index = True , nullable = False )
    balance : float
    role : UserRole



    def add_funds(self, amount: float) -> None:
        """Увеличивает баланс пользователя."""
        if amount > 0:
          self.balance += amount

    def charge(self, amount: float) -> bool:
        """Списывает средства с баланса, если достаточно. Возвращает True, если успешно, иначе False."""
        if self.balance >= amount:
            self.balance -= amount
            return True
        else:
            return False

    
    

    
    
