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


BASE_URL = "http://localhost:8080" 

#--- Тесты для Endpoint'a Signup --- 
# Позитивный тест , успешная авторизация
def test_signup_success():

    api_url = f"{BASE_URL}/user/signup"  

 
    email = f"admin{random.randint(1,100000)}@mail.ru"
    payload = {"email": email, "password": "test", "username": "vova"}

    
    response = requests.post(api_url, json=payload)
    response.raise_for_status()  
    assert response.status_code == status.HTTP_200_OK, f"Unexpected status code: {response.status_code}"
    assert response.json() == {"message": "User was create"}, f"Unexpected response body: {response.json()}"
    print(f"Signup test successful for email: {email}")  

    


# Негативный тест, ошибка при авторизации
def test_signup_failure():
   
    api_url = f"{BASE_URL}/user/signup"  

    email = f"admin{random.randint(1,100000)}"
    payload = {"email": email, "password": "test", "username": "vova"}

   
    response = requests.post(api_url, json=payload)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, f"Expected 422, but got {response.status_code}"
    assert "Email must contain the '@' symbol" in response.text, "Error message is missing or incorrect"

    
# Негативный тест, регистрация существующего пользователя 
def test_signup_email_exists():
    api_url = f"{BASE_URL}/user/signup"  

    email = f"admin@mail.ru"
    payload = {"email": email, "password": "test", "username": "vova"}

   
    response = requests.post(api_url, json=payload)

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == {"detail": "Email is exist"}

#--- Тесты для Endpoint'a all_users ---

def test_get_all_users_success():
    api_url = f"{BASE_URL}/user/all_users"

    
    response = requests.get(api_url)  
    response.raise_for_status()

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert "users" in data, "Response should contain a 'users' key"
    assert len(data["users"]) >= 2, "Expected at least 2 users, but found less"

# # ---- Тесты для Endpoint'a /signin ----
# Позитивный тест
def test_signin_success():
    
    api_url = f"{BASE_URL}/user/signin"
    payload =  {"email": 'admin@mail.ru', "password": "test", "username": "vova"}
    
    response = requests.post(api_url , json= payload )  

    response.raise_for_status()
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "User signed in successfully"}

# Негативный тест, несуществующий пользователь
def test_signin_user_not_found():
    api_url = f"{BASE_URL}/user/signin"
    payload =  {"email": 'boris3943939489@mail.ru', "password": "test", "username": "vova"}
    
    response = requests.post(api_url , json= payload )  

    assert response.status_code == status.HTTP_404_NOT_FOUND

    assert response.json() == {"detail": "User does not exist"}

# Негативный тест, неправильный пароль при авторизации
def test_signin_wrong_password():
    api_url = f"{BASE_URL}/user/signin"
    payload =  {"email": 'admin@mail.ru', "password": "test1223", "username": "vova"}
    
    response = requests.post(api_url , json= payload )


    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"detail": "Wrong credentials passed"}

# --- Тесты для Endpoint'a predict ---
# Позитивный тест
def test_predict_success():
    payload = {
  "user": {
    "password": "test",
    "user_id": 0,
    "username": "vova",
    "email": "admin@mail.ru",
    "balance": 0,
    "role": "admin"
  },
  "prediction": {
    "feature1": 0,
    "feature2": 0,
    "feature3": 0,
    "feature4": 0,
    "feature5": 0
  }
}
    
    api_url = f"{BASE_URL}/user/predict"
    response = requests.post(
        api_url,
        json= payload
        
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "prediction" in data
    assert "user_id" in data

# Негативный тест
def test_predict_user_not_found():
    
    payload = {
  "user": {
    "password": "test",
    "user_id": 0,
    "username": "vova",
    "email": "adminnnnn@mail.ru",
    "balance": 0,
    "role": "admin"
  },
  "prediction": {
    "feature1": 0,
    "feature2": 0,
    "feature3": 0,
    "feature4": 0,
    "feature5": 0
  }
}
    
    api_url = f"{BASE_URL}/user/predict"
    response = requests.post(
        api_url,
        json= payload
        
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "User does not exist"}

# --- Тесты для Endpoint'a predictions --- 
# Позитивный тест
def test_predictions_success():
    
    payload = {
  "password": "test",
  "user_id": 0,
  "username": "vova",
  "email": "admin@mail.ru",
  "balance": 0,
  "role": "admin"
}
    
    api_url = f"{BASE_URL}/user/predictions"
    response = requests.post(
        api_url,
        json= payload
        
    )


    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "predictions" in data
    assert "user_id" in data
    assert len(data["predictions"]) != 0

# Негативный тест
def test_predictions_user_not_found():
   
    payload = {
  "password": "test",
  "user_id": 0,
  "username": "vova",
  "email": "adminnnn12213@mail.ru",
  "balance": 0,
  "role": "admin"
}
    
    api_url = f"{BASE_URL}/user/predictions"
    response = requests.post(
        api_url,
        json= payload
        
    )


    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "User does not exist"}