import express from "express";
import crypto from "node:crypto";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { createJob, getJob } from "../shared/jobStore.js";
import { connectToRabbitMQ, QUEUE_NAME, setupQueues } from "../shared/rabbitmq.js";

const app = express();
const port = process.env.PORT || 3000;
const currentDirectory = path.dirname(fileURLToPath(import.meta.url));

app.use(express.json());
app.use(express.static(path.join(currentDirectory, "..", "public")));

let channel;

async function startServer() {
  const connection = await connectToRabbitMQ();
  channel = await connection.createChannel();

  await setupQueues(channel);

  app.post("/api/jobs", (request, response) => {
    const { reportName } = request.body;
    if (typeof reportName !== "string" || reportName.trim().length === 0) {
      return response.status(400).json({ error: "reportName is required." });
    }

    const id = crypto.randomUUID();
    const job = createJob(id, reportName.trim());
    const payload = Buffer.from(JSON.stringify({ id, reportName: job.reportName }));

    channel.sendToQueue(QUEUE_NAME, payload, { persistent: true });
    console.log(`[API] Published job ${id}: ${job.reportName}`);
    return response.status(202).json(job);
  });

  app.get("/api/jobs/:id", (request, response) => {
    const job = getJob(request.params.id);
    if (!job) return response.status(404).json({ error: "Job not found." });
    return response.json(job);
  });

  app.listen(port, () => {
    console.log(`[API] Running at http://localhost:${port}`);
  });
}

startServer().catch((error) => {
  console.error("[API] Could not connect to RabbitMQ:", error.message);
  process.exit(1);
});
