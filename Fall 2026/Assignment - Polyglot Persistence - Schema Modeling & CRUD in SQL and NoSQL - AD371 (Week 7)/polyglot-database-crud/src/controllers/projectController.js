import * as service from '../services/postgresProjectService.js';
import * as mongoService from '../services/mongoProjectService.js';

export async function createProject(req, res, next) {
  try { if (!req.body.name?.trim()) return res.status(400).json({ error: 'Project name is required' }); res.status(201).json(await service.createProject(req.body)); } catch (e) { next(e); }
}
export async function listProjects(req, res, next) {
  try { res.json(await service.listProjects()); } catch (e) { next(e); }
}
export async function getProject(req, res, next) {
  try {
    const project = await service.getProject(req.params.id);
    if (!project) return res.status(404).json({ error: 'Project not found' });
    res.json(project);
  } catch (e) { next(e); }
}
export async function updateProject(req, res, next) {
  try { res.json(await service.updateProject(req.params.id, req.body)); } catch (e) { next(e); }
}
export async function deleteProject(req, res, next) {
  try { if (!await service.deleteProject(req.params.id)) return res.status(404).json({ error: 'Project not found' }); res.status(204).end(); } catch (e) { next(e); }
}
export async function createTask(req, res, next) { try { if (!req.body.title?.trim()) return res.status(400).json({ error: 'Task title is required' }); res.status(201).json(await service.createTask(req.params.projectId, req.body)); } catch (e) { next(e); } }
export async function listTasks(req, res, next) { try { res.json(await service.listTasks(req.params.projectId)); } catch (e) { next(e); } }
export async function updateTask(req, res, next) { try { const task = await service.updateTask(req.params.id, req.body); if (!task) return res.status(404).json({ error: 'Task not found' }); res.json(task); } catch (e) { next(e); } }
export async function deleteTask(req, res, next) { try { if (!await service.deleteTask(req.params.id)) return res.status(404).json({ error: 'Task not found' }); res.status(204).end(); } catch (e) { next(e); } }
