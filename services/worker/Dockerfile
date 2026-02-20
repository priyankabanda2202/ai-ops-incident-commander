FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install redis ollama sentence-transformers numpy sqlalchemy

CMD ["python", "-m", "workers.incident_reasoner"]