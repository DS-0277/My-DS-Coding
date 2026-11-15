# Step 3 QA Checklist

## SQL

- [x] Create and read a project and related task
- [x] Update a task and verify the changed value
- [x] Delete a project and verify cascade deletion of its tasks
- [x] Reject a task with an invalid project foreign key

## MongoDB

- [x] Create and read a project with embedded tasks in one query
- [x] Atomically update an embedded task
- [x] Delete the project document and verify clean-up

## Test command

```text
npm run test:qa
```

Result: 6 tests passed, 0 failed.
