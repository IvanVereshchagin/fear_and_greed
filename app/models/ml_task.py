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

    task_id : Optional[int] = Field(default=None, primary_key=True, index=True) 
    features : str
    labels : str 
   



    


    