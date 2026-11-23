# AI Prompt Log

## Step 1: Initial Prompt

**AI tool used:** ChatGPT (Codex)

```text
Act as a senior Node.js distributed-systems developer. Create an initial learning-project draft for a local asynchronous report-generation application.

Use Node.js and Express for the REST API, RabbitMQ with amqplib as the external message broker, SQLite as a shared job-status store between the API and worker, plain HTML/CSS/JavaScript for a small dashboard, and Docker Compose to run RabbitMQ with its management dashboard enabled.

The application needs: POST /api/jobs that validates a required reportName string, creates a unique job ID, saves queued status, publishes to RabbitMQ, and immediately returns HTTP 202; GET /api/jobs/:id that returns the job status; a worker that processes each job with a five-second delay; and a dashboard that submits and polls jobs. Keep it beginner-friendly. This is an initial draft that will later be audited for ACK/NACK handling, persistence, idempotency, and crash recovery.
```

## Initial Draft Summary

The initial draft uses a real RabbitMQ broker, a separate Express API producer, a separate worker consumer, SQLite for shared job statuses, and a browser dashboard. The API returns `202 Accepted` after publishing a job.

## Step 2: Messaging Architecture Audit

The assignment requires these four checks. The status names make clear whether the initial AI draft needed a correction.

| Required audit item | Status | What the initial AI draft did | Result / change made |
| --- | --- | --- | --- |
| 1. True asynchronous decoupling vs. fake queue | **Good — no change** | It used an external RabbitMQ broker through `amqplib`, not a JavaScript array or a temporary background promise. | Kept RabbitMQ. The API and worker remain separate programs, so the API can accept work even when the worker is busy or stopped. |
| 2. Immediate `202 Accepted` response | **Good — no change** | `POST /api/jobs` saved the `queued` status, published the message, and returned `202` without waiting for the worker's five-second task. | Kept this flow. The client receives a job ID right away and polls `GET /api/jobs/:id` for progress. |
| 3. ACK / NACK mechanics | **Defect found — fixed** | The worker used `noAck: true`. RabbitMQ removed the message as soon as it delivered it to the worker. If the worker crashed during the five-second task, that job could be lost. | Changed to `noAck: false`. The worker now calls `channel.ack(message)` only after it updates the job to `completed`. It calls `channel.nack(message, false, true)` for a temporary failure so RabbitMQ requeues the job. |
| 4. Worker crash recovery and durability | **Defect found — fixed** | The queue used `durable: false` and messages were published without `{ persistent: true }`. A broker restart could remove the queue or discard waiting jobs. | Main queue, dead-letter queue, and dead-letter exchange now use `durable: true`. The API now publishes messages with `{ persistent: true }`, allowing RabbitMQ to preserve them across a broker restart. |

### Additional Reliability Improvements

These two additions support the four required checks and address risks named in the assignment overview.

| Improvement | Status | Previous risk | Correction made |
| --- | --- | --- | --- |
| Dead-Letter Queue (DLQ) | **Defect found — fixed** | A malformed JSON payload could continually fail and interfere with normal processing. | Invalid JSON is NACKed without requeueing and routed to the durable `report_jobs_dlq` for inspection. |
| Consumer idempotency | **Defect found — fixed** | A message can be redelivered after a crash. Without a check, an already-completed job could run twice. | Before processing, the worker checks SQLite. If the job is already `completed`, it ACKs and skips it. |

### Manual Audit Evidence

- `api/server.js` now declares queue topology with `setupQueues()` and publishes persistent messages.
- `worker/worker.js` uses manual acknowledgments: ACK follows a successful status update; NACK/requeue is used for transient failures.
- `shared/rabbitmq.js` defines the main durable queue and its dead-letter exchange/queue.

### Important Operational Note

RabbitMQ will reject a declaration if a queue already exists with different durable settings. Before testing the corrected version, stop the old broker and remove its old queue/data with `docker compose down -v`, then start the broker again. This is a local learning-project reset; do not do this in production because it deletes broker data.

## Live Demo Quick Reference

Use this section during the recording.

### Start RabbitMQ

```bash
docker compose up -d
```

### Start the API server

Run this in the first Terminal window:

```bash
npm run start:api
```

Expected log:

```text
[API] Running at http://localhost:3000
```

### Start the worker

Run this in a second Terminal window, in the same project folder:

```bash
npm run start:worker
```

Expected log:

```text
[WORKER] Waiting for report jobs...
```

### Open the app and RabbitMQ dashboard

| Item | Address / login |
| --- | --- |
| Job dashboard | `http://localhost:3000` |
| RabbitMQ Management | `http://localhost:15672` |
| RabbitMQ username | `guest` |
| RabbitMQ password | `guest` |

### Useful Demo Reminder

- For a normal job, keep both API and worker running.
- For the crash-recovery test, stop only the worker with `Ctrl + C`; keep the API and RabbitMQ running.
- In RabbitMQ Management, open **Queues and Streams** then `report_jobs`. Use it only to observe `Ready` and `Unacked` counts; do not delete messages manually.
