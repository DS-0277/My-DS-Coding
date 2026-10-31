FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_PORT=8000

WORKDIR /app

COPY pyproject.toml uv.lock README.md ./
COPY src ./src
COPY corpus ./corpus
COPY data ./data

RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir \
        pydantic rank-bm25 sentence-transformers numpy pandas tiktoken streamlit pytest

EXPOSE 8000

CMD ["streamlit", "run", "src/app.py"]
