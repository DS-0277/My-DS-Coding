# MongoDB Manual Test

## Connection

Start MongoDB:

```bash
docker compose up -d
```

Connect in MongoDB Compass with:

```text
mongodb://127.0.0.1:27017
```

Use database `polyglot` and collection `projects`.

## 1. Create a Project Document

In MongoDB Compass, select **Add Data → Insert Document**, paste this JSON, and click **Insert**:

```json
{
  "_id": "mongo-project-1",
  "name": "Mobile App Launch",
  "description": "Prepare and release the mobile application",
  "status": "active",
  "tasks": [
    {
      "id": "mongo-task-1",
      "title": "Design App Icon",
      "status": "todo",
      "priority": "high"
    },
    {
      "id": "mongo-task-2",
      "title": "Test Login Screen",
      "status": "todo",
      "priority": "medium"
    }
  ],
  "createdAt": "2026-11-14T00:00:00.000Z",
  "updatedAt": "2026-11-14T00:00:00.000Z"
}
```

## 2. Read the Document

Click **Find** or refresh the collection. Verify that the project contains both embedded tasks in the `tasks` array.

Expected result: one project document with two tasks.

## 3. Update an Embedded Task

Click the pencil/edit icon. In `tasks[0]`, change `status` from `todo` to `completed`. Save the document and verify that the second task remains `todo`.

## 4. Delete the Document

Click the trash icon, then click **Delete** in the confirmation dialog. Refresh or click **Find**.

Expected result: no documents remain in the collection.

## Result

- [x] Created a project with embedded tasks
- [x] Read the project and tasks in one document
- [x] Updated one embedded task
- [x] Deleted the project document and embedded tasks
