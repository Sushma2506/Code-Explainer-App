# ⚡ Code Analyzer - AI-Powered Insights

A premium Streamlit application that uses Google's Gemini 1.5 Flash to provide deep insights, line-by-line explanations, and improvement suggestions for your code.

## ✨ Features

- **AI-Powered Analysis**: Leverages Google's Gemini 1.5 Flash model for accurate code understanding.
- **Premium UI**: sleek dark mode design with glassmorphism effects and custom fonts (Inter & Fira Code).
- **Multi-Language Support**: Analyzes Python, JavaScript, Java, C++, Go, Rust, and more.
- **Structured Insights**:
    - **Overview**: High-level summary of code purpose.
    - **Line-by-Line**: Detailed breakdown of complex logic.
    - **Suggestions**: Actionable improvements for performance and best practices.

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- A [Google Gemini API Key](https://aistudio.google.com/)

### Installation

1.  Clone the repository or navigate to the project directory:
    ```bash
    cd code_explainer_v2
    ```

2.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Usage

1.  Run the Streamlit application:
    ```bash
    streamlit run app.py
    ```

2.  Open your browser (usually at `http://localhost:8501`).

3.  **Enter your API Key**: Expand the sidebar and paste your Google Gemini API Key.

4.  **Analyze**: Paste a code snippet into the text area, select the language, and click **Analyze Code**.

## 🛠️ Built With

- [Streamlit](https://streamlit.io/) - The fastest way to build data apps in Python.
- [Google Generative AI](https://ai.google.dev/) - Powering the code analysis.

## 📄 License

This project is open-source and available for personal and educational use.
