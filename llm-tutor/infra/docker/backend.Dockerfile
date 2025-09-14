FROM python:3.11-slim

WORKDIR /app
COPY backend /app
RUN pip install -U pip && pip install -e .
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
