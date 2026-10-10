FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN pip install uv

RUN uv sync --frozen

COPY . .

EXPOSE 8501

CMD ["uv", "run", "streamlit", "run", "src/app.py", "--server.address=0.0.0.0"]