import { randomUUID } from 'node:crypto';
import { pool } from '../database/postgres.js';

export async function createProject(input) {
  const id = randomUUID();
  const result = await pool.query(
    'INSERT INTO projects (id, name, description) VALUES ($1, $2, $3) RETURNING *',
    [id, input.name, input.description ?? null]
  );
  return result.rows[0];
}
export async function listProjects() { return (await pool.query('SELECT * FROM projects ORDER BY created_at DESC')).rows; }
export async function getProject(id) { return (await pool.query('SELECT * FROM projects WHERE id = $1', [id])).rows[0] ?? null; }
export async function updateProject(id, input) {
  return (await pool.query('UPDATE projects SET name = $1, description = $2, updated_at = NOW() WHERE id = $3 RETURNING *', [input.name, input.description ?? null, id])).rows[0];
}
export async function deleteProject(id) { return (await pool.query('DELETE FROM projects WHERE id = $1 RETURNING id', [id])).rowCount > 0; }
export async function createTask(projectId, input) {
  const result = await pool.query('INSERT INTO tasks (id, project_id, title, description) VALUES ($1, $2, $3, $4) RETURNING *', [randomUUID(), projectId, input.title, input.description ?? null]);
  return result.rows[0];
}
export async function listTasks(projectId) { return (await pool.query('SELECT * FROM tasks WHERE project_id = $1 ORDER BY created_at', [projectId])).rows; }
export async function updateTask(id, input) { return (await pool.query('UPDATE tasks SET title = $1, status = COALESCE($2, status), updated_at = NOW() WHERE id = $3 RETURNING *', [input.title, input.status ?? null, id])).rows[0] ?? null; }
export async function deleteTask(id) { return (await pool.query('DELETE FROM tasks WHERE id = $1 RETURNING id', [id])).rowCount > 0; }
