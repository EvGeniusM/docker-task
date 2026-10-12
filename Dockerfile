FROM python:3.12-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN useradd -r -u 1000 app
COPY --chown=app:app . .
USER app

EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]