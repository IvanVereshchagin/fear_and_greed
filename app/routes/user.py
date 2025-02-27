from fastapi import APIRouter, HTTPException, status, Depends  , Body
from  database.database import get_session
from models.user import User, UserRole

from cruds import crud_user as UserService
from cruds import crud_prediction as PredictionService

from typing import List
from pydantic import BaseModel
import joblib 
import numpy as np
import datetime
from models.prediction import MarketSentiment , PredictionHistory
from publisher import Publisher
import sqlalchemy.exc as alc_errors
from app.logging.signup_logger import logger 
from psycopg import errors as pg_errors

import time 
from publisher import Publisher 

user_route = APIRouter(tags=['User'])

class SignUpForm(BaseModel): 
    email: str
    password: str
    username : str

@user_route.post('/signup')
async def signup( data : SignUpForm , session =Depends(get_session)) -> dict: 

    if "@" not in data.email:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Email must contain the '@' symbol")


    if UserService.get_user_by_email(data.email, session=session) is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User is exist")

    user = User(password= data.password , username = data.username , email= data.email , balance = 0 , role =  UserRole.USER)

    try:
        UserService.insert_user(user , session=session)
    except alc_errors.IntegrityError as e:
        pass
    except pg_errors.UniqueViolation as e: 
        pass


    # --- Logging ---
    data = {

        'password' : user.password,
        'username' : user.username,
        'email' : user.email, # Исправлено: было user.password, должно быть user.email
        'role' : user.role

    }
    logger.info(f"NewUser" , extra = data )

    # --- Logging ---

    return {"message": "User was create"}


@user_route.get('/all_users')
async def get_all_users(session=Depends(get_session)) -> dict:
    users = UserService.get_all_users(session=session)

    user_dict = {"users": users}

    return user_dict


class SignInForm(BaseModel):
    email: str
    password: str

@user_route.post('/signin')
async def signin(data : SignInForm, session=Depends(get_session)) -> dict:
    user = UserService.get_user_by_email(data.email, session=session)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")

    if user.password != data.password:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong credentials passed")

    return {"message": "User signed in successfully"}


class PredictionInput(BaseModel):
    feature1: float
    feature2: float
    feature3: float
    feature4: float
    feature5: float 



@user_route.post('/predict')
async def predict(user : User, prediction : PredictionInput = Body(...), session=Depends(get_session)) -> dict:
    """
    Эндпоинт для получения предсказаний на основе данных пользователя и данных о признаках.
    """
    user = UserService.get_user_by_email(user.email, session=session)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")
    
    feature_array = np.array([prediction.feature1, prediction.feature2, prediction.feature3 , prediction.feature4 , prediction.feature5])

    task = {
  "user": {
    "password": user.password,
    "user_id": user.user_id,
    "username": user.username ,
    "email": user.email,
    "balance": user.balance,
    "role": user.role
  },
  "prediction": {
    "feature1": prediction.feature1,
    "feature2": prediction.feature2,
    "feature3": prediction.feature3,
    "feature4": prediction.feature4,
    "feature5": prediction.feature5
  } }
    
    
    Publisher.send_ml_task(task)

    

    return {"user_id": user.user_id, "message": 'Сообщение отправлено на обработку'}

class EmailForm(BaseModel): 
    email: str


@user_route.post('/predictions')
async def predictions(data : EmailForm,  session=Depends(get_session)) -> dict:
    
    user_get = UserService.get_user_by_email( data.email , session=session)
    if user_get is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")
    all_user_predictions = PredictionService.get_user_prediction( user_get.user_id , session)
    return {"email": data.email, "predictions": all_user_predictions }
