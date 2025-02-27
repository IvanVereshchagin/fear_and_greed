from datetime import datetime
from enum import Enum
from typing import List, Dict, Union
from abc import ABC, abstractmethod
from sqlmodel import SQLModel, Field
from typing import Optional, List

class Model(SQLModel, table=True):
    """
     Пример простой ML модели для регрессии.
    """
    #__tablename__ = 'model'
    __table_args__ = {'extend_existing': True}
    model : str
    model_id : Optional[int] = Field(default=None, primary_key=True, index=True)  

    def predict(self, features: Dict[str, Union[float, str]]) -> float:
        pass

    def train(self, features: List[Dict[str,  Union[float, str]]], labels: List[float]) -> None:
        
        pass

    
