# Assignment - Semantic Document Search Engine & Empirical Retrieval Benchmarking - AD331 (Week 5)


*1. Objective:* In enterprise search and Retrieval-Augmented Generation (RAG), engineers frequently assume that high-dimensional dense vector embeddings universally outperform traditional lexical keyword search. In reality, production search is governed by trade-offs: lexical matching (e.g., BM25) excels at exact identifier lookup, API parameters, and domain-specific acronyms, whereas semantic vector search (ANN) captures conceptual intent and paraphrasing at the cost of higher latency and index overhead. Furthermore, retrieval quality is heavily dependent on chunking strategy. Fixed-character chunking splits critical context across arbitrary token boundaries, whereas structure-aware or dynamic semantic chunking preserves antecedent references and cohesive units of technical thought. In this assignment, you will build an end-to-end semantic document search engine. You will ingest complex technical documentation, evaluate dynamic vs. fixed chunking strategies, generate dense vector embeddings, index them in an in-memory or embedded vector store, and construct an automated evaluation harness to benchmark retrieval recall, Hit Rate@K, and MRR (Mean Reciprocal Rank) against a BM25 lexical baseline.

*2. Source Files:* The source files to the assignment are stored in 'semantic-search-benchmarker' folder.

*3. YouTube Link:* The explanation is provided via the youtube link as follows: https://youtu.be/zF1nEH3TMoM
