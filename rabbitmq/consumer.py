import sys
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
parameters = pika.ConnectionParameters(host='rabbitmq',
                                        port=5672,
                                        virtual_host='/',
                                        credentials=credentials,
                                        heartbeat=30,
                                        blocked_connection_timeout=2)

def callback(ch, method, properties, body):
    try:
        print(f"Получено сообщение с delivery_tag: {method.delivery_tag}")  # Добавлено логирование

        task_data = json.loads(body.decode('utf-8'))

        print(task_data)


        if not isinstance(task_data, dict):
            raise ValueError("Данные должны быть словарем")
        if "user" not in task_data or "prediction" not in task_data:
            raise ValueError("Данные должны содержать ключи 'user' и 'prediction'")

        
        try:
            response = requests.post('http://app:8080/user/predict', json=task_data)
            response.raise_for_status()
            result = response.json()
            print(f" [x] Получен ответ от ML сервиса: {result}")

            print(f" [x] Задача выполнена. Результат сохранена.")

            
            

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

