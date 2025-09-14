FROM python:3.11-slim
WORKDIR /app
COPY backend /app
RUN pip install -U pip && pip install -e .
ENV PYTHONUNBUFFERED=1
CMD ["celery", "-A", "app.workers.celery_app.celery_app", "worker", "--loglevel=INFO"]
