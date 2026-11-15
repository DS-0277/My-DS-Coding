import { Router } from 'express';
import * as controller from '../controllers/projectController.js';

const router = Router();
router.post('/projects', controller.createProject);
router.get('/projects', controller.listProjects);
router.get('/projects/:id', controller.getProject);
router.patch('/projects/:id', controller.updateProject);
router.delete('/projects/:id', controller.deleteProject);
router.post('/projects/:projectId/tasks', controller.createTask);
router.get('/projects/:projectId/tasks', controller.listTasks);
router.patch('/tasks/:id', controller.updateTask);
router.delete('/tasks/:id', controller.deleteTask);
export default router;
