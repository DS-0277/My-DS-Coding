# Semantic Document Search Engine & Empirical Retrieval Benchmarking

This project compares BM25 lexical retrieval with dense vector retrieval over technical documentation. It also evaluates fixed-size and structure-aware chunking strategies.

## Step 1 status

The repository layout and initial evaluation plan are being established first. Implementation and benchmarking will follow the assignment's remaining steps.

## Run the containerized demo

This project uses the assignment's Option B deployment: a Dockerized local demo.

Requirements:

- Docker Desktop with Compose support.

Start the dashboard:

```bash
docker compose up --build
```

Open [http://localhost:8001](http://localhost:8001) in a browser. The first dense-search request may download the local `all-MiniLM-L6-v2` model into the persistent Docker volume.

Stop the demo with:

```bash
docker compose down
```

Run the automated tests outside Docker with:

```bash
uv run pytest -v
```

