# 🚀 Code Analyzer

A beautiful, AI-powered application that analyzes your code and provides:
- **What the code does** - High-level overview
- **Line-by-line explanation** - Detailed breakdown of each line
- **2-3 suggestions to improve** - Actionable recommendations

## ✨ Features

- 🎨 **Premium Dark Theme** with glassmorphism effects
- ⚡ **Real-time Analysis** with smooth animations
- 🌈 **Multiple Language Support** (JavaScript, Python, Java, C++, and more)
- 📱 **Fully Responsive** design for all devices
- 🎯 **Intuitive UI** with micro-interactions
- 💡 **Smart Suggestions** for code improvement

## 🚀 Quick Start (Python/Streamlit Version)

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**
   ```bash
   streamlit run app.py
   ```

3. **Use the app**
   - The app will open in your default browser (usually at http://localhost:8501)
   - Select your programming language from the dropdown
   - Paste your code into the editor
   - Click "🔍 Analyze Code" to get insights

## 🛠️ How It Works

Currently, the app uses **local rule-based analysis** to provide basic code insights. This works great for demonstrating the functionality!

### 🔌 Integrating with AI APIs

For more powerful analysis, you can integrate with AI services like:

- **OpenAI GPT-4** - Most versatile, great for all languages
- **Anthropic Claude** - Excellent code understanding
- **Google Gemini** - Fast and capable
- **Local LLMs** - For privacy-focused deployments

#### Integration Steps:

1. Open `script.js`
2. Find the `getCodeAnalysis` function (around line 60)
3. Replace it with an API call (detailed example provided in comments)
4. Add your API key securely (use environment variables)

Example API integration is documented in the `script.js` file!

## 📁 Project Structure

```
Code-Explainer-App/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## 🎨 Customization

### Colors & Theme
Edit the CSS in `app.py` (look for `st.markdown("""<style>...`):
- Modify gradient colors (search for `#667eea` and `#764ba2`)
- Adjust card styling and backgrounds
- Change fonts and spacing

### Analysis Logic
Modify these functions in `app.py`:
- `generate_overview()` - Customize the overview generation
- `explain_line()` - Adjust line-by-line explanations
- `generate_suggestions()` - Add/modify suggestion rules

## 🌟 Design Philosophy

This app follows modern web design principles:
- **Visual Excellence** - Rich gradients, smooth animations
- **User Experience** - Intuitive interactions, responsive feedback
- **Performance** - Optimized load times, efficient rendering
- **Accessibility** - Semantic HTML, keyboard navigation support

## 🔧 Browser Compatibility

- ✅ Chrome/Edge (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Opera (latest)

## 📝 Supported Languages

Currently recognizes:
- JavaScript
- Python
- Java
- C++
- C#
- Go
- Rust
- TypeScript

More languages can be added easily!

## 🚀 Advanced Features (Future Ideas)

- [ ] Syntax highlighting in the editor
- [ ] Export analysis as PDF/Markdown
- [ ] Code comparison mode
- [ ] Performance metrics
- [ ] Security vulnerability detection
- [ ] Custom rule sets
- [ ] Team collaboration features

## 💡 Tips

- Use `Ctrl+Enter` (or `Cmd+Enter`) for quick analysis
- The textarea auto-expands as you type
- All animations respect "prefers-reduced-motion" setting
- Code is escaped to prevent XSS vulnerabilities

## 📄 License

Free to use and modify for personal and commercial projects!

## 🤝 Contributing

Feel free to enhance the analysis logic, improve the UI, or add new features!

---

Built with ❤️ using modern web technologies
