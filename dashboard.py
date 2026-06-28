import streamlit as st
import networkx as nx
import os
import shutil
import zipfile
import subprocess
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

# 2. Unified Ingestion Layer (Supports Remote GitHub Links & Local Zip Uploads)
st.subheader("📁 Provide Codebase for Analysis")

upload_method = st.radio(
    "Choose how you want to provide the source code:",
    ["GitHub Repository URL", "Upload Local Project Folder (.zip)"],
    horizontal=True
)

# Initialize container variables in session state to handle page refreshes correctly
if "target_path" not in st.session_state:
    st.session_state.target_path = None
if "processing_ready" not in st.session_state:
    st.session_state.processing_ready = False

if upload_method == "GitHub Repository URL":
    repo_url = st.text_input(
        "Enter public GitHub Repository URL:", 
        placeholder="https://github.com/username/repository"
    )
    if repo_url:
        st.session_state.target_path = "./cloned_user_repo"
        if st.button("Download and Prepare Repository", use_container_width=True):
            if os.path.exists(st.session_state.target_path):
                shutil.rmtree(st.session_state.target_path)
            
            with st.spinner("Executing Git tracking layer... cloning source files from GitHub..."):
                try:
                    # Execute clone without creating sub-commit loops
                    result = subprocess.run(
                        ["git", "clone", repo_url, st.session_state.target_path], 
                        check=True, capture_output=True
                    )
                    st.success("✨ Repository cloned successfully into cloud workspace sandbox!")
                    st.session_state.processing_ready = True
                except subprocess.CalledProcessError as e:
                    st.error(f"Failed to clone repository. Ensure the URL is public. Error: {e.stderr.decode()}")
                    st.session_state.target_path = None
                    st.session_state.processing_ready = False

else:
    uploaded_zip = st.file_uploader("Upload local project codebase compressed as a .zip file:", type=["zip"])
    if uploaded_zip:
        st.session_state.target_path = "./extracted_user_code"
        if st.button("Extract and Prepare Files", use_container_width=True):
            if os.path.exists(st.session_state.target_path):
                shutil.rmtree(st.session_state.target_path)
                
            with st.spinner("Decompressing code architecture map structures..."):
                try:
                    os.makedirs(st.session_state.target_path, exist_ok=True)
                    with zipfile.ZipFile(uploaded_zip, "r") as zip_ref:
                        zip_ref.extractall(st.session_state.target_path)
                    st.success("✨ Local codebase extracted successfully into cloud workspace sandbox!")
                    st.session_state.processing_ready = True
                except Exception as e:
                    st.error(f"Failed to unzip archive layout. Error: {str(e)}")
                    st.session_state.target_path = None
                    st.session_state.processing_ready = False

st.markdown("---")

# Assign standard script runtime execution tracking variable
# Assign standard script runtime execution tracking variable
target_path = st.session_state.target_path