import sys
import json
import time
import requests
import threading
import os
import pika
import joblib 
from app.models.prediction import MarketSentiment , PredictionHistory
from app.cruds import crud_user as UserService
from app.cruds import crud_prediction as PredictionService
import datetime 
from  app.database.database import get_session
import numpy as np

import time 
from app.database.config import get_settings
from app.database.database import init_db
import sqlalchemy

from sqlmodel import SQLModel, Session, create_engine , Field
from typing import Optional, List
from app.database.database import engine

from app.cruds.crud_prediction import get_all_predictions , insert_prediction , get_user_prediction , get_prediction_by_id


exchange_name = 'ml_tasks'
queue_name = 'test'

credentials = pika.PlainCredentials('rmuser', 'rmpassword')
parameters = pika.ConnectionParameters(host='rabbitmq',
                                        port=5672,
                                        virtual_host='/',
                                        credentials=credentials,
                                        heartbeat=30,
                                        blocked_connection_timeout=2)

def callback(ch, method, properties, body):
    try:
        print(f"Получено сообщение с delivery_tag: {method.delivery_tag}") 

        task_data = json.loads(body.decode('utf-8'))

        print(task_data)


        if not isinstance(task_data, dict):
            raise ValueError("Данные должны быть словарем")
        if "user" not in task_data or "prediction" not in task_data:
            raise ValueError("Данные должны содержать ключи 'user' и 'prediction'")

        
        try:

            settings = get_settings()
            time.sleep(4)
            try:
                init_db()
            except sqlalchemy.exc.ProgrammingError as e : 
                print(e)
                pass

            

            
            loaded_model = joblib.load("./app/regression_model.joblib")
            feature_array = np.array([ i for i in task_data['prediction'].values() ])
            predicted_index = loaded_model.predict(feature_array.reshape(1, -1))[0]

            print('predicted index' , predicted_index)

            if 0 <= predicted_index <= 10:
                sentiment =  MarketSentiment.EXTREME_BEARISH
            elif 11 <= predicted_index <= 20:
                sentiment = MarketSentiment.RADICAL_BEARISH
            elif 21 <= predicted_index <= 30:
                sentiment = MarketSentiment.STRONG_BEARISH
            elif 31 <= predicted_index <= 40:
                sentiment = MarketSentiment.MODERATE_BEARISH
            elif 41 <= predicted_index <= 60:
                sentiment = MarketSentiment.NEUTRAL
            elif 61 <= predicted_index <= 70:
                sentiment = MarketSentiment.MODERATE_BULLISH
            elif 71 <= predicted_index <= 80:
                sentiment = MarketSentiment.STRONG_BULLISH
            elif 81 <= predicted_index <= 90:
                sentiment = MarketSentiment.RADICAL_BULLISH
            elif 91 <= predicted_index <= 100:
                sentiment = MarketSentiment.EXTREME_BULLISH
            else:
                
                sentiment = MarketSentiment.EXTREME_BULLISH


            pred_hist = PredictionHistory( user_id = task_data['user']['user_id'] , 
                                        model_id= 1 , 
                                        features = 'test' , 
                                        prediction = predicted_index , 
                                        category = sentiment ,
                                        timestamp = datetime.datetime.now())
            
            with Session(engine) as session:
                try:
                    insert_prediction(pred_hist , session )
                    
                except:
                    pass

            
            

            
            

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при вызове ML сервиса: {e}")
            
            return 
    except Exception as e:
        print(f"Ошибка при обработке задачи: {e}")
       
def process_ml_task():
    try:
        
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        channel.queue_declare(queue=queue_name)

        channel.basic_consume(
            queue=queue_name,
            on_message_callback=callback,
            auto_ack=True
        )

        print(f" [*] Воркер {threading.current_thread().name} ожидает задач. Для выхода нажмите CTRL+C")
        channel.start_consuming()
    except Exception as e:
        print(f"Ошибка в process_ml_task: {e}", file=sys.stderr)
if __name__ == '__main__':
    try:
        print('Запускаемся')
        process_ml_task()
    except Exception as e:
        print(f"Необработанное исключение в main: {e}", file=sys.stderr)
        sys.exit(1)

        