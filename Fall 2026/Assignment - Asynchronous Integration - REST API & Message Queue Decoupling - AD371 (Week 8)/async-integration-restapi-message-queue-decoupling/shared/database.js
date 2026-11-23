import Database from "better-sqlite3";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const currentDirectory = path.dirname(fileURLToPath(import.meta.url));
const dataDirectory = path.join(currentDirectory, "..", "data");
fs.mkdirSync(dataDirectory, { recursive: true });

const database = new Database(path.join(dataDirectory, "jobs.db"));
database.pragma("journal_mode = WAL");
database.exec(`
  CREATE TABLE IF NOT EXISTS jobs (
    id TEXT PRIMARY KEY,
    report_name TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    started_at TEXT,
    completed_at TEXT,
    error_message TEXT
  )
`);

export default database;
