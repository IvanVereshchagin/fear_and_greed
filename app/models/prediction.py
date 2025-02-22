from datetime import datetime
from enum import Enum
from typing import List, Dict, Union
from abc import ABC, abstractmethod
from sqlmodel import SQLModel, Field
from typing import Optional, List


class MarketSentiment(Enum):
    """
    Возможные значения настроения рынка (категории на основе предсказанного индекса страха и жадности)
    """
    EXTREME_BEARISH = -4  # 0 - 10
    RADICAL_BEARISH = -3   # 11-20
    STRONG_BEARISH = -2  # 21 - 30
    MODERATE_BEARISH = -1 # 31-40
    NEUTRAL = 0         # 41-60
    MODERATE_BULLISH = 1 # 61-70
    STRONG_BULLISH = 2   # 71-80
    RADICAL_BULLISH = 3  # 81-90
    EXTREME_BULLISH = 4  # 91-100



class PredictionHistory(SQLModel, table=True):
    prediction_id : Optional[int] = Field(default=None, primary_key=True, index=True) 
    user_id : int
    model_id : int 
    features : str
    prediction : float
    category : MarketSentiment
    timestamp : datetime



