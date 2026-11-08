FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml uv.lock README.md ./
COPY src ./src
COPY docs ./docs
COPY .streamlit ./.streamlit

RUN pip install --no-cache-dir uv \
    && uv sync --frozen --no-dev --no-install-project

EXPOSE 8500

CMD [".venv/bin/streamlit", "run", "src/app.py", "--server.address=0.0.0.0", "--server.port=8500"]

