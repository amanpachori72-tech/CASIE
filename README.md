# Code-Architecture Semantic Integrity Evaluator (CASIE) 🚀

[![Streamlit App](https://static.streamlit.io/badge_svg.svg)](h[ttps://share.streamlit.io/](https://4yevmvfwpmo5yrx9aqgnw5.streamlit.app/)) [![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

CASIE is an advanced static code analysis and machine learning pipeline that parses entire Python repositories, builds a high-fidelity topological dependency graph, and utilizes LLM semantic reasoning to isolate and generate refactoring blueprints for structural architectural bottlenecks.

---

## 🌟 Key Features

- **Multi-Channel Ingestion:** Supports automated public GitHub repository cloning and local project folder `.zip` extractions directly through an isolated cloud sandbox.
- **AST Parsing Engine:** Leverages `tree-sitter` to compile high-fidelity Abstract Syntax Trees (AST) and extract fine-grained code structural entities (classes, methods, dependencies).
- **Semantic Code Embeddings:** Utilizes Hugging Face `CodeBERT` transformer layers to project semantic code characteristics into vector space.
- **Topological Network Mapping:** Construct global repository dependency networks using `NetworkX` and visualizes code coupling topologies using `Matplotlib`.
- **AI-Driven Refactoring Blueprints:** Isolates critical code smells via Network Centrality Metrics (Betweenness Centrality) and triggers the Google Gemini Flash API to generate production-grade refactoring critiquing layers.

---

## 🏗️ System Architecture & Data Flow

The platform executes code ingestion, graph tensor compilation, and semantic audit generation across 5 deterministic pipeline phases:

[User Input: GitHub URL / ZIP]
│
▼
[Sandboxed Ingestion Layer (Git/Zip)] ──> [Tree-Sitter AST Parsing]
│
▼
[NetworkX Graph Matrix Creation] <─── [CodeBERT Semantic Vector Mapping]
│
▼
[Betweenness Centrality Outlier Isolation]
│
▼
[Google Gemini Gen-AI Evaluation Engine] ──> [Interactive Metrics UI & Markdown Audit Export] 

---

## 🛠️ Tech Stack & Core Dependencies

- **Frontend/Dashboard:** Streamlit (Production Cloud Micro-container Container)
- **Graph Engineering:** NetworkX, Matplotlib
- **Machine Learning Core:** Hugging Face Transformers (`CodeBERT`), PyTorch (CPU-Optimized Runtime)
- **Language Parsing Engine:** Tree-Sitter, Tree-Sitter-Languages
- **Generative AI Core:** Google GenAI SDK (Gemini Core Configuration Framework)

---

## 🚀 Local Installation & Setup

To spin up a local instance of CASIE on your computer, follow these configuration stages:

### 1. Clone the Workspace & Initialize Environment
```bash
git clone [https://github.com/amanpachori72-tech/CASIE.git](https://github.com/amanpachori72-tech/CASIE.git)
cd CASIE
python -m venv casie_env
source casie_env/bin/activate  # On Windows use: casie_env\Scripts\activate