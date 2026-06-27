import os
import torch
from tree_sitter_languages import get_parser
from transformers import AutoTokenizer, AutoModel
import networkx as nx
import matplotlib.pyplot as plt

# =====================================================================
# STAGE 1: MULTI-LANGUAGE PARSING VIA TREE-SITTER
# =====================================================================
def extract_code_structures(file_path, language="python"):
    """
    Parses any source file using Tree-Sitter and extracts structural blocks
    (functions, classes) along with their raw text bodies.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        source_code = f.read()

    parser = get_parser(language)
    tree = parser.parse(bytes(source_code, "utf8"))
    root_node = tree.root_node

    structures = []

    # Recursive function to traverse the Concrete Syntax Tree (CST)
    def traverse(node):
        # Identify function or method definitions across languages
        if node.type in ["function_definition", "method_definition"]:
            # Extract raw string from bytes matching the node position
            start_byte = node.start_byte
            end_byte = node.end_byte
            raw_text = source_code[start_byte:end_byte]
            
            # Simple fallback to get name; a full production system queries identifiers
            name = f"func_{node.start_point[0]}" 
            
            structures.append({
                "name": name,
                "type": "function",
                "code": raw_text,
                "line": node.start_point[0]
            })
            
        for child in node.children:
            traverse(child)

    traverse(root_node)
    return structures

# =====================================================================
# STAGE 2: SEMANTIC EMBEDDINGS VIA HUGGING FACE (CodeBERT)
# =====================================================================
class CodeEmbeddingEngine:
    def __init__(self, model_name="microsoft/codebert-base"):
        print(f"Loading deep learning model: {model_name}...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        
    def generate_embedding(self, code_text):
        """
        Passes raw code blocks through CodeBERT to extract a 768-dimensional
        vector representing its semantic logic.
        """
        inputs = self.tokenizer(code_text, return_tensors="pt", truncation=True, max_length=512)
        with torch.no_grad():
            outputs = self.model(**inputs)
        # Extract mean pooled vector representation
        embedding = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
        return embedding

# =====================================================================
# STAGE 3: TOPOLOGICAL GRAPH COMPILATION
# =====================================================================
def build_repository_graph(structures, embedding_engine):
    """
    Compiles entities into a network map where nodes represent functions
    and hold their deep learning semantic vectors.
    """
    G = nx.DiGraph()

    # Step A: Add nodes with their mathematical features
    for idx, item in enumerate(structures):
        print(f"Processing node {idx}: Generating semantic vector...")
        vector = embedding_engine.generate_embedding(item["code"])
        
        G.add_node(
            item["name"],
            type=item["type"],
            line=item["line"],
            embedding=vector  # This holds the 768-dim semantic array
        )

    # Step B: Establish Topological Edges
    # (In production, you'll map function calls; here we map consecutive execution sequence)
    node_list = list(G.nodes)
    for i in range(len(node_list) - 1):
        G.add_edge(node_list[i], node_list[i+1], relation="execution_sequence")

    return G

# =====================================================================
# EXECUTION ENTRY POINT
# =====================================================================
if __name__ == "__main__":
    # 1. Create a dummy test file simulating a repository file
    test_file = "demo_repo_file.py"
    with open(test_file, "w") as f:
        f.write("def calculate_total(price, tax):\n    return price + tax\n\n"
                "def process_payment(user_id, amount):\n    print('Charging user')\n    return True")

    try:
        # Step 1: Run Static Analysis Parse
        print("Executing Stage 1: Parsing Abstract Syntax Logic...")
        extracted_blocks = extract_code_structures(test_file, language="python")
        print(f"Successfully extracted {len(extracted_blocks)} discrete components.")

        # Step 2 & 3: Run Model Embeddings and Graph Construction
        embed_engine = CodeEmbeddingEngine()
        print("\nExecuting Stage 2 & 3: Multi-Dimensional Graph Compiling...")
        code_graph = build_repository_graph(extracted_blocks, embed_engine)

        # Print out the graph state to prove successful matrix loading
        print("\n=== SYSTEM GRAPH STATUS ===")
        print(f"Total Nodes Processed: {code_graph.number_of_nodes()}")
        print(f"Total Edges Defined: {code_graph.number_of_edges()}")
        
        for node in code_graph.nodes(data=True):
            print(f"\nNode: {node[0]}")
            print(f" -> Type: {node[1]['type']}")
            print(f" -> Tensor Vector Shape: {node[1]['embedding'].shape}")

        # Clean up the dummy file
        os.remove(test_file)

    except Exception as e:
        print(f"Execution failed: {str(e)}")
        if os.path.exists(test_file):
            os.remove(test_file)