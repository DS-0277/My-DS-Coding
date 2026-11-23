import amqp from "amqplib";

export const QUEUE_NAME = "report_jobs";
export const DEAD_LETTER_EXCHANGE = "report_jobs_dlx";
export const DEAD_LETTER_QUEUE = "report_jobs_dlq";
const rabbitUrl = process.env.RABBITMQ_URL || "amqp://localhost";

export async function connectToRabbitMQ() {
  return amqp.connect(rabbitUrl);
}

// Both the API and worker declare the same topology. RabbitMQ keeps the
// declarations idempotent: declaring an already-existing matching queue is safe.
export async function setupQueues(channel) {
  await channel.assertExchange(DEAD_LETTER_EXCHANGE, "direct", { durable: true });
  await channel.assertQueue(DEAD_LETTER_QUEUE, { durable: true });
  await channel.bindQueue(DEAD_LETTER_QUEUE, DEAD_LETTER_EXCHANGE, QUEUE_NAME);
  await channel.assertQueue(QUEUE_NAME, {
    durable: true,
    arguments: { "x-dead-letter-exchange": DEAD_LETTER_EXCHANGE }
  });
}
