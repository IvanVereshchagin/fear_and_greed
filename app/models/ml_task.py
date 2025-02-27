from datetime import datetime
from enum import Enum
from typing import List, Dict, Union
from abc import ABC, abstractmethod
from sqlmodel import SQLModel, Field
from typing import Optional, List

class MLTask(SQLModel, table=True):
    """
     Представляет задачу для обучения ML модели.
    """

    #__tablename__ = 'ml task'
    __table_args__ = {'extend_existing': True}

    task_id : Optional[int] = Field(default=None, primary_key=True, index=True) 
    features : str
    labels : str 
   



    


    