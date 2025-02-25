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
from cruds.crud_prediction import get_all_predictions , insert_prediction , get_user_prediction , get_prediction_by_id
from cruds.crud_model import insert_model , get_all_models , get_model_by_id
from cruds.crud_ml_task import insert_ml_task , get_all_ml_tasks , get_ml_task_by_id

from sqlmodel import SQLModel, Session, create_engine , Field
from typing import Optional, List
from database.database import engine
from datetime import datetime

from routes.user import user_route
from app.routes.balance import balance_route
from fastapi.middleware.cors import CORSMiddleware
from api_analytics.fastapi import Analytics 

import uvicorn
from fastapi import FastAPI

from publisher import Publisher

def initialize_database():
    settings = get_settings()

    time.sleep(40)

    init_db()

    admin = User(password='test' , username = 'vova', email='admin@mail.ru', balance = 0 , role = UserRole.ADMIN  )
    user = User(password='test2' , username = 'katya', email='user@mail.ru', balance = 0 , role =  UserRole.USER)

    with Session(engine) as session:
        try:
            insert_user(admin, session)
            insert_user(user, session)
        except:
            pass

app = FastAPI()
app.include_router(user_route, prefix='/user')
app.include_router(balance_route , prefix='/balance')
app.add_middleware(Analytics , api_key = "268f2ff9-1819-49c3-b1f9-8cffdafde6a4")

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins , 
    allow_credentials = True , 
    allow_methods = ["*"],
    allow_headers = ["*"]

)

@app.on_event("startup") 
def on_startup():
    initialize_database()

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8080)