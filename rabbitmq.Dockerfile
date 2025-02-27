FROM python:3.9-slim-buster




COPY ./app/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./project/app
COPY ./rabbitmq ./project/

WORKDIR /project


CMD ["python", "consumer.py"]