# Step 2: Simple Container Audit

This file checks the four items required by the assignment. The Docker Compose
deployment has now been built and tested.

## 1. Multi-Stage Build and Layer Caching

**Result: Good.**

The Dockerfile has two parts:

- One part installs the application packages.
- The other part runs the application.

This keeps the final image smaller.

The dependency file is copied before the application code. This helps Docker
rebuild faster when only the code changes.

## 2. Non-Root User

**Result: Good.**

The Dockerfile creates a user named `appuser` and uses that user to run the
application.

This is safer than running the application as the powerful root user.

This was confirmed during testing. The running Gunicorn processes used UID
`1000`, not root.

## 3. Image Size and Starting Image

**Result: Good.**

The Dockerfile uses `python:3.12-slim` instead of a large Python image. This
helps keep the image smaller. The image built successfully at approximately
213 MB, so this item is accepted for this project.

## 4. Resource Limits and Health Checks

**Result: Good after testing.**

The Compose file includes:

- CPU and memory limits.
- A health check for `/healthz`.
- A restart rule.

The specific concern was the `deploy` section. Local Docker Compose did not
automatically use that section to create all the replicas we needed, so we used
an explicit scaling command.

For local scaling, we should use:

```bash
docker compose up -d --scale web=3
```

Testing confirmed that three web containers ran and became healthy. Testing
also confirmed the CPU limit, memory limit, health check, and restart rule on
the running containers.

## Simple Video Finding

The specific problem we found was:

> The Compose file lists replicas under `deploy`, but local Docker Compose may
> need an explicit scaling command. We corrected the run instructions to use
> `docker compose up -d --scale web=3` and will verify the result.

The other three items were also checked successfully.

## Final Audit Result

All four required audit areas have now been reviewed and tested successfully.
The application built, ran as a non-root user, returned healthy responses,
used resource limits, scaled to three replicas, and recovered after an
application process was terminated.
