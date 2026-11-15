# Frontend Manual Test

## Start the Application

From the project folder, make sure the database containers are running:

```bash
docker compose up -d
```

Start the Express server:

```bash
npm start
```

Open the frontend in a browser:

```text
http://localhost:3000
```

## 1. Create a Project

1. Enter a project name.
2. Enter an optional description.
3. Click **Create Project**.

Expected result:

- A success message appears.
- The project ID is copied into the task form.
- A new project is inserted into PostgreSQL.
- The browser Network tab shows `201 Created`.

## 2. Create a Task

1. Confirm that the project ID is present.
2. Enter a task title.
3. Enter an optional description.
4. Click **Create Task**.

Expected result:

- A success message appears.
- The task is inserted into PostgreSQL.
- The browser Network tab shows `201 Created`.

## 3. Empty Input Validation

Submit the project form without a project name, then submit the task form without a task title.

Expected result:

- A clear validation message appears.
- The request is not sent for the empty required field.

## 4. Invalid Project ID

Enter a project ID that does not exist and submit a task.

Expected result:

- The request fails safely.
- The page shows an error message.
- PostgreSQL rejects the invalid foreign-key relationship.

## 5. Long Text

Enter a long project description or task description.

Expected result:

- Text wraps inside the form.
- No content is clipped.
- The page does not overflow horizontally.

## 6. Responsive Layout

1. Open browser Developer Tools.
2. Enable device or mobile view.
3. Check a narrow mobile width.

Expected result:

- Forms fit the screen.
- Fields remain readable.
- Buttons remain usable.
- Cards stack vertically.
- No horizontal scrolling is required.

## 7. Browser Network Check

In Developer Tools, open the **Network** tab and submit the forms.

Verify the requests show appropriate HTTP responses:

```text
201 Created  Successful project or task creation
400 Bad Request  Empty required input
```

The current frontend sends create requests to PostgreSQL through the Express API. MongoDB is tested separately with MongoDB Compass and the MongoDB manual test.

## Result

- [ ] Project creation works
- [ ] Task creation works
- [ ] Empty input is rejected
- [ ] Invalid project ID is handled safely
- [ ] Long text wraps correctly
- [ ] Mobile layout is usable
- [ ] Network responses are visible
