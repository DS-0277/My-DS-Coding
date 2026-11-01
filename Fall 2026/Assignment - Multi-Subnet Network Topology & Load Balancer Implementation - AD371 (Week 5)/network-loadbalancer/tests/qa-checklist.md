# Step 3 QA Test Results

Date tested: 2026-11-01

The tests were run locally through the Nginx load balancer at `http://localhost`.

## 1. Load distribution

Result: PASS

Ten consecutive requests alternated between `backend-1` and `backend-2`:

```text
backend-1, backend-2, backend-1, backend-2, backend-1,
backend-2, backend-1, backend-2, backend-1, backend-2
```

## 2. High availability and failover

Result: PASS

After stopping `backend_1`, five consecutive requests were served by `backend-2` with no `502 Bad Gateway` responses. After restarting `backend_1` and allowing Nginx's passive recovery window to pass, requests again reached both backends.

## 3. Network boundary and isolation

Result: PASS

Direct requests to `http://localhost:3001` and `http://localhost:3002` were rejected or unreachable. The backend containers showed only the internal port `3000/tcp` and no published host ports.

## 4. Health and browser verification

Result: PASS

The load balancer health endpoint returned HTTP `200 OK` and the response `load-balancer healthy`. The normal load-balancer endpoint returned valid JSON with the backend server identifier.

## Commands used

```text
docker compose up -d --build
docker compose ps
curl http://localhost/healthz
curl http://localhost/
docker compose stop backend_1
docker compose start backend_1
docker compose down
```
