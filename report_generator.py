import streamlit as st
from google import genai
from google.genai import types

def generate_architectural_critique(node_name, structural_score, raw_code):
    """
    Leverages Gemini-2.5-Flash to synthesize localized, architectural advice
    based on custom topological graph measurements.
    """
    # Fix: Safely fetch the API key using Streamlit's secrets manager
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        return f"### {node_name} Audit\n*Error: GEMINI_API_KEY missing from Streamlit secrets config.*"

    client = genai.Client(api_key=api_key)
    
    prompt = f"""
    You are a Principal Software Architect. Analyze this architectural regression found in the codebase graph logic.
    
    ENTITY: {node_name}
    GRAPH CENTRALITY IMPACT: {structural_score:.4f} (High structural bottleneck)
    
    RAW ENTITY IMPLEMENTATION CODE:
    \"\"\"
    {raw_code}
    \"\"\"
    
    Provide a concise evaluation mapping:
    1. Architectural Impact of this structural coupling.
    2. Targeted Refactoring Recommendation to decouple this layout.
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.2)
        )
        return response.text
    except Exception as e:
        return f"Failed to generate LLM report for {node_name}: {str(e)}"