# Step 2: Database Reality Check

## 1. SQL Referential Integrity

**Status:** Passed

**Issue:** The original draft included a real foreign key using `REFERENCES projects(id)`, `ON DELETE CASCADE`, and an index on `tasks.project_id`. This prevents a task from pointing to a nonexistent project. Cascade deletion means deleting a project also deletes its tasks; this is an intentional design choice for this project.

**Correction:** No correction needed.

## 2. NoSQL Anti-Patterns

**Status:** Passed

**Issue:** The original draft embedded tasks inside project documents, allowing a complete project to be read with one query.

**Correction:** No correction needed.

## 3. SQL Injection & Parameterization

**Status:** Passed

**Issue:** The original SQL example used `$1` parameters instead of string concatenation.

**Correction:** No correction needed.

## 4. ID & Primary Key Generation

**Status:** Initially failed but fixed

**Issue:** The original draft declared UUID primary keys but did not define a generation strategy. Its MongoDB example also used a hard-coded string ID.

**Correction:** Added `randomUUID()` for application-side IDs and enabled PostgreSQL `pgcrypto` for database-side UUID generation.

**After correction:** Both database models have an explicit UUID generation strategy.
