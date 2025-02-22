import streamlit as st
import requests
import hashlib
import os
import json
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, status, Depends  , Body
from  database.database import get_session
from cruds import crud_user as UserService
from database.config import get_settings


FASTAPI_URL = "http://app:8080"  


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


class PredictionInput(BaseModel):
    feature1: float
    feature2: float
    feature3: float
    feature4: float
    feature5: float 


def register_user(email, password, username):
    user = { "email" : email , "password" : password , "username" : username }
    try:
        response = requests.post(f"{FASTAPI_URL}/user/signup", json=user)  
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"Ошибка при регистрации: {e} - {response.text if 'response' in locals() else ''}")
        return False

def authenticate_user(email, password):
    user_data = { "email" :  email , "password" :  password }
    try:
        response = requests.post(f"{FASTAPI_URL}/user/signin", json=user_data) 
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"Ошибка при входе: {e} - {response.text if 'response' in locals() else ''}")
        return False

def get_user_balance(email):
    """Получает баланс пользователя из FastAPI."""
    try:
        response = requests.post(f"{FASTAPI_URL}/balance/user_balance", json={"email": email})
        response.raise_for_status()
        data = response.json()
        return data["user balance"]
    except requests.exceptions.RequestException as e:
        st.error(f"Ошибка при получении баланса: {e} - {response.text if 'response' in locals() else ''}")
        return None

def update_balance(email, amount):
    """Пополняет баланс пользователя через FastAPI."""
    try:
        response = requests.post(f"{FASTAPI_URL}/balance/add_funds", json={"email": email, "amount": amount})
        response.raise_for_status()
        data = response.json()
        return data["new_balance"]
    except requests.exceptions.RequestException as e:
        st.error(f"Ошибка при пополнении баланса: {e} - {response.text if 'response' in locals() else ''}")
        return None
    
def get_prediction(email, f1 , f2 , f3 , f4 , f5 ):
    """Получает предсказание из FastAPI."""
    session_generator = get_session()
    session = next(session_generator)
    user_data = UserService.get_user_by_email(email, session=session) 
    user_data_dict = {
    "password": user_data.password,
    "user_id": user_data.user_id,
    "username": user_data.username,
    "email": user_data.email,
    "balance": user_data.balance,
    "role": user_data.role
  }
    try:
        response = requests.post(f"{FASTAPI_URL}/user/predict",
                                 json={"user": user_data_dict, "prediction": {"feature1" : f1 , "feature2" : f2 , "feature3" : f3 , "feature4" : f4 , "feature5" : f5}})
        response.raise_for_status()
        data = response.json()
        return data["prediction"]
    except requests.exceptions.RequestException as e:
        st.error(f"Ошибка при получении предсказания: {e} - {response.text if 'response' in locals() else ''}")
        return None
    

def show_login_form():
    """Отображает форму логина/регистрации."""
    login_option = st.radio("Выберите:", ["Войти", "Зарегистрироваться"])

    if login_option == "Войти":
        email = st.text_input("Email")
        password = st.text_input("Пароль", type="password")
        if st.button("Войти"):
            if authenticate_user(email, password):
                st.session_state["authenticated"] = True
                st.session_state["email"] = email
                st.success("Вы успешно вошли!")
                st.rerun()
            else:
                st.error("Неверный email или пароль.")
    else:
        email = st.text_input("Email")
        username = st.text_input("Имя пользователя")
        password = st.text_input("Пароль", type="password")
        if st.button("Зарегистрироваться"):
            if register_user(email, password, username):
                st.success("Вы успешно зарегистрировались! Теперь можете войти.")
            else:
                st.error("Ошибка при регистрации. Пожалуйста, попробуйте еще раз.")


def main():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if "email" not in st.session_state:
        st.session_state["email"] = None

    if st.session_state["authenticated"]:
        email = st.session_state["email"]  
        st.write(f"## Добро пожаловать, {email}!")

        balance = get_user_balance(email)
        if balance is not None:
            st.write(f"Ваш баланс: {balance}")

        amount = st.number_input("Сумма для пополнения:", min_value=1.0, step=1.0)
        if st.button("Пополнить баланс"):
            new_balance = update_balance(email, amount)
            if new_balance is not None:
                st.success(f"Баланс успешно пополнен. Ваш новый баланс: {new_balance}")
                st.rerun()  
            else:
                st.error("Не удалось пополнить баланс.")

       
        st.subheader("Получить предсказание (Стоимость: 5 е.д.)")
        if balance is not None and balance >= 5:
            feature1 = st.number_input("feature1", value=0.0)
            feature2 = st.number_input("feature2", value=0.0)
            feature3 = st.number_input("feature3", value=0.0)
            feature4 = st.number_input("feature4", value=0.0)
            feature5 = st.number_input("feature5", value=0.0)

            if st.button("Получить предсказание"):
                prediction_input = PredictionInput(
                    feature1=feature1,
                    feature2=feature2, 
                    feature3=feature3,
                    feature4=feature4,
                    feature5=feature5
                )

                new_balance = update_balance(email, -5)
                if new_balance is not None:
                    prediction = get_prediction(email, prediction_input.feature1 , prediction_input.feature2 , prediction_input.feature3 , prediction_input.feature4 , prediction_input.feature5 )
                    
                    if prediction is not None:
                        st.success(f"Предсказание: {prediction}")
                        
                        
                    else:
                        st.error("Не удалось получить предсказание.")
                else:
                    st.error("Не удалось списать средства с баланса.")

        elif balance is not None:
            st.warning(f"Недостаточно средств на балансе.  Требуется 5 ед. для получения предсказания.")

        if st.button("Выйти"):
            st.session_state["authenticated"] = False
            st.session_state["email"] = None
            st.rerun()
    else:
        show_login_form()

if __name__ == "__main__":
    main()