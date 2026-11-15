# Initial AI Response

This file records the initial implementation draft produced from `ai-prompt.md`. It is intentionally unaudited. Step 2 will inspect and correct it.

## Proposed structure

```text
src/
  server.js
  routes/projectRoutes.js
  controllers/projectController.js
  services/postgresProjectService.js
  services/mongoProjectService.js
  database/postgres.js
  database/mongo.js
sql/schema.sql
nosql/sample-project.json
tests/crud.test.js
docker-compose.yml
```

## PostgreSQL draft

```sql
CREATE TABLE projects (
  id UUID PRIMARY KEY,
  name VARCHAR(120) NOT NULL,
  description TEXT,
  status VARCHAR(20) NOT NULL DEFAULT 'active',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE tasks (
  id UUID PRIMARY KEY,
  project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  title VARCHAR(160) NOT NULL,
  description TEXT,
  status VARCHAR(20) NOT NULL DEFAULT 'todo',
  priority VARCHAR(20) NOT NULL DEFAULT 'medium',
  due_date DATE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX tasks_project_id_idx ON tasks(project_id);
```

## MongoDB draft

```json
{
  "_id": "project-1",
  "name": "Website Redesign",
  "description": "Update the company website",
  "status": "active",
  "tasks": [
    {
      "id": "task-101",
      "title": "Design homepage",
      "status": "todo",
      "priority": "high"
    }
  ],
  "createdAt": "2026-11-14T00:00:00.000Z",
  "updatedAt": "2026-11-14T00:00:00.000Z"
}
```

## Draft backend pseudocode

```js
router.post('/projects', projectController.createProject);
router.get('/projects/:id', projectController.getProject);
router.patch('/projects/:id', projectController.updateProject);
router.delete('/projects/:id', projectController.deleteProject);

export async function createProject(req, res, next) {
  try {
    const project = await projectService.createProject(req.body);
    res.status(201).json(project);
  } catch (error) {
    next(error);
  }
}

export async function getProject(id) {
  const result = await pool.query(
    'SELECT * FROM projects WHERE id = $1',
    [id]
  );
  return result.rows[0] ?? null;
}
```

The draft proposes equivalent MongoDB operations using `findOne`, `$set`, `$push`, and `deleteOne`. It also proposes Docker Compose services named `postgres` and `mongo`, with the Express application connecting to each by service name.

## Initial assumptions to audit

- UUID generation must be made explicit and safe.
- Project and task validation needs clearer rules.
- MongoDB update behavior must be atomic for embedded tasks.
- PostgreSQL transaction boundaries need to be documented for multi-step operations.
- Error responses and negative tests need to be added.
