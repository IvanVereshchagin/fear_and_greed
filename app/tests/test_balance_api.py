import sys
import os

APP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, APP_DIR)

import warnings
warnings.filterwarnings("ignore")

import pytest

from fastapi import status

from main import app 


from service import Service
from payment import Payment

from models.ml_task import MLTask
from models.model import Model
from models.prediction import MarketSentiment , PredictionHistory
from models.transaction import Transaction
from models.user import User , UserRole

import time 
from database.config import get_settings
from database.database import init_db
from database.database import engine , get_session

from sqlmodel import SQLModel, Session, create_engine , Field
from typing import Optional, List

from datetime import datetime

from routes.user import user_route
from routes.balance import balance_route

import uvicorn
from fastapi import FastAPI

from fastapi.testclient import TestClient

from cruds import crud_user as UserService
from cruds import crud_prediction as PredictionService

import requests

import random




#Тесты для Endpoint'a user_balance
# Позитивный тест
def test_user_balance_success():
    
    api_url = 'http://localhost:8080/balance/user_balance'

    payload = {"email": 'admin@mail.ru'}

    response = requests.post(api_url, json=payload)

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "user balance" in data
    assert data["user balance"] == 0 

#Негативный тест
def test_user_balance_not_found():
   
    api_url = 'http://localhost:8080/balance/user_balance'

    payload = {"email": "admin@gmail.com"}

    response = requests.post(api_url, json=payload)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "User does not exist"}

#Тесты для Endpoint'a add_funds 
# Позитивный тест
def test_add_funds_success():
   
    api_url = "http://localhost:8080/balance/add_funds"

    amount = 100.0
    payload = {"email": 'user@mail.ru', "amount": amount}

    response = requests.post(api_url, json=payload)
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "message" in data
    assert data["message"] == "Balance was changed"
    assert "new_balance" in data
    assert data["new_balance"] == amount

    
    

# Негативный тест , не найден юзер
def test_add_funds_user_not_found():
   
    api_url = "http://localhost:8080/balance/add_funds"

    amount = 100.0
    payload = {"email": "nonexistent@example.com", "amount": amount}

    response = requests.post(api_url, json=payload)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "User is not exist"}


# Позитивный тест
def test_add_funds_zero_amount():
    api_url = "http://localhost:8080/balance/add_funds"


    amount = 0
    payload = {"email": 'user@mail.ru', "amount": amount}

    response = requests.post(api_url, json=payload)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['new_balance'] == 0