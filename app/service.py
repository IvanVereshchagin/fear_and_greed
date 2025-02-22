from datetime import datetime
from enum import Enum
from typing import List, Dict, Union
from abc import ABC, abstractmethod
from payment import Payment

from models.ml_task import MLTask
from models.model import Model
from models.prediction import MarketSentiment , PredictionHistory
from models.transaction import Transaction
from models.user import User , UserRole

class Service:
    """
    Главный класс, инкапсулирующий логику сервиса
    """
    def __init__(self, payment: Payment):
        self._users: Dict[int, User] = {}
        self._models: Dict[int, Model] = {}
        self._transactions: List[Transaction] = []
        self._predictions: List[PredictionHistory] = []
        self._tasks: Dict[int, MLTask] = {}
        self._payment = payment

    def register_user(self, username: str, email: str , password) -> User:
         user_id = len(self._users) + 1
         user = User(user_id, username, email , password)
         self._users[user_id] = user
         return user

    def add_model(self , model) -> Model:
         model_id = len(self._models) + 1
         model = Model(model , model_id )
         self._models[model_id] = model
         return model

    def get_user(self, user_id: int) -> Union[User, None]:
        return self._users.get(user_id)

    def add_funds(self, user_id: int, amount: float) -> bool:
        """Пополнение баланса пользователя"""
        user = self.get_user(user_id)
        if user is None:
          return False

        # Обработка платежа 
        if self._payment.process_payment(user_id, amount):
             user.add_funds(amount)
             self._transactions.append(Transaction(len(self._transactions) + 1, user_id, amount, datetime.now(), "Add Funds", True))
             return True
        else:
             self._transactions.append(Transaction(len(self._transactions) + 1, user_id, amount, datetime.now(), "Add Funds", False))
             return False


    def create_training_task(self, features: List[Dict[ str , Union[float, str]]], labels: List[float]) -> MLTask:
         task_id = len(self._tasks) + 1
         task = MLTask(task_id, features, labels)
         self._tasks[task_id] = task
         return task

    def train_model(self, model_id: int, task_id: int) -> bool:
         """Обучение модели."""
         model = self._models.get(model_id)
         task = self._tasks.get(task_id)

         if model is None or task is None:
             return False

         model.train(task.features, task.labels)
         return True

    def categorize_sentiment(self, predicted_index: float) -> MarketSentiment:
        """Определение категории настроения на основе предсказанного индекса."""

        if 0 <= predicted_index <= 10:
           return MarketSentiment.EXTREME_BEARISH
        elif 11 <= predicted_index <= 20:
           return MarketSentiment.RADICAL_BEARISH
        elif 21 <= predicted_index <= 30:
           return MarketSentiment.STRONG_BEARISH
        elif 31 <= predicted_index <= 40:
            return MarketSentiment.MODERATE_BEARISH
        elif 41 <= predicted_index <= 60:
            return MarketSentiment.NEUTRAL
        elif 61 <= predicted_index <= 70:
            return MarketSentiment.MODERATE_BULLISH
        elif 71 <= predicted_index <= 80:
            return MarketSentiment.STRONG_BULLISH
        elif 81 <= predicted_index <= 90:
            return MarketSentiment.RADICAL_BULLISH
        elif 91 <= predicted_index <= 100:
            return MarketSentiment.EXTREME_BULLISH
        else:
            raise ValueError("Предсказано неверное значение")



    def make_prediction(self, user_id: int, model_id: int, features: Dict[ str , Union[float, str]]) -> Union[PredictionHistory, None]:
         """Выполняет предсказание модели, категоризирует его и сохраняет результат."""

         user = self.get_user(user_id)
         if user is None:
            return None

         model = self._models.get(model_id)

         if model is None or model.status != ModelStatus.READY:
            return None

         predicted_index = model.predict(features)
         category = self.categorize_sentiment(predicted_index)

         # Стоимость предсказания
         prediction_price = 1
         if not user.charge(prediction_price):
           return None

         prediction_history = PredictionHistory(len(self._predictions) + 1, user_id, model_id, features, predicted_index, category, datetime.now())
         self._predictions.append(prediction_history)
         self._transactions.append(Transaction(len(self._transactions) + 1, user_id, prediction_price, datetime.now(), "Prediction", True))
         return prediction_history


    def get_transaction_history(self, user_id: int) -> List[Transaction]:
        """Возвращает историю транзакций пользователя"""
        return [transaction for transaction in self._transactions if transaction.user_id == user_id]

    def get_prediction_history(self, user_id: int) -> List[PredictionHistory]:
         """Возвращает историю предсказаний пользователя."""
         return [prediction for prediction in self._predictions if prediction.user_id == user_id]

