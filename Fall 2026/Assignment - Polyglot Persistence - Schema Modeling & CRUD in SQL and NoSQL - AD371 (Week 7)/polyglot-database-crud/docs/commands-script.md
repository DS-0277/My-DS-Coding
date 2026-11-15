# Commands Script

## Commands to Run the Project

Run these commands from the project folder:

```bash
cd /Users/sendara/Desktop/polyglot-database-crud
npm install
docker compose up -d
npm run test:qa
```

Expected test result:

```text
6 tests passed
0 tests failed
```

To stop the database containers:

```bash
docker compose down
```

pgAdmin is optional. It can be used to inspect PostgreSQL tables and demonstrate the foreign key and cascade behavior.

