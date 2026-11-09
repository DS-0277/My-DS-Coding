# AI Prompt Log

## Initial draft prompt

Act as a senior DevOps and cloud infrastructure architect.

Create a beginner-friendly lightweight Python Flask web application that will
be containerized with Docker and orchestrated locally with Docker Compose.

The application must include:

1. A simple landing page.
2. A GET /healthz endpoint that returns HTTP 200 and a healthy JSON response.
3. A runtime metadata endpoint that displays the container hostname and
   application uptime.
4. Clear error handling.
5. A pinned Flask dependency version.

Generate the following project artifacts:

- Flask application source code.
- requirements.txt.
- A Dockerfile.
- docker-compose.yml.
- .dockerignore.
- .env.example.
- README.md.
- AI_PROMPTS.md.

The Dockerfile should attempt to include a lightweight pinned Python base
image, a multi-stage build, dependency installation separated from application
source copying for Docker layer caching, a non-root user, no unnecessary
package-manager cache files, a health check for /healthz, and a clear startup
command.

The Docker Compose file should attempt to include a web service, port mapping,
environment-file support, health checks, restart behavior, CPU and memory
limits, and configuration that supports scaling the web service to at least
three replicas.

Use a simple project structure and provide exact commands to build, start,
check, scale, inspect logs, and stop the deployment. Do not use Kubernetes,
Docker Swarm, external cloud services, or a database.

## Video Demonstration: Step 3 Only

### Item 1: Container image and build verification

```bash
cd ~/Desktop/container-orchestration
docker compose build
docker image ls container-orchestration-web
docker compose up -d --scale web=3
docker top container-orchestration-web-1 -eo user,pid,comm,args
```

Check and explain:

- The image builds successfully without errors.
- A non-blocking pip warning may appear during the temporary build stage.
- The image has the correct name and tag and is about 213 MB.
- The running process uses UID 1000 instead of root.

### Item 2: Functional and endpoint testing

```bash
curl -i http://localhost:8080/
curl -i http://localhost:8080/healthz
curl http://localhost:8080/runtime
```

Check and explain:

- The main page returns HTTP 200.
- `/healthz` returns a healthy response.
- `/runtime` shows the container hostname and uptime.

Also open `http://localhost:8080` in the browser and show the landing page.

### Item 3: Orchestration and resilience testing

```bash
docker compose ps web
for i in 1 2 3 4 5 6; do curl -s http://localhost:8080/runtime; echo; done
```

Check and explain:

- Three web containers are running.
- All three are healthy.
- Different hostnames show that different replicas are handling requests.

Choose one ID from `docker compose ps -q web`, then run:

```bash
docker exec CONTAINER_ID sh -c 'kill 1'
docker compose ps
```

Check that the container returns to a healthy state.

### Item 4: Browser console and health-check status

- Open `http://localhost:8080`.
- Open Developer Tools.
- Reload the page.
- Show successful requests in the Network tab.
- Show no uncaught errors in the Console tab.

### Finish

After the demonstration, stop the deployment:

```bash
docker compose down --remove-orphans
```
