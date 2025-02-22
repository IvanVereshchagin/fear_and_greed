import os

from app.service import Service
from app.payment import Payment

from models.ml_task import MLTask
from models.model import Model
from models.prediction import MarketSentiment , PredictionHistory
from models.transaction import Transaction
from models.user import User , UserRole


import time 
from database.config import get_settings
from database.database import init_db

from cruds.crud_user import get_all_users, insert_user, get_user_by_id ,  get_user_by_email
from cruds.crud_transaction import get_all_transactions, insert_transaction, get_transaction_by_id , get_transaction_by_user_id
from cruds.crud_prediction import get_all_predictions , insert_prediction , get_last_user_prediction , get_prediction_by_id
from cruds.crud_model import insert_model , get_all_models , get_model_by_id
from cruds.crud_ml_task import insert_ml_task , get_all_ml_tasks , get_ml_task_by_id



from sqlmodel import SQLModel, Session, create_engine , Field
from typing import Optional, List
from database.database import engine
from datetime import datetime

if __name__ == "__main__":

  test_user = User(password='test' , username = 'vova', email='test1@mail.ru', balance = 0 , role = UserRole.ADMIN  )
  test_user_2 = User(password='test2' , username = 'katya', email='test2@mail.ru', balance = 0 , role =  UserRole.USER)
  test_user_3 = User(password='test3' , username = 'zhanna', email='test3@mail.ru', balance = 0 , role =  UserRole.USER)

  test_transaction = Transaction( transaction_id= 1 , user_id=1, amount = 5 , timestamp = datetime(2025,1,5,10,30,30) , description = 'test' , successful= True )

  test_prediction = PredictionHistory( user_id = 1 , model_id= 1 , features = 'test' , prediction = 20.0 , category = MarketSentiment.EXTREME_BEARISH , timestamp = datetime(2025, 1, 30,10,25,25))

  test_model = Model(model = 'boosting.pkl')


  test_ml_task = MLTask(features = {'test' : 123 }, labels = [1,2] )

  settings = get_settings()
  print(settings.DB_HOST)
  print(settings.DB_NAME)

  time.sleep(40)
  
  init_db()
  print('init is succesful')

  with Session(engine) as session:
    insert_user(test_user, session)
    insert_user(test_user_2, session)
    insert_user(test_user_3, session)
    users = get_all_users(session)

    for user in users:
      user.add_funds(5)
      user.charge(3)

    user1 = get_user_by_id('1' , session)
    user2 = get_user_by_email('test3@mail.ru' , session )

    print(user1)
    print(user2)

    insert_transaction(test_transaction , session)
    transactions = get_all_transactions(session)

    

    for user in users:
      print(f'id: {user.user_id} - {user.email} ')
      print(f'user balance : {user.balance}')

    for transaction in transactions : 
      print(f'user_id {transaction.user_id} , timestamp {transaction.timestamp} ')
  

    transaction1 = get_transaction_by_user_id(1 , session)
    print(transaction1)

    insert_prediction(test_prediction , session)
    predictions = get_all_predictions(session)

    for prediction in predictions :
      print(f'prediction_id {prediction.prediction_id} , timestamp {prediction.timestamp}')

    

    insert_ml_task(test_ml_task  ,session)
    ml_tasks = get_all_ml_tasks(session)

    for ml_task in ml_tasks :
      print(f'task_id {ml_task.task_id} , features {ml_task.features}')
    
    insert_model(test_model , session)
    models = get_all_models(session)

    for model in models:
      print(f'model_id {model.model_id} , model path {model.model}')

    




















