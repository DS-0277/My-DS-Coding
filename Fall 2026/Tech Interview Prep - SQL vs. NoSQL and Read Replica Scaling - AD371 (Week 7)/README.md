# Tech Interview Prep - SQL vs. NoSQL and Read Replica Scaling - AD371 (Week 7)

**1. Objective:** In distributed systems and backend system design interviews, data architecture questions separate junior engineers who memorize acronyms from seniors who understand query patterns and physical data constraints. Two standard interview questions test this boundary: (1) "Can this candidate clearly explain the underlying data modeling and consistency trade-offs of relational vs. non-relational engines beyond just 'one uses tables and one uses JSON'?"; (2) "Does this candidate understand horizontal read scaling, and are they prepared to handle replication lag and eventual consistency bugs in production?"

**2. Files:**

- *Slides - Tech Interview Prep - SQL vs. NoSQL and Read Replica Scaling - Week 7 - AD371_Darasen.pptx*: The Week 7 slide deck covering SQL, NoSQL, and read replica scaling.
- *Slides - Tech Interview Prep - SQL vs. NoSQL and Read Replica Scaling - Week 7 - AD371_Darasen.pdf*: A PDF version of the Week 7 slide deck for convenient viewing.
- *Diagram - SQL vs NoSQL Data Organization.png*: Compares relational tables and relationships with flexible NoSQL document and key-value structures.
- *Diagram - ACID BASE and Scaling Trade-Offs.png*: Explains consistency models and the trade-offs between vertical and horizontal scaling.
- *Diagram - Read Replica Scaling.png*: Shows writes routed to a primary database and reads distributed across replicas.
- *Diagram - Replication Methods and Replication Lag.png*: Compares synchronous and asynchronous replication, including the risk of stale data.
- *Diagram - Preventing Stale Reads.png*: Shows sticky routing and replica-progress checks for maintaining read-after-write consistency.

**3. YouTube Link:** The explanation is provided via the youtube link as follows: https://youtu.be/FBssihioV_8
