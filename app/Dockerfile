FROM python:3.9-slim-buster




COPY requirements.txt .


RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt


COPY . .

EXPOSE 8080


CMD ["python", "main.py"]