# PostgreSQL Manual Test

## Start the Database

From the project folder, run:

```bash
docker compose up -d
```

## Connect with pgAdmin

In pgAdmin 4, right-click **Servers** and select **Register → Server**.

The server name is only a label. Use any name, such as `Polyglot PostgreSQL`.

In the **Connection** tab, enter:

```text
Host name/address: 127.0.0.1
Port:              55432
Maintenance DB:    polyglot
Username:          polyglot
Password:          polyglot
```

Open:

```text
Servers → Polyglot PostgreSQL → Databases → polyglot
```

Use **Tools → Query Tool**. Run each section separately and in order.

## 1. Reset the Rehearsal Tables

This removes previous test data while keeping the table structure.

```sql
TRUNCATE TABLE tasks, projects CASCADE;
```

## 2. Create a Project

```sql
INSERT INTO projects (id, name, description)
VALUES (
  '11111111-1111-1111-1111-111111111111',
  'Website Redesign',
  'Update the company website'
)
RETURNING *;
```

Expected result: one project is returned.

## 3. Create a Related Task

```sql
INSERT INTO tasks (id, project_id, title, description)
VALUES (
  '22222222-2222-2222-2222-222222222222',
  '11111111-1111-1111-1111-111111111111',
  'Design Homepage',
  'Create the new homepage layout'
)
RETURNING *;
```

Expected result: one task is returned with the project ID.

## 4. Read the Project and Task Together

```sql
SELECT
  p.name AS project_name,
  t.title AS task_title
FROM projects p
JOIN tasks t ON t.project_id = p.id;
```

Expected result: `Website Redesign | Design Homepage`.

## 5. Update the Task

```sql
UPDATE tasks
SET
  title = 'Design Responsive Homepage',
  status = 'in-progress',
  updated_at = NOW()
WHERE id = '22222222-2222-2222-2222-222222222222'
RETURNING *;
```

## 6. Verify the Update

```sql
SELECT
  p.name AS project_name,
  t.title AS task_title,
  t.status
FROM projects p
JOIN tasks t ON t.project_id = p.id;
```

Expected result: the task title is `Design Responsive Homepage` and its status is `in-progress`.

## 7. Delete the Project and Test Cascade Deletion

```sql
DELETE FROM projects
WHERE id = '11111111-1111-1111-1111-111111111111'
RETURNING *;
```

Then verify that the related task was deleted:

```sql
SELECT *
FROM tasks
WHERE id = '22222222-2222-2222-2222-222222222222';
```

Expected result: `0 rows`, because `ON DELETE CASCADE` removed the task.

## 8. Test an Invalid Foreign Key

This insert should fail because the project ID does not exist:

```sql
INSERT INTO tasks (id, project_id, title, description)
VALUES (
  '33333333-3333-3333-3333-333333333333',
  '00000000-0000-0000-0000-000000000000',
  'Orphan Task',
  'This insert should be rejected'
);
```

Expected result: a foreign-key constraint violation.

## 9. Confirm the Invalid Task Was Not Inserted

```sql
SELECT *
FROM tasks
WHERE id = '33333333-3333-3333-3333-333333333333';
```

Expected result: `0 rows`.

## Optional Cleanup

```sql
TRUNCATE TABLE tasks, projects CASCADE;
```
