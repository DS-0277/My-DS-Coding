# Assignment - Resilient Unstructured Data Extraction & Pydantic Validation Pipelines - AD331 (Week 4)


*1. Objective:* In enterprise data engineering, downstream relational databases, ERPs, and automated accounting workflows cannot consume unstructured natural language or raw PDF scans directly. They demand strongly typed, validated records with deterministic constraints. While LLMs excel at semantic pattern matching across unstructured documents (e.g., invoices, clinical trial reports, legal disclosures, or web scrapes), they frequently hallucinate fields, omit required keys, or emit malformed types. In this assignment, you will engineer a production-ready, fault-tolerant data extraction pipeline. Your application will ingest complex, messy PDFs or raw HTML strings, extract multi-entity records directly into strictly typed Pydantic v2 models using grammar-constrained decoding, and execute a self-correcting reflection loop with dead-letter queue (DLQ) fallback mechanisms when validation fails.

*2. Source Files:* The source files to the assignment are stored in 'structured-data-extractor' folder.

*3. YouTube Link:* The explanation is provided via the youtube link as follows: https://youtu.be/RB937xvdqDc
