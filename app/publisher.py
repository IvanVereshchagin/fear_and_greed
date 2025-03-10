class Publisher:
    def send_ml_task(task_data):
        import pika
        import json
        import os 

        
        


        credentials = pika.PlainCredentials('rmuser', 'rmpassword')
        parameters = pika.ConnectionParameters( host = 'rabbitmq',
                                                port = 5672 , 
                                                virtual_host='/',
                                                credentials=credentials
                                             
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
    Publisher.send_ml_task(task)

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
    Publisher.send_ml_task(task)

    print("Задачи отправлены.")