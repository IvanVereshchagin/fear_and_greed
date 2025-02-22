FROM python:3.9


COPY . . 


RUN pip install --upgrade pip && pip install -r requirements.txt


EXPOSE 8080


CMD ["python", "main.py"]