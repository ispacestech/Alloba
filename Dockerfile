FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md LICENSE ./
COPY src ./src

RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir .

# RAG index and knowledge docs are mounted at runtime (see docker-compose.yml).
ENV ALLOBA_RAG_INDEX_DIR=/app/rag_index
ENV ALLOBA_RAG_DOCS_DIR=/app/kb/docs
ENV ALLOBA_BACKEND_URL=http://host.docker.internal:8561
ENV ALLOBA_HOST=0.0.0.0
ENV ALLOBA_PORT=8582

EXPOSE 8582 8020

CMD ["uvicorn", "alloba.main:app", "--host", "0.0.0.0", "--port", "8582"]
