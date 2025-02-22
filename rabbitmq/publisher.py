def send_ml_task(task_data):
    import pika
    import json
    import os 

    
    rabbitmq_host = os.environ.get('RABBITMQ_HOST', 'localhost')
    rabbitmq_user = os.environ.get('RABBITMQ_USER', 'rmuser')
    rabbitmq_pass = os.environ.get('RABBITMQ_PASSWORD', 'rmpassword')
    exchange_name = 'ml_tasks'      


    credentials = pika.PlainCredentials('rmuser', 'rmpassword')
    parameters = pika.ConnectionParameters( host = 'localhost',
                                            port = 5675 , 
                                            virtual_host='/',
                                            credentials=credentials,
                                            heartbeat=30,
                                            blocked_connection_timeout=2
                                            )

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()


    queue_name = 'test'
    channel.queue_declare(queue=queue_name)

    message = json.dumps(task_data) 
    channel.basic_publish(exchange='', routing_key= queue_name, body=message)
    print(f" [x] Отправлена задача: {task_data}")

    connection.close()

if __name__ == '__main__':
    
    task = {
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
    send_ml_task(task)

    task = {
  "user": {
    "password": "test2",
    "user_id": 0,
    "username": "katya",
    "email": "user@mail.ru",
    "balance": 0,
    "role": "user"
  },
  "prediction": {
    "feature1": 0,
    "feature2": 0,
    "feature3": 0,
    "feature4": 0,
    "feature5": 0
  }
}
    send_ml_task(task)

    print("Задачи отправлены.")