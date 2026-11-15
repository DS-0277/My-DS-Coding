import test, { after, before } from 'node:test';
import assert from 'node:assert/strict';
import { randomUUID } from 'node:crypto';
import { pool } from '../src/database/postgres.js';
import { mongoClient, mongoProjects } from '../src/database/mongo.js';

let projectId;
let taskId;

before(async () => {
  await mongoClient.connect();
  await mongoProjects().deleteMany({});
  await pool.query('TRUNCATE tasks, projects CASCADE');
});

test('SQL create and read project and task', async () => {
  projectId = randomUUID();
  taskId = randomUUID();
  await pool.query('INSERT INTO projects (id, name) VALUES ($1, $2)', [projectId, 'QA Project']);
  await pool.query('INSERT INTO tasks (id, project_id, title) VALUES ($1, $2, $3)', [taskId, projectId, 'QA Task']);
  const result = await pool.query('SELECT p.name AS project, t.title AS task FROM projects p JOIN tasks t ON t.project_id = p.id WHERE p.id = $1', [projectId]);
  assert.deepEqual(result.rows[0], { project: 'QA Project', task: 'QA Task' });
});

test('SQL update and invalid foreign key rejection', async () => {
  await pool.query('UPDATE tasks SET status = $1 WHERE id = $2', ['completed', taskId]);
  const updated = await pool.query('SELECT status FROM tasks WHERE id = $1', [taskId]);
  assert.equal(updated.rows[0].status, 'completed');
  await assert.rejects(pool.query('INSERT INTO tasks (id, project_id, title) VALUES ($1, $2, $3)', [randomUUID(), randomUUID(), 'Orphan']), /foreign key|violates/i);
});

test('SQL cascade deletes child tasks', async () => {
  await pool.query('DELETE FROM projects WHERE id = $1', [projectId]);
  const result = await pool.query('SELECT id FROM tasks WHERE id = $1', [taskId]);
  assert.equal(result.rowCount, 0);
});

test('MongoDB creates and reads an embedded project', async () => {
  const project = { _id: 'qa-project', name: 'Mongo QA', tasks: [{ id: 'qa-task', title: 'Embedded task', status: 'todo' }] };
  await mongoProjects().insertOne(project);
  const found = await mongoProjects().findOne({ _id: project._id });
  assert.equal(found.tasks[0].title, 'Embedded task');
});

test('MongoDB atomically updates an embedded task', async () => {
  const result = await mongoProjects().updateOne({ _id: 'qa-project', 'tasks.id': 'qa-task' }, { $set: { 'tasks.$.status': 'completed' } });
  assert.equal(result.modifiedCount, 1);
  const found = await mongoProjects().findOne({ _id: 'qa-project' });
  assert.equal(found.tasks[0].status, 'completed');
});

test('MongoDB deletes the project document cleanly', async () => {
  await mongoProjects().deleteOne({ _id: 'qa-project' });
  assert.equal(await mongoProjects().countDocuments({ _id: 'qa-project' }), 0);
});

after(async () => { await pool.end(); await mongoClient.close(); });
