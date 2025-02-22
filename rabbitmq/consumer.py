import json
import time
import requests
import threading
import os
import pika 

rabbitmq_host = os.environ.get('RABBITMQ_HOST', 'localhost')
rabbitmq_user = os.environ.get('RABBITMQ_USER', 'rmuser')
rabbitmq_pass = os.environ.get('RABBITMQ_PASSWORD', 'rmpassword')
exchange_name = 'ml_tasks'
queue_name = 'test' 


credentials = pika.PlainCredentials('rmuser', 'rmpassword')
parameters = pika.ConnectionParameters(host='localhost',
                                        port=5675,
                                        virtual_host='/',
                                        credentials=credentials,
                                        heartbeat=30,
                                        blocked_connection_timeout=2)

def callback(ch, method, properties, body):
    """
    Функция, которая вызывается при получении сообщения.
    """
    try:
        print(type(body))
        print(body)
        task_data = json.loads(body.decode('utf-8'))

        # Валидация входных данных
        if not isinstance(task_data, dict):
            raise ValueError("Данные должны быть словарем")
        if "user" not in task_data or "prediction" not in task_data:
            raise ValueError("Данные должны содержать ключи 'user' и 'prediction'")

        # Предсказание
        try:
            response = requests.post('http://localhost:8080/user/predict' , json=task_data) 
            response.raise_for_status()
            result = response.json()
            print(f" [x] Получен ответ от ML сервиса: {result}")

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при вызове ML сервиса: {e}")

        print(f" [x] Задача выполнена. Результат сохранен.")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print(f"Ошибка при обработке задачи: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

def process_ml_task():  
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue=queue_name)  

    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=False  
    )

    print(f" [*] Воркер {threading.current_thread().name} ожидает задач. Для выхода нажмите CTRL+C")
    channel.start_consuming()




if __name__ == '__main__':
    
    print('Запускаемся')
    
    process_ml_task()

    print("Все воркеры запущены.")

    try:
        while True:
            time.sleep(5) 
    except KeyboardInterrupt:
        print("\nПолучен сигнал завершения. Завершаем работу...")

 