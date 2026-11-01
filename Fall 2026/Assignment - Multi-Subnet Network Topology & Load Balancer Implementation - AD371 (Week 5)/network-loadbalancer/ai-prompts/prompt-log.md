# AI Prompt Log — Step 1 Initial Draft

## Prompt used

Act as a senior network systems architect. I need a multi-container network topology configured using Docker Compose demonstrating isolated subnets and reverse-proxy load balancing for a web application.

The architecture must include a public_subnet accessible from the host, a private_subnet for backend services, a dual-homed Nginx load balancer exposing port 80, and at least two backend replicas connected only to the private subnet. Each backend must return a unique identifier and provide `/healthz`. Provide the Docker Compose file, Nginx configuration, minimal backend application, and run/test instructions.

## Initial-draft status

This is an unverified AI-style draft for Step 1. It must be audited before it is run.

## Issues intentionally recorded for Step 2 review

- The backend services publish host ports `3001` and `3002`.
- The private network is not yet marked `internal: true`.
- Nginx does not yet include explicit proxy timeouts or retry behavior.
- The health-check behavior needs to be verified against the assignment requirements.

## Step 2 audit results

### 1. Port leakage and network isolation — issue found and fixed

The initial draft published backend ports `3001:3000` and `3002:3000`. That created direct host-to-backend paths and allowed users to bypass Nginx. The mappings were removed. The backends still listen on internal port `3000` and use `expose` for container-to-container communication.

Result: the intended public entry point is now only Nginx on host port `80`.

### 2. Subnet dual-homing — issue found and fixed

The initial draft had the correct container memberships: Nginx was on both networks, while each backend was on the private network only. The private network was strengthened with `internal: true`.

Result: Nginx remains the only dual-homed service, and the backend network is explicitly internal.

### 3. Upstream configuration and DNS resolution — issue found and fixed

The initial draft correctly used Docker service names rather than static IP addresses, but it lacked explicit proxy timeout and retry behavior. Nginx now includes connection, read, and send timeouts plus `proxy_next_upstream` conditions.

Result: service-name discovery remains stable across container restarts, and Nginx can retry another backend after common upstream failures.

### 4. True load balancing and failover — verified in configuration

The upstream pool contains both `backend_1:3000` and `backend_2:3000`, so Nginx uses its default round-robin selection. The retry settings support passive failover when a backend connection fails. Live request distribution and stop/restart testing belong to Step 3.

Result: the configuration is ready for functional QA, but runtime behavior still must be demonstrated with live tests.
