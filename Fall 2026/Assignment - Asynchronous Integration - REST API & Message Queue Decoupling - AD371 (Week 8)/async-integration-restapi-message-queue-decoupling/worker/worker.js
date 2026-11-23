import { connectToRabbitMQ, QUEUE_NAME, setupQueues } from "../shared/rabbitmq.js";
import { getJob, updateJobStatus } from "../shared/jobStore.js";

const wait = (milliseconds) => new Promise((resolve) => setTimeout(resolve, milliseconds));

async function startWorker() {
  const connection = await connectToRabbitMQ();
  const channel = await connection.createChannel();

  await setupQueues(channel);
  channel.prefetch(1);

  console.log("[WORKER] Waiting for report jobs...");
  channel.consume(QUEUE_NAME, async (message) => {
    if (!message) return;
    try {
      const job = JSON.parse(message.content.toString());
      const existingJob = getJob(job.id);

      // Idempotency: a redelivered message must not create a second completed job.
      if (!existingJob || existingJob.status === "completed") {
        console.log(`[WORKER] ACK duplicate or unknown job ${job.id}`);
        channel.ack(message);
        return;
      }

      console.log(`[WORKER] Processing ${job.id}: ${job.reportName}`);
      updateJobStatus(job.id, "processing");
      await wait(5000);
      updateJobStatus(job.id, "completed");
      channel.ack(message);
      console.log(`[WORKER] Completed and ACKed ${job.id}`);
    } catch (error) {
      if (error instanceof SyntaxError) {
        // Poison payload: reject it without requeueing so RabbitMQ routes it to the DLQ.
        console.error("[WORKER] NACK poison message to DLQ:", error.message);
        channel.nack(message, false, false);
      } else {
        // A temporary database/network failure can be retried after worker recovery.
        console.error("[WORKER] NACK and requeue transient failure:", error.message);
        channel.nack(message, false, true);
      }
    }
  }, { noAck: false });
}

startWorker().catch((error) => {
  console.error("[WORKER] Could not connect to RabbitMQ:", error.message);
  process.exit(1);
});
