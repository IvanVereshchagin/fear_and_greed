from datetime import datetime
from enum import Enum
from typing import List, Dict, Union
from abc import ABC, abstractmethod
from sqlmodel import SQLModel, Field
from typing import Optional, List


class Transaction(SQLModel, table=True):
    transaction_id:  Optional[int] = Field(default=None, primary_key=True, index=True) 
    user_id: int 
    amount: float
    timestamp: datetime
    description: str
    successful: bool