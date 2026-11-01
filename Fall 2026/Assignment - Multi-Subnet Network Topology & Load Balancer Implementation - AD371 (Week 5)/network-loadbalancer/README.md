# Multi-Subnet Network Topology & Load Balancer

This repository contains the Step 1 draft and Step 2 audited configuration for the AD371 Week 5 assignment.

## Current status

The configuration has completed the Step 2 networking and security audit. Runtime traffic, failover, and isolation tests belong to Step 3.

## Planned topology

```text
Client
  |
  v
public_subnet
  |
  v
Nginx load balancer
  |
  v
private_subnet
  |---------------- backend_1
  |---------------- backend_2
```

The initial draft and its known risks are documented in `ai-prompts/prompt-log.md`.

## Step 2 audit summary

- Backend host port leakage: fixed by removing host mappings for ports 3001 and 3002.
- Network isolation: strengthened with an internal private network; only Nginx is dual-homed.
- Upstream discovery: uses Docker service names and now includes proxy timeouts and retry behavior.
- Load balancing: both backends are in the round-robin upstream pool; live failover testing remains for Step 3.

## Step 3 QA results

The live QA test results are documented in `tests/qa-checklist.md`.

- Ten requests alternated between both backend IDs.
- Stopping `backend_1` routed requests to `backend_2` without `502` errors.
- Restarting `backend_1` returned it to the pool after Nginx's passive recovery window.
- Direct host requests to ports `3001` and `3002` were unreachable.
- The load balancer health endpoint returned `200 OK`.

## Step 3 presentation commands

Use these commands during the video walkthrough. Run them from this project folder.

### Item 1 — Load Distribution (Round-Robin)

#### Confirm the containers are running

```bash
docker compose ps
```

The load balancer, `backend_1`, and `backend_2` should show as running.

#### Send ten requests for the round-robin test

```bash
for i in $(seq 1 10); do
  printf "Request %s: " "$i"
  curl -s http://localhost/
  echo
done
```

Look for the `server_id` values `backend-1` and `backend-2` in the responses. The expected pattern is:

```text
backend-1, backend-2, backend-1, backend-2, backend-1,
backend-2, backend-1, backend-2, backend-1, backend-2
```

Suggested explanation:

> I am sending ten requests to the Nginx load balancer at `http://localhost`. I am not connecting directly to either backend. Each response shows the server ID, and the alternating IDs demonstrate round-robin load distribution.

### Item 2 — High Availability and Failover

#### Test failover after stopping Backend 1

Stop Backend 1 to simulate a server failure:

```bash
docker compose stop backend_1
```

Suggested explanation:

> I am stopping Backend 1 to simulate a backend server failure. The client will continue sending requests only to the Nginx load balancer.

Send five requests through Nginx:

```bash
for i in $(seq 1 5); do
  printf "Failover request %s: " "$i"
  curl -s http://localhost/
  echo
done
```

Expected result: all five responses show `backend-2`, with no `502 Bad Gateway` response.

Suggested explanation:

> Backend 1 is stopped, but the load balancer is still responding. All requests were routed to Backend 2, so failover is working.

Restart Backend 1:

```bash
docker compose start backend_1
```

Wait for Nginx's passive recovery window:

```bash
sleep 12
```

Verify that both backends are available again:

```bash
for i in $(seq 1 6); do
  printf "Recovery request %s: " "$i"
  curl -s http://localhost/
  echo
done
```

Expected result: the responses include both `backend-1` and `backend-2`.

### Item 3 — Network Isolation

Explain that this test checks whether a client can bypass Nginx and contact the backend containers directly.

First inspect the published ports:

```bash
docker compose ps
```

Only the load balancer should show a host port, `0.0.0.0:80->80/tcp`. The backends should show only their internal port, `3000/tcp`.

Test direct host access to the unsafe draft ports:

```bash
curl --connect-timeout 2 http://localhost:3001
curl --connect-timeout 2 http://localhost:3002
```

Both requests should be refused or unreachable. The equivalent browser demonstration is to open `http://localhost:3001` and `http://localhost:3002`; both should fail.

Compare with the intended public path:

```bash
curl http://localhost/
```

This request should succeed and return backend JSON because it goes through Nginx.

Suggested explanation:

> I tested the old direct host-port paths, and both failed because the backend ports are not published. The normal request to localhost succeeds through Nginx. This proves that the client cannot bypass the load balancer.

### Item 4 — Health Check and Browser Verification

Check the load balancer health endpoint:

```bash
curl -i http://localhost/healthz
```

Expected result: HTTP `200 OK` and the message `load-balancer healthy`.

Check a normal application request:

```bash
curl -i http://localhost/
```

Expected result: HTTP `200 OK` and JSON containing a `server_id` of `backend-1` or `backend-2`.

Suggested explanation:

> The load balancer health endpoint returned HTTP 200 OK, which confirms that Nginx is responding. The normal application request also returned HTTP 200 OK and identified the backend that handled it.

Optional browser verification:

1. Open `http://localhost/healthz` in a browser.
2. Open `http://localhost/` in a browser.
3. Open Developer Tools and select the Network tab.
4. Refresh the page and show a successful `200` request.
5. Show that the Console has no red client-side errors.

Suggested browser explanation:

> The browser received successful HTTP responses, and there are no client-side or gateway errors.
