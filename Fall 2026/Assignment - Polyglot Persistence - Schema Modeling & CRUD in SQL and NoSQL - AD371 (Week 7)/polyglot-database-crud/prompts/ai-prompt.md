# Initial AI Prompt

Act as a senior database architect. I am designing a Project and Task Management System with two related entities: Projects and Tasks.

I need to implement polyglot persistence to compare relational and non-relational modeling.

Relational database: PostgreSQL. Create normalized 3NF tables with primary keys, foreign keys, timestamps, indexes, and appropriate cascade rules.

NoSQL database: MongoDB. Design an idiomatic document model for the same domain. Optimize for reading a complete project with its associated tasks in a single query by embedding tasks or using appropriate denormalization.

Working application: Node.js with Express. Use the pg library for PostgreSQL and the official MongoDB Node.js driver for MongoDB. Implement CRUD operations for projects and tasks, including create, read by ID, list, update, and delete.

Provide the initial project structure, PostgreSQL DDL, MongoDB sample document, database connection logic, routes, controllers, services, and a basic test script. Use parameterized SQL queries and explain any assumptions. This is an initial draft that will be audited for SQL referential integrity, NoSQL query-driven modeling, safe query handling, ID generation, and transaction boundaries.

Also explain how Docker Compose could run PostgreSQL and MongoDB together and how pgAdmin could be used to inspect PostgreSQL.
