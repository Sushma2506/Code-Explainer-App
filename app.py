"""
Code Analyzer - AI-Powered Code Insights & Suggestions
A Streamlit application that analyzes code and provides:
- Overview of what the code does
- Line-by-line explanations
- Suggestions for improvement
"""

import streamlit as st
import google.generativeai as genai
import json
import os
from typing import List, Dict, Any

# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="Code Analyzer - AI-Powered Insights",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CUSTOM CSS FOR PREMIUM STYLING
# ============================================
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Fira+Code:wght@400;500&display=swap');
    
    /* Force dark mode */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%) !important;
    }
    
    [data-testid="stHeader"] {
        background: transparent !important;
    }
    
    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%) !important;
        font-family: 'Inter', sans-serif;
        color: #e0e0ff;
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
    }
    
    .tagline {
        text-align: center;
        color: #a0a0c0;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Fix text color throughout */
    p, span, div, label {
        color: #e0e0ff !important;
    }
    
    /* Code input styling - CRITICAL FIX */
    .stTextArea textarea {
        font-family: 'Fira Code', monospace !important;
        background-color: rgba(30, 30, 50, 0.8) !important;
        border: 2px solid rgba(102, 126, 234, 0.4) !important;
        border-radius: 12px !important;
        color: #e0e0ff !important;
        font-size: 14px !important;
        min-height: 300px !important;
        padding: 1rem !important;
    }
    
    .stTextArea textarea::placeholder {
        color: #7070a0 !important;
        opacity: 1 !important;
    }
    
    .stTextArea textarea:focus {
        border-color: rgba(102, 126, 234, 0.8) !important;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2) !important;
    }
    
    /* Select box styling */
    .stSelectbox label {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }
    
    /* Main select container - force dark background */
    div[data-baseweb="select"] {
        background-color: rgba(30, 30, 50, 0.9) !important;
    }
    
    div[data-baseweb="select"] > div {
        background-color: rgba(30, 30, 50, 0.9) !important;
        border: 2px solid rgba(102, 126, 234, 0.5) !important;
        border-radius: 8px !important;
    }
    
    div[data-baseweb="select"] div {
        color: #ffffff !important;
        background-color: transparent !important;
    }
    
    div[data-baseweb="select"] span {
        color: #ffffff !important;
    }
    
    /* Force text color in select value */
    div[data-baseweb="select"] input {
        color: #ffffff !important;
    }
    
    /* ===== AGGRESSIVE DROPDOWN MENU STYLING ===== */
    /* Target the exact popover content */
    div[data-baseweb="popover"],
    div[data-baseweb="menu"],
    ul[role="listbox"] {
        background-color: #0f0f23 !important;
        border: 2px solid rgba(102, 126, 234, 0.4) !important;
    }

    /* Force background on the specific list container */
    ul[data-baseweb="menu"] {
        background-color: #0f0f23 !important;
    }

    /* Override any light theme defaults */
    .stSelectbox div[data-baseweb="select"] > div:first-child {
        background-color: rgba(30, 30, 50, 0.9) !important;
        color: white !important;
        border-color: rgba(102, 126, 234, 0.5) !important;
    }

    /* OPTIONS STYLING */
    li[role="option"] {
        background-color: #0f0f23 !important;
        color: white !important;
    }

    /* Text inside options */
    li[role="option"] div, 
    li[role="option"] span {
        color: white !important;
    }

    /* Hover state */
    li[role="option"]:hover {
        background-color: rgba(102, 126, 234, 0.4) !important;
    }

    /* Selected state */
    li[role="option"][aria-selected="true"] {
        background-color: rgba(102, 126, 234, 0.6) !important;
    }
    
    /* Result cards */
    .result-card {
        background: rgba(30, 30, 50, 0.6) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
    }
    
    .card-header {
        font-size: 1.3rem;
        font-weight: 600;
        color: #667eea !important;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Line-by-line styling */
    .line-item {
        background: rgba(40, 40, 70, 0.4);
        border-left: 3px solid #667eea;
        padding: 1rem;
        margin: 0.8rem 0;
        border-radius: 8px;
    }
    
    .line-number {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 0.8rem;
    }
    
    .line-code {
        font-family: 'Fira Code', monospace;
        background: rgba(0, 0, 0, 0.5);
        padding: 0.6rem;
        border-radius: 6px;
        display: block;
        margin: 0.5rem 0;
        color: #a8e6cf !important;
        font-size: 0.9rem;
        overflow-x: auto;
    }
    
    .line-explanation {
        color: #d0d0e0 !important;
        line-height: 1.6;
        margin-top: 0.5rem;
    }
    
    /* Suggestion cards */
    .suggestion-item {
        background: rgba(102, 126, 234, 0.15);
        border-left: 4px solid #667eea;
        padding: 1.2rem;
        margin: 1rem 0;
        border-radius: 8px;
    }
    
    .suggestion-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #a8e6cf !important;
        margin-bottom: 0.5rem;
    }
    
    .suggestion-description {
        color: #d0d0e0 !important;
        line-height: 1.6;
        margin-bottom: 0.8rem;
    }
    
    .suggestion-example {
        font-family: 'Fira Code', monospace;
        background: rgba(0, 0, 0, 0.6);
        padding: 1rem;
        border-radius: 6px;
        display: block;
        color: #a8e6cf !important;
        font-size: 0.85rem;
        white-space: pre-wrap;
        overflow-x: auto;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.8rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1.1rem;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #050510 !important;
        border-right: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    /* Sidebar Input Styling */
    [data-testid="stSidebar"] input {
        background-color: rgba(30, 30, 50, 0.8) !important;
        color: white !important;
        border: 1px solid rgba(102, 126, 234, 0.4) !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Divider styling */
    hr {
        border-color: rgba(102, 126, 234, 0.3) !important;
        margin: 2rem 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# GEMINI API INTEGRATION
# ============================================

def get_gemini_analysis(code: str, language: str, api_key: str) -> Dict[str, Any]:
    """
    Analyze code using Google Gemini API.
    Returns a dictionary with overview, line_by_line, and suggestions.
    """
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Analyze the following {language} code and provide a response in JSON format.
        
        The JSON structure should be:
        {{
            "overview": "A brief summary of what the code does.",
            "line_by_line": [
                {{
                    "line_number": 1,
                    "code": "code snippet",
                    "explanation": "Explanation of this specific line."
                }}
            ],
            "suggestions": [
                {{
                    "title": "Suggestion Title",
                    "description": "Why this suggestion helps.",
                    "example": "Code example of the improvement."
                }}
            ]
        }}
        
        Rules:
        1. "line_by_line" should only include meaningful lines (skip empty lines or just brackets if they don't add context).
        2. Provide at most 3 top "suggestions" for improvement. If code is perfect, suggest best practices or tests.
        3. Ensure the response is VALID JSON. Do not include markdown formatting like ```json ... ```.
        
        Code to analyze:
        {code}
        """
        
        response = model.generate_content(prompt)
        text_response = response.text
        
        # Clean up markdown if present
        if text_response.startswith("```json"):
            text_response = text_response.replace("```json", "").replace("```", "")
        
        return json.loads(text_response)
        
    except Exception as e:
        return {"error": str(e)}

# ============================================
# STREAMLIT UI
# ============================================

# Sidebar for API Key
with st.sidebar:
    st.markdown("### 🔑 API Configuration")
    api_key = st.text_input("Enter Google Gemini API Key", type="password", help="Get your key from https://aistudio.google.com/")
    if not api_key:
        st.warning("⚠️ API Key is required for analysis.")
    st.markdown("---")
    st.markdown("### About")
    st.markdown("This tool uses **Gemini 1.5 Flash** to analyze your code structure, explain logic, and suggest improvements.")

# Header
st.markdown('<h1 class="main-header">⚡ Code Analyzer</h1>', unsafe_allow_html=True)
st.markdown('<p class="tagline">AI-Powered Code Insights & Suggestions</p>', unsafe_allow_html=True)

# Language selector
col1, col2 = st.columns([3, 1])
with col2:
    language = st.selectbox(
        "Language",
        ["javascript", "python", "java", "cpp", "csharp", "go", "rust", "typescript", "other"],
        index=0
    )

# Code input
st.markdown("### 📝 Paste Your Code")
code_input = st.text_area(
    "Code",
    placeholder="// Paste or type your code here...\\nfunction example() {\\n    return 'Hello, World!';\\n}",
    height=300,
    label_visibility="collapsed"
)

# Analyze button
if st.button("🔍 Analyze Code", use_container_width=True):
    if not api_key:
        st.error("❌ Please enter your Google Gemini API Key in the sidebar to proceed.")
    elif code_input.strip():
        with st.spinner("🤖 AI is analyzing your code..."):
            
            # Fetch analysis from Gemini
            analysis = get_gemini_analysis(code_input, language, api_key)
            
            if "error" in analysis:
                st.error(f"❌ Analysis Failed: {analysis['error']}")
            else:
                st.markdown("---")
                
                # Overview Section
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.markdown('<div class="card-header">📄 What This Code Does</div>', unsafe_allow_html=True)
                st.markdown(f'<p style="color: #d0d0e0; line-height: 1.6;">{analysis.get("overview", "No overview available.")}</p>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Line-by-Line Section
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.markdown('<div class="card-header">📋 Line-by-Line Explanation</div>', unsafe_allow_html=True)
                
                line_items = analysis.get("line_by_line", [])
                if line_items:
                    for item in line_items:
                        st.markdown(f'''
                        <div class="line-item">
                            <span class="line-number">Line {item.get('line_number', '-')}</span>
                            <code class="line-code">{item.get('code', '')}</code>
                            <p class="line-explanation">{item.get('explanation', '')}</p>
                        </div>
                        ''', unsafe_allow_html=True)
                else:
                    st.markdown('<p style="color: #a0a0c0;">No detailed explanation returned.</p>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Suggestions Section
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.markdown('<div class="card-header">💡 Suggestions to Improve</div>', unsafe_allow_html=True)
                
                suggestions = analysis.get("suggestions", [])
                if suggestions:
                    for suggestion in suggestions:
                        example_html = f'<code class="suggestion-example">{suggestion.get("example", "")}</code>' if suggestion.get('example') else ''
                        st.markdown(f'''
                        <div class="suggestion-item">
                            <div class="suggestion-title">{suggestion.get('title', 'Suggestion')}</div>
                            <p class="suggestion-description">{suggestion.get('description', '')}</p>
                            {example_html}
                        </div>
                        ''', unsafe_allow_html=True)
                else:
                    st.markdown('<p style="color: #a0a0c0;">No suggestions found.</p>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("⚠️ Please enter some code to analyze!")

# Footer
st.markdown("---")
st.markdown('<p style="text-align: center; color: #a0a0c0; margin-top: 2rem;">Built with ❤️ using Gemini 1.5 Flash</p>', unsafe_allow_html=True)
