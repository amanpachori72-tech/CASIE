import streamlit as st
import networkx as nx
import os
import matplotlib.pyplot as plt
# Import logic from your other core files
from app import extract_code_structures, CodeEmbeddingEngine, build_repository_graph
from analytics import identify_architectural_bottlenecks
from report_generator import generate_architectural_critique

# 1. Page Configuration and Titles (Rendered Instantly)
st.set_page_config(page_title="CASIE Engine", layout="wide")
st.title("Code-Architecture Semantic Integrity Evaluator (CASIE)")
st.write("Topological Graph Analysis & AI-Driven Refactoring Pipeline")

st.markdown("---")

# 2. Interactive Input Controls (Rendered Instantly so the page never looks empty)
target_path = st.text_input("Enter local repository directory path to analyze:", value="./test_repo")
analyze_button = st.button("Run Global Structural Analysis")

# 3. Deferred Heavy Model Initialization (Wrapped in a loading layer)
if "embed_engine" not in st.session_state:
    with st.spinner("Initializing Deep Learning Core... Loading CodeBERT semantic layers from Hugging Face (This may take 2-3 minutes on the first run)..."):
        st.session_state.embed_engine = CodeEmbeddingEngine()
    st.success("🤖 CodeBERT Semantic Engine loaded successfully and cached in memory!")

# 4. Global Analysis Execution Workflow
if analyze_button:
    if os.path.exists(target_path):
        with st.spinner("Processing repository topology... Compiling static structures & generating mathematical graph tensors..."):
            
            # Step 1: Parse Directory Files
            all_structures = []
            for root, _, files in os.walk(target_path):
                for file in files:
                    if file.endswith(".py"):
                        structures = extract_code_structures(os.path.join(root, file), language="python")
                        # Add raw code block lookup references for the LLM step
                        all_structures.extend(structures)
            
            if not all_structures:
                st.error(f"Analysis halted: No valid Python code components extracted from path '{target_path}'. Check if the folder contains active .py files.")
            else:
                # Step 2 & 3: Compile Graph Network using cached model engine
                G = build_repository_graph(all_structures, st.session_state.embed_engine)
                
                # Step 4: Programmatic Bottleneck Filtering
                bottlenecks = identify_architectural_bottlenecks(G, top_n=2)
                
                # Render Metrics Dashboard Layout
                st.subheader("📊 Structural Topological Metrics")
                col1, col2 = st.columns(2)
                col1.metric("Total Extracted Components (Nodes)", G.number_of_nodes())
                col2.metric("Topological Dependencies (Edges)", G.number_of_edges())
                
                # --- VISUAL NETWORK GRAPH RENDERING LAYER ---
                st.markdown("---")
                st.subheader("🌐 Codebase Topological Network Map")
                
                # Create a fresh matplotlib figure object to prevent state bleeding
                fig, ax = plt.subplots(figsize=(8, 4))
                fig.patch.set_facecolor('#0e1117')  # Match Streamlit's dark theme background
                ax.set_facecolor('#0e1117')
                
                # Compute visual spring layout node coordinates
                pos = nx.spring_layout(G, seed=42)
                
                # Draw the network structural layers
                nx.draw_networkx_nodes(G, pos, ax=ax, node_color='#ff4b4b', node_size=500)
                nx.draw_networkx_edges(G, pos, ax=ax, edge_color='#ffffff', arrows=True, arrowsize=15)
                nx.draw_networkx_labels(G, pos, ax=ax, font_color='#ffffff', font_size=10, font_weight='bold')
                
                plt.axis('off') # Clean layout border removal
                st.pyplot(fig)  # Safely push the compiled matrix figure plot to the frontend
                # -------------------------------------------------
                
                st.markdown("---")
                st.subheader("⚠️ Top Architectural Bottlenecks Isolated via Betweenness Centrality")
                
                if not bottlenecks:
                    st.info("No major architectural outliers isolated in this codebase layout.")
                    full_report_text = f"# CASIE: Code-Architecture Semantic Integrity Report\nNo critical anomalies found."
                else:
                    # Initialize the report compiler markdown buffer string
                    full_report_text = f"""# CASIE: Code-Architecture Semantic Integrity Report
                     
**Target Directory Analyzed:** `{target_path}`
**Total Extracted Components (Nodes):** {G.number_of_nodes()}
**Topological Dependencies (Edges):** {G.number_of_edges()}

=====================================================================
"""
                    # Step 5: Iterative LLM Generation per structural outlier
                    for idx, item in enumerate(bottlenecks):
                        st.markdown(f"### Anomaly {idx+1}: `{item['name']}` (Structural Impact Score: `{item['score']:.4f}`)")
                        
                        # Match graph entry back to code block array
                        code_match = next((x["code"] for x in all_structures if x["name"] == item["name"]), "")
                        
                        with st.spinner(f"Querying generative architectural critique for {item['name']}..."):
                            report = generate_architectural_critique(item["name"], item["score"], code_match)
                            st.info(report)
                            
                            # Append the data directly to the markdown export string
                            full_report_text += f"""
## Anomaly {idx+1}: `{item['name']}`
* **Structural Centrality Score:** {item['score']:.4f}
* **Entity Type:** {item['type']}
* **Declaration Line:** {item['line']}

### Architectural Audit & Refactoring Blueprint:
{report}
---------------------------------------------------------------------
"""
                
                # Render the Actionable Export Button Layer
                st.markdown("---")
                st.subheader("💾 Export Architecture Audit")
                
                st.download_button(
                    label="Download Full Architecture Report (.md)",
                    data=full_report_text,
                    file_name="casie_architecture_report.md",
                    mime="text/markdown",
                    use_container_width=True
                )
    else:
        st.error(f"Provided path '{target_path}' does not exist. Please check the spelling or absolute path syntax.")