FROM python:3.9-slim-buster

COPY ./app ./project/app
COPY ./app/streamlit_app.py ./project/

COPY ./app/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

ENV DATABASE_HOST=postgres
ENV DATABASE_PORT=5432
ENV DATABASE_USER=postgres
ENV DATABASE_PASSWORD=postgres
ENV DATABASE_NAME=sa


WORKDIR /project

CMD ["streamlit", "run", "streamlit_app.py"]