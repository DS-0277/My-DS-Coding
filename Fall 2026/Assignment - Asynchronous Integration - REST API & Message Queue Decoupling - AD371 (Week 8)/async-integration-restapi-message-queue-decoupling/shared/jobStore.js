import database from "./database.js";

export function createJob(id, reportName) {
  const createdAt = new Date().toISOString();
  database.prepare(`
    INSERT INTO jobs (id, report_name, status, created_at)
    VALUES (?, ?, 'queued', ?)
  `).run(id, reportName, createdAt);
  return getJob(id);
}

export function getJob(id) {
  const job = database.prepare("SELECT * FROM jobs WHERE id = ?").get(id);
  if (!job) return null;
  return {
    id: job.id,
    reportName: job.report_name,
    status: job.status,
    createdAt: job.created_at,
    startedAt: job.started_at,
    completedAt: job.completed_at,
    errorMessage: job.error_message
  };
}

export function updateJobStatus(id, status, errorMessage = null) {
  const now = new Date().toISOString();
  if (status === "processing") {
    database.prepare("UPDATE jobs SET status = ?, started_at = ? WHERE id = ?").run(status, now, id);
  } else if (status === "completed") {
    database.prepare("UPDATE jobs SET status = ?, completed_at = ? WHERE id = ?").run(status, now, id);
  } else {
    database.prepare("UPDATE jobs SET status = ?, error_message = ? WHERE id = ?").run(status, errorMessage, id);
  }
  return getJob(id);
}
