"""
Code Analyzer - AI-Powered Code Insights & Suggestions
A Streamlit application that analyzes code and provides:
- Overview of what the code does
- Line-by-line explanations
- Suggestions for improvement
"""

import streamlit as st
import re
from typing import List, Dict, Any

# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="Code Analyzer - AI-Powered Insights",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
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
# ANALYSIS FUNCTIONS
# ============================================

def detect_code_purpose(code: str) -> str:
    """Detect the purpose of the code based on keywords."""
    purposes = [
        (['fetch', 'axios', 'http', 'api', 'request'], 'performing HTTP requests or API calls'),
        (['addEventListener', 'onClick', 'DOM', 'document'], 'handling DOM manipulation and events'),
        (['useState', 'useEffect', 'component'], 'building a React component'),
        (['class', 'constructor', 'extends'], 'implementing object-oriented programming concepts'),
        (['async', 'await', 'Promise'], 'handling asynchronous operations'),
        (['map', 'filter', 'reduce'], 'performing array transformations'),
    ]
    
    for keywords, purpose in purposes:
        if any(keyword in code for keyword in keywords):
            return purpose
    
    return 'general programming logic'


def generate_overview(code: str, language: str) -> str:
    """Generate an overview of what the code does."""
    lines = [line for line in code.split('\n') if line.strip()]
    line_count = len(lines)
    
    overview = f"This {language} code snippet contains {line_count} lines. "
    
    # Detect common patterns
    if any(keyword in code for keyword in ['function', 'def ', 'void ']):
        overview += 'It defines one or more functions. '
    
    if 'class ' in code:
        overview += 'It includes class definitions. '
    
    if any(keyword in code for keyword in ['import ', 'require(', '#include']):
        overview += 'It imports external modules or libraries. '
    
    if any(keyword in code for keyword in ['for ', 'while ']):
        overview += 'It contains loop structures for iteration. '
    
    if any(keyword in code for keyword in ['if ', 'switch ']):
        overview += 'It uses conditional logic for decision-making. '
    
    overview += f"\n\nThe code appears to be {detect_code_purpose(code)} based on its structure and keywords."
    
    return overview


def explain_line(line: str, language: str) -> str:
    """Explain a single line of code."""
    trimmed = line.strip()
    
    # Function declarations
    func_match = re.search(r'function\s+(\w+)', trimmed)
    if func_match:
        func_name = func_match.group(1)
        params_match = re.search(r'\((.*?)\)', trimmed)
        params = params_match.group(1) if params_match else ''
        if params:
            return f"Declares a function named '{func_name}' that accepts parameters: {params}. This creates a reusable block of code."
        return f"Declares a function named '{func_name}' with no parameters. This creates a reusable block of code."
    
    # Python function definitions
    py_func_match = re.search(r'def\s+(\w+)', trimmed)
    if py_func_match:
        func_name = py_func_match.group(1)
        return f"Defines a Python function named '{func_name}'. This creates a reusable code block that can be called later."
    
    # Arrow functions
    arrow_match = re.search(r'(?:const|let|var)\s+(\w+)\s*=\s*\([^)]*\)\s*=>', trimmed)
    if arrow_match:
        func_name = arrow_match.group(1)
        return f"Creates an arrow function assigned to '{func_name}'. Arrow functions are a concise way to write functions in JavaScript."
    
    # Return statements
    if trimmed.startswith('return '):
        return_value = re.sub(r';.*$', '', trimmed.replace('return ', ''))
        if len(return_value) < 30:
            return f"Returns the value: {return_value}. This exits the function and sends back the result to wherever it was called."
        return "Returns a computed value back to the caller. This exits the current function and provides its result."
    
    # Variable declarations
    var_match = re.search(r'(?:const|let|var)\s+(\w+)\s*=\s*(.+)', trimmed)
    if var_match:
        var_name = var_match.group(1)
        value = re.sub(r';.*$', '', var_match.group(2))
        var_type = 'constant' if trimmed.startswith('const') else 'variable'
        
        if 'require(' in value or 'import' in value:
            return f"Creates a {var_type} '{var_name}' that imports/requires an external module for use in this code."
        if re.match(r'^\d+$', value):
            return f"Declares a {var_type} '{var_name}' and assigns it the numeric value {value}."
        if re.match(r"^['\"`]", value):
            return f"Declares a {var_type} '{var_name}' and assigns it a string value."
        if 'new ' in value:
            class_match = re.search(r'new\s+(\w+)', value)
            class_name = class_match.group(1) if class_match else 'a class'
            return f"Creates a new instance of {class_name} and stores it in '{var_name}'."
        if '=>' in value or 'function' in value:
            return f"Assigns a function to the {var_type} '{var_name}', creating a callable reference."
        return f"Declares a {var_type} '{var_name}' and initializes it with a value."
    
    # Conditional statements
    if_match = re.search(r'if\s*\((.*?)\)', trimmed)
    if if_match:
        condition = if_match.group(1)
        if len(condition) < 40:
            return f"Checks if the condition '{condition}' is true. If so, the following code block executes."
        return "Evaluates a conditional statement. If the condition is true, it executes the code inside the if block."
    
    if re.search(r'else\s+if\s*\(', trimmed):
        return "Checks an alternative condition if the previous 'if' was false. Allows testing multiple conditions sequentially."
    
    if trimmed == 'else' or trimmed.startswith('else {'):
        return "Executes this code block if all previous 'if' and 'else if' conditions were false. Acts as a fallback option."
    
    # Loops
    if re.search(r'for\s*\(', trimmed):
        if ' of ' in trimmed:
            return "Iterates over each element in a collection using a for...of loop. Simpler than traditional for loops."
        if ' in ' in trimmed:
            return "Iterates over object properties or array indices using a for...in loop."
        return "Creates a loop that repeats code a specific number of times, typically using a counter variable."
    
    if re.search(r'while\s*\(', trimmed):
        return "Creates a loop that continues executing as long as the condition remains true. Use caution to avoid infinite loops."
    
    # Array methods
    if '.map(' in trimmed:
        return "Transforms each element of an array using the provided function, creating a new array with the results."
    if '.filter(' in trimmed:
        return "Creates a new array containing only elements that pass the test implemented by the provided function."
    if '.reduce(' in trimmed:
        return "Reduces an array to a single value by executing a function on each element, accumulating the result."
    if '.forEach(' in trimmed:
        return "Executes a function once for each array element. Similar to a for loop but more functional in style."
    if '.find(' in trimmed:
        return "Searches the array and returns the first element that satisfies the provided testing function."
    
    # Async/await
    if 'async ' in trimmed and 'function' in trimmed:
        return "Declares an asynchronous function that can use 'await' to pause execution until promises resolve."
    if 'await ' in trimmed:
        return "Pauses execution until the promise resolves, then continues with the result. Makes async code read like synchronous code."
    
    # Imports/requires
    import_match = re.search(r'import\s+(.+?)\s+from', trimmed)
    if import_match:
        imported = import_match.group(1)
        return f"Imports {imported} from an external module, making it available for use in this file."
    
    if 'require(' in trimmed:
        module_match = re.search(r"require\(['\"](.+?)['\"]\)", trimmed)
        if module_match:
            module = module_match.group(1)
            return f"Loads the '{module}' module using Node.js require system, making its exports available."
        return "Loads an external module using the CommonJS require system."
    
    # Class definitions
    class_match = re.search(r'class\s+(\w+)', trimmed)
    if class_match:
        class_name = class_match.group(1)
        extends_match = re.search(r'extends\s+(\w+)', trimmed)
        if extends_match:
            return f"Defines a class '{class_name}' that inherits from '{extends_match.group(1)}', gaining its properties and methods."
        return f"Defines a class named '{class_name}', which is a blueprint for creating objects with specific properties and methods."
    
    # Console/print statements
    if 'console.log(' in trimmed:
        return "Outputs information to the console for debugging or monitoring purposes. Useful for tracking code execution."
    if 'console.error(' in trimmed:
        return "Outputs an error message to the console, typically used for error handling and debugging."
    if re.search(r'print\s*\(', trimmed):
        return "Outputs text or values to the standard output (usually the screen or console)."
    
    # Try-catch
    if trimmed == 'try {' or trimmed.startswith('try {'):
        return "Begins a try block to execute code that might throw an error. Allows graceful error handling."
    if re.search(r'catch\s*\(', trimmed):
        return "Catches and handles any errors thrown in the try block, preventing the program from crashing."
    if trimmed == 'finally {' or trimmed.startswith('finally {'):
        return "Executes code regardless of whether an error occurred, typically used for cleanup operations."
    
    # Object/Array operations
    if 'push(' in trimmed:
        return "Adds one or more elements to the end of an array, modifying the original array."
    if 'pop(' in trimmed:
        return "Removes and returns the last element from an array, modifying the original array."
    
    # Method calls
    method_match = re.search(r'\.(\w+)\(', trimmed)
    if method_match:
        method = method_match.group(1)
        return f"Calls the '{method}' method on an object, executing its associated functionality."
    
    # Assignments
    if '=' in trimmed and '==' not in trimmed and '===' not in trimmed:
        var_name = trimmed.split('=')[0].strip()
        return f"Assigns a new value to '{var_name}', updating its stored data."
    
    # Generic fallback
    if trimmed.endswith('{'):
        return "Opens a code block that groups related statements together."
    if trimmed in ['}', '};']:
        return "Closes the current code block, ending the scope of the previous statement (function, loop, conditional, etc.)."
    
    return "Executes a statement that performs an operation or calculation as part of the program logic."


def generate_line_by_line(code: str, language: str) -> List[Dict[str, Any]]:
    """Generate line-by-line explanations."""
    lines = code.split('\n')
    explanations = []
    
    for index, line in enumerate(lines):
        trimmed = line.strip()
        
        # Skip empty lines and pure comment lines
        if not trimmed:
            continue
        if any(trimmed.startswith(c) for c in ['//', '#', '/*', '*']):
            continue
        
        explanation = explain_line(trimmed, language)
        explanations.append({
            'line_number': index + 1,
            'code': line,
            'explanation': explanation
        })
    
    return explanations


def generate_suggestions(code: str, language: str) -> List[Dict[str, str]]:
    """Generate improvement suggestions."""
    suggestions = []
    lines = code.split('\n')
    
    # Nested loops
    if re.search(r'for\s*\([^)]*\)\s*{[^}]*for\s*\(', code, re.DOTALL):
        suggestions.append({
            'title': 'Optimize Nested Loops',
            'description': 'Nested loops can have O(n²) complexity. Consider using hash maps, array methods like .find(), or refactoring to reduce iterations.',
            'example': '// Instead of nested loops:\nconst item = array.find(x => x.id === targetId);\n// Or use a Map for O(1) lookups:\nconst map = new Map(items.map(i => [i.id, i]));'
        })
    
    # Missing error handling for async
    if ('fetch(' in code or 'axios' in code) and 'catch' not in code and 'try' not in code:
        suggestions.append({
            'title': 'Add Error Handling for Network Requests',
            'description': 'Network requests can fail due to connectivity issues, server errors, or timeouts. Always handle errors to provide a better user experience.',
            'example': 'try {\n  const response = await fetch(url);\n  if (!response.ok) throw new Error(`HTTP ${response.status}`);\n  const data = await response.json();\n} catch (error) {\n  console.error("Failed to fetch:", error);\n  // Show error message to user\n}'
        })
    
    # Using var instead of const/let
    if language == 'javascript' and 'var ' in code:
        var_count = len(re.findall(r'\bvar\b', code))
        suggestions.append({
            'title': 'Replace "var" with "const" or "let"',
            'description': f'Found {var_count} use(s) of "var". Use "const" for values that won\'t change, "let" for values that will. This provides better scoping (block vs function) and prevents hoisting issues.',
            'example': 'const API_URL = "https://api.example.com"; // won\'t change\nlet counter = 0; // will change\n\n// "var" has function scope and hoisting issues:\nvar x = 1; // can leak outside blocks'
        })
    
    # Magic numbers
    magic_numbers = re.findall(r'(?<![a-zA-Z0-9_])\d{2,}(?![a-zA-Z0-9_])', code)
    if len(magic_numbers) > 2 and not re.search(r'const\s+[A-Z_]+\s*=', code):
        suggestions.append({
            'title': 'Extract Magic Numbers to Named Constants',
            'description': f'Hard-coded values like {", ".join(magic_numbers[:3])} make code harder to understand and maintain. Use descriptive constant names.',
            'example': 'const MAX_RETRY_ATTEMPTS = 3;\nconst TIMEOUT_MILLISECONDS = 5000;\nconst MIN_PASSWORD_LENGTH = 8;\n\n// More readable:\nif (password.length < MIN_PASSWORD_LENGTH) { ... }'
        })
    
    # console.log in production
    if 'console.log(' in code:
        log_count = len(re.findall(r'console\.log\(', code))
        suggestions.append({
            'title': 'Use Proper Logging Instead of console.log',
            'description': f'Found {log_count} console.log statement(s). Consider using a proper logging library or remove before production.',
            'example': '// Development:\nif (process.env.NODE_ENV === "development") {\n  console.debug("Debug info:", data);\n}\n\n// Or use a logger:\nimport logger from "./logger";\nlogger.info("User logged in", { userId });'
        })
    
    # == instead of ===
    if '==' in code and '===' not in code:
        suggestions.append({
            'title': 'Use Strict Equality (===)',
            'description': 'Use === instead of == to avoid type coercion bugs. Strict equality checks both value and type.',
            'example': '// Bad: Uses type coercion\nif (value == "5") // true for both "5" and 5\n\n// Good: Strict comparison\nif (value === "5") // only true for string "5"'
        })
    
    # Large functions
    if len(lines) > 25 and 'function' in code:
        suggestions.append({
            'title': 'Break Down Large Functions',
            'description': 'This function is quite long. Consider breaking it into smaller, focused functions that each do one thing well. Aim for functions under 20-30 lines.',
            'example': '// Instead of one large function:\nfunction processOrder(order) {\n  const validated = validateOrder(order);\n  const calculated = calculateTotal(validated);\n  const saved = saveOrder(calculated);\n  return notifyUser(saved);\n}'
        })
    
    # No suggestions case
    if len(suggestions) == 0:
        suggestions.append({
            'title': 'Consider Adding Unit Tests',
            'description': 'Well-tested code is more maintainable and reliable. Consider writing unit tests for your functions to catch bugs early.',
            'example': '// Using pytest or similar:\ndef test_calculate_total():\n    assert calculate_total(10, 5) == 15'
        })
        
        suggestions.append({
            'title': 'Add Type Safety with Type Hints',
            'description': 'Type hints catch type errors early and improve code quality with better IDE support.',
            'example': '# Python with type hints:\ndef greet(name: str) -> str:\n    return f"Hello, {name}"\n\n# Editor will catch: greet(123) # Error'
        })
    
    # Return max 3 suggestions
    return suggestions[:3]


# ============================================
# STREAMLIT UI
# ============================================

# Header
st.markdown('<h1 class="main-header">⚡ Code Analyzer</h1>', unsafe_allow_html=True)
st.markdown('<p class="tagline">AI-Powered Code Insights & Suggestions</p>', unsafe_allow_html=True)

# Language selector
col1, col2 = st.columns([3, 1])
with col2:
    language = st.selectbox(
        "Language",
        ["javascript", "python", "java", "cpp", "csharp", "go", "rust", "typescript"],
        index=0
    )

# Code input
st.markdown("### 📝 Paste Your Code")
code_input = st.text_area(
    "Code",
    placeholder="// Paste or type your code here...\nfunction example() {\n    return 'Hello, World!';\n}",
    height=300,
    label_visibility="collapsed"
)

# Analyze button
if st.button("🔍 Analyze Code", use_container_width=True):
    if code_input.strip():
        with st.spinner("Analyzing your code..."):
            # Generate analysis
            overview = generate_overview(code_input, language)
            line_by_line = generate_line_by_line(code_input, language)
            suggestions = generate_suggestions(code_input, language)
            
            st.markdown("---")
            
            # Overview Section
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-header">📄 What This Code Does</div>', unsafe_allow_html=True)
            st.markdown(f'<p style="color: #d0d0e0; line-height: 1.6;">{overview}</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Line-by-Line Section
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-header">📋 Line-by-Line Explanation</div>', unsafe_allow_html=True)
            
            if line_by_line:
                for item in line_by_line:
                    st.markdown(f'''
                    <div class="line-item">
                        <span class="line-number">Line {item['line_number']}</span>
                        <code class="line-code">{item['code']}</code>
                        <p class="line-explanation">{item['explanation']}</p>
                    </div>
                    ''', unsafe_allow_html=True)
            else:
                st.markdown('<p style="color: #a0a0c0;">No executable lines found to explain.</p>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Suggestions Section
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-header">💡 Suggestions to Improve</div>', unsafe_allow_html=True)
            
            for suggestion in suggestions:
                example_html = f'<code class="suggestion-example">{suggestion["example"]}</code>' if suggestion.get('example') else ''
                st.markdown(f'''
                <div class="suggestion-item">
                    <div class="suggestion-title">{suggestion['title']}</div>
                    <p class="suggestion-description">{suggestion['description']}</p>
                    {example_html}
                </div>
                ''', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("⚠️ Please enter some code to analyze!")

# Footer
st.markdown("---")
st.markdown('<p style="text-align: center; color: #a0a0c0; margin-top: 2rem;">Built with ❤️ using AI-powered analysis</p>', unsafe_allow_html=True)
