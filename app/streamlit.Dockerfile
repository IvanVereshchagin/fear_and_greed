FROM python:3.9-slim-buster

WORKDIR /app


COPY app /app


RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 8501

ENV DATABASE_HOST=postgres
ENV DATABASE_PORT=5432
ENV DATABASE_USER=your_user
ENV DATABASE_PASSWORD=your_password
ENV DATABASE_NAME=your_database

ENV PYTHONPATH=/app

CMD ["streamlit", "run", "/app/streamlit_app.py"]