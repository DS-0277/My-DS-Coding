# Tech Interview Prep - Appromixate Nearest Neighbor (ANN) Mechanics & Strategic Chunking Architecture - AD331 (Week 5)


**1. Objective:** Demonstrate technical mastery of vector retrieval systems and ingestion pipelines by: (1) Deconstructing the algorithmic mechanics of Approximate Nearest Neighbor (ANN) search, contrasting exact k-Nearest Neighbors (O(Nd) brute-force compute) with graph-based indexing (Hierarchical Navigable Small World / HNSW) and cluster-based indexing (Inverted File with Product Quantization / IVF-PQ); (2) Explaining the indexing trade-offs between memory footprint, index build time, throughput (QPS), and recall tuning parameters (e.g., M, efConstruction, and efSearch in HNSW); (3) Establishing a rigorous architectural framework for selecting optimal chunk sizes and splitting strategies across contrasting document typologies: dense technical/API documentation versus long-form narrative/case-law documents; (4) Designing advanced mitigation patterns (hierarchical parent-child retrieval, contextual prefixing, and hybrid sparse-dense reranking) to bridge the tension between retrieval precision and generation context.

**2. Files:**

- *Slides - Approximate Nearest (ANN) Mechanics & Strategic Chunking Architecture - Week 5 - AD331_Darasen.pptx*: The Week 5 slide deck covering ANN mechanics and strategic chunking architecture.
- *Slides - Approximate Nearest (ANN) Mechanics & Strategic Chunking Architecture - Week 5 - AD331_Darasen.pdf*: A PDF version of the Week 5 slide deck for convenient viewing.
- *Diagram - HNSW vs IVF-PQ Search Methods.png*: Compares graph-based HNSW search with cluster-based IVF-PQ search.
- *Diagram - ANN Speed Accuracy and Memory Trade-Off.png*: Shows the accuracy, speed, and memory trade-offs in ANN tuning.
- *Diagram - Strategic Document Chunking.png*: Illustrates chunking approaches for technical and narrative documents.
- *Diagram - Parent-Child Retrieval Architecture.png*: Explains parent-child retrieval for precise search and full-context answers.

**3. YouTube Link:** The explanation is provided via the youtube link as follows: 
