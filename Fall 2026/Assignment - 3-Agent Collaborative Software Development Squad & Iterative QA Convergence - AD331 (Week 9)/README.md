# Assignment - 3-Agent Collaborative Software Development Squad & Iterative QA Convergence - AD331 (Week 9)

*1. Objective:* In enterprise agentic engineering, asking a single monolithic LLM to write, verify, and debug complex code leads to blind spots: models exhibit confirmation bias toward their own generated logic, hallucinate that non-existent tests pass, and overlook edge cases. Modern autonomous software development divides labor across specialized multi-agent squads governed by an orchestrator, strict communication contracts, and sandboxed test execution. In this assignment, you will engineer an autonomous 3-agent collaborative software development squad: (1) Product Spec Agent: Ingests user requirements, decomposes them into technical specifications, and formulates deterministic acceptance criteria and unit test plans; (2) Coder Agent: Reads the specification, writes clean, modular Python implementation code, and pairs it with matching test suites; (3) Reviewer/QA Agent: Executes the generated test suite in a sandboxed runtime, audits the code for logic bugs and security flaws, and either signs off (LGTM) or issues structured critique back to the Coder Agent. The squad executes in an iterative convergence loop—re-prompting and repairing code and tests until the test suite passes 100% or reaches a deterministic iteration bound.

*2. Source Files:* The source files to the assignment are stored in the GitHub repo: https://github.com/DS-0277/multi-agent-dev-squad

*3. YouTube Link:* The explanation is provided via the youtube link as follows: https://youtu.be/JeHmQ3FUaWM

*4. Deployment:* The deployment URL is available on: https://qwhpvjwny8v5wbfhmxep4q.streamlit.app/
