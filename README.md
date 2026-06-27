# Code-Architecture Semantic Integrity Evaluator (CASIE)

An advanced, graph-driven architectural audit engine that maps codebase topologies, programmatically isolates structural bottlenecks using network centrality mathematics, and generates automated refactoring blueprints via large language models.

---

## 🏗️ Core System Architecture

CASIE decouples architectural evaluation from standard static analysis metrics by mapping code relationships into a multidimensional topological graph:

1. **AST Syntactic Parsing:** Utilizes `tree-sitter` to parse multi-language source files into concrete abstract syntax trees, identifying core entities (functions/classes) and call-graph dependencies.
2. **Semantic Code Embeddings:** Converts raw code snippets into dense 768-dimensional vector tensors using a deep-learning `CodeBERT` layer to track structural intent.
3. **Directed Graph Compilation:** Assembles code units into a mathematical network graph using `NetworkX` (Nodes = Code Entities, Edges = Execution Dependencies).
4. **Topological Centrality Analytics:** Evaluates network traffic bottlenecks by programmatically computing **Betweenness Centrality** metrics to catch highly-coupled architectural anomalies.
5. **Generative LLM Audit:** Passes structural bottleneck metrics and raw logic to the `Gemini-2.5-Flash` engine to compile automated refactoring blueprints.

---

## 📊 Dashboard Visualizations & Capabilities

* **Structural Metrics Grid:** Real-time extraction tracking of absolute repository Node and Edge totals.
* **Topological Network Map:** Live visual mapping of codebase execution streams rendered directly through Matplotlib spring layouts.
* **Automated Audit Exporter:** One-click compiling of metric graphs and AI critique blocks into downloadable local Markdown logs.

---

## 🚀 Local Quickstart Setup

### Prerequisites
* Python 3.10 or higher
* A valid Gemini API Key (Generated free at [Google AI Studio](https://aistudio.google.com/))

### 1. Environment Installation
Clone the repository to your local directory machine and initialize your isolated virtual dependency tracking frame:
```bash
# Clone the repository
git clone [https://github.com/YOUR_USERNAME/CASIE.git](https://github.com/YOUR_USERNAME/CASIE.git)
cd CASIE

# Initialize and activate virtual environment
python -m venv casie_env
source casie_env/bin/activate  # On Linux/macOS
.\casie_env\Scripts\activate   # On Windows PowerShell

# Install required manifest packages
pip install -r requirements.txt