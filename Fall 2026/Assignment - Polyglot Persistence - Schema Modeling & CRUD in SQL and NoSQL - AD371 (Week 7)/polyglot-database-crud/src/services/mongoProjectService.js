import { randomUUID } from 'node:crypto';
import { mongoProjects } from '../database/mongo.js';

export async function createProject(input) {
  const project = { _id: randomUUID(), name: input.name, description: input.description ?? null, status: 'active', tasks: [], createdAt: new Date(), updatedAt: new Date() };
  await mongoProjects().insertOne(project);
  return project;
}
export async function getProject(id) { return mongoProjects().findOne({ _id: id }); }
export async function updateProject(id, input) { await mongoProjects().updateOne({ _id: id }, { $set: { name: input.name, description: input.description ?? null, updatedAt: new Date() } }); return getProject(id); }
export async function deleteProject(id) { return mongoProjects().deleteOne({ _id: id }); }
export async function addTask(projectId, input) {
  const task = { id: randomUUID(), title: input.title, description: input.description ?? null, status: 'todo', priority: input.priority ?? 'medium' };
  const result = await mongoProjects().updateOne({ _id: projectId }, { $push: { tasks: task }, $set: { updatedAt: new Date() } });
  if (!result.matchedCount) return null;
  return task;
}
export async function updateTask(projectId, taskId, input) { const result = await mongoProjects().updateOne({ _id: projectId, 'tasks.id': taskId }, { $set: { 'tasks.$.title': input.title, 'tasks.$.status': input.status, updatedAt: new Date() } }); return result.matchedCount > 0; }
export async function removeTask(projectId, taskId) { const result = await mongoProjects().updateOne({ _id: projectId }, { $pull: { tasks: { id: taskId } }, $set: { updatedAt: new Date() } }); return result.modifiedCount > 0; }
