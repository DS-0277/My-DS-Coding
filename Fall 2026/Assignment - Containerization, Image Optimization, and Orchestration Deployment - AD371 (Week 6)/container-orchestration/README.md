# Containerized Web Application

This is the initial draft for the containerization and orchestration assignment.
It is a small Flask web application intended to run in Docker Compose.

## Application endpoints

- `/` — landing page with runtime information.
- `/healthz` — health-check endpoint.
- `/runtime` — JSON runtime metadata.

## Initial run commands

```bash
cp .env.example .env
docker compose build
docker compose up -d
curl http://localhost:8080/healthz
curl http://localhost:8080/runtime
docker compose ps
docker compose logs -f
docker compose down
```

To start additional web replicas during the QA step:

```bash
docker compose up -d --scale web=3
```

## Architecture

The `web` service runs the Flask application. The `proxy` service exposes port
8080 on the host and forwards requests to the web service over the Compose
network. This allows the web service to be scaled without assigning the same
host port to every replica.

## Status

This is an initial AI-generated draft. The Dockerfile and Compose configuration
must be audited and verified in Step 2 before they are considered final.

## Step 3 QA Results

### 1. Image and build check

- Image built successfully as `container-orchestration-web:latest`.
- Reported image size: approximately 213 MB.
- Running Gunicorn processes used UID `1000`, not root.

### 2. Application and endpoint check

- The landing page returned `HTTP 200 OK`.
- `/healthz` returned `HTTP 200 OK` with `{"status":"healthy"}`.
- `/runtime` returned a container hostname and uptime.

### 3. Scaling and self-healing check

- The web service was scaled to three containers with:

  ```bash
  docker compose up -d --scale web=3
  ```

- All three web containers became healthy.
- Requests returned three different container hostnames, proving that the
  replicas were running.
- A web process was terminated inside one replica. Docker restarted the
  container, and it returned to a healthy state.

### 4. Browser and response check

- The browser-facing proxy returned successful responses for the landing page,
  `/healthz`, and `/runtime`.
- The landing page loaded its runtime data through the `/runtime` request.
