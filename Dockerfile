FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    DATA_DIR=/data

COPY requirements.txt .
COPY .. .
RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 8000

CMD ["python", "app.py"]