// ============================================
// CODE ANALYZER - MAIN JAVASCRIPT
// ============================================

// DOM Elements
const codeInput = document.getElementById('code-input');
const analyzeBtn = document.getElementById('analyze-btn');
const resultsSection = document.getElementById('results');
const loadingOverlay = document.getElementById('loading-overlay');
const overviewContent = document.getElementById('overview-content');
const explanationContent = document.getElementById('explanation-content');
const suggestionsContent = document.getElementById('suggestions-content');
const languageSelect = document.getElementById('language-select');

// ============================================
// EVENT LISTENERS
// ============================================
analyzeBtn.addEventListener('click', analyzeCode);

codeInput.addEventListener('input', (e) => {
    // Auto-resize textarea
    e.target.style.height = 'auto';
    e.target.style.height = Math.max(300, e.target.scrollHeight) + 'px';
});

// Allow Ctrl+Enter or Cmd+Enter to analyze
codeInput.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        analyzeCode();
    }
});

// ============================================
// MAIN ANALYSIS FUNCTION
// ============================================
async function analyzeCode() {
    const code = codeInput.value.trim();

    if (!code) {
        alert('Please enter some code to analyze!');
        return;
    }

    // Show loading state
    showLoading();

    try {
        // Simulate API call delay
        await sleep(2000);

        // Get analysis (you can replace this with actual API call)
        const analysis = await getCodeAnalysis(code, languageSelect.value);

        // Display results
        displayResults(analysis);

    } catch (error) {
        console.error('Analysis error:', error);
        alert('An error occurred during analysis. Please try again.');
    } finally {
        hideLoading();
    }
}

// ============================================
// ANALYSIS LOGIC
// ============================================
async function getCodeAnalysis(code, language) {
    // This is a placeholder function that demonstrates the structure.
    // In a real application, you would call an AI API (OpenAI, Anthropic, etc.)
    // 
    // Example API integration:
    // const response = await fetch('YOUR_API_ENDPOINT', {
    //     method: 'POST',
    //     headers: { 'Content-Type': 'application/json' },
    //     body: JSON.stringify({ code, language })
    // });
    // return await response.json();

    // For now, we'll use a simple rule-based analysis
    return analyzeCodeLocally(code, language);
}

function analyzeCodeLocally(code, language) {
    const lines = code.split('\n').filter(line => line.trim());

    // Overview Analysis
    const overview = generateOverview(code, language, lines.length);

    // Line-by-Line Explanation
    const lineByLine = generateLineByLine(code, language);

    // Suggestions
    const suggestions = generateSuggestions(code, language);

    return {
        overview,
        lineByLine,
        suggestions
    };
}

function generateOverview(code, language, lineCount) {
    let overview = `This ${language} code snippet contains ${lineCount} lines. `;

    // Detect common patterns
    if (code.includes('function') || code.includes('def ') || code.includes('void ')) {
        overview += 'It defines one or more functions. ';
    }

    if (code.includes('class ')) {
        overview += 'It includes class definitions. ';
    }

    if (code.includes('import ') || code.includes('require(') || code.includes('#include')) {
        overview += 'It imports external modules or libraries. ';
    }

    if (code.includes('for ') || code.includes('while ')) {
        overview += 'It contains loop structures for iteration. ';
    }

    if (code.includes('if ') || code.includes('switch ')) {
        overview += 'It uses conditional logic for decision-making. ';
    }

    overview += `\n\nThe code appears to be ${detectCodePurpose(code)} based on its structure and keywords.`;

    return overview;
}

function detectCodePurpose(code) {
    const purposes = [
        { keywords: ['fetch', 'axios', 'http', 'api', 'request'], purpose: 'performing HTTP requests or API calls' },
        { keywords: ['addEventListener', 'onClick', 'DOM', 'document'], purpose: 'handling DOM manipulation and events' },
        { keywords: ['useState', 'useEffect', 'component'], purpose: 'building a React component' },
        { keywords: ['class', 'constructor', 'extends'], purpose: 'implementing object-oriented programming concepts' },
        { keywords: ['async', 'await', 'Promise'], purpose: 'handling asynchronous operations' },
        { keywords: ['map', 'filter', 'reduce'], purpose: 'performing array transformations' },
    ];

    for (const { keywords, purpose } of purposes) {
        if (keywords.some(keyword => code.includes(keyword))) {
            return purpose;
        }
    }

    return 'general programming logic';
}

function generateLineByLine(code, language) {
    const lines = code.split('\n');
    const explanations = [];

    lines.forEach((line, index) => {
        const trimmedLine = line.trim();
        // Skip empty lines and pure comment lines only
        if (!trimmedLine) return;
        if (trimmedLine.startsWith('//') || trimmedLine.startsWith('#') || trimmedLine.startsWith('/*') || trimmedLine.startsWith('*')) {
            return;
        }

        const explanation = explainLine(trimmedLine, language);
        explanations.push({
            lineNumber: index + 1,
            code: line,
            explanation
        });
    });

    return explanations;
}

function explainLine(line, language) {
    const trimmed = line.trim();

    // Function declarations
    if (trimmed.match(/function\s+(\w+)/)) {
        const funcName = trimmed.match(/function\s+(\w+)/)[1];
        const hasParams = trimmed.includes('(') && trimmed.match(/\((.*?)\)/);
        const params = hasParams ? trimmed.match(/\((.*?)\)/)[1] : '';
        if (params) {
            return `Declares a function named '${funcName}' that accepts parameters: ${params}. This creates a reusable block of code.`;
        }
        return `Declares a function named '${funcName}' with no parameters. This creates a reusable block of code.`;
    }

    // Python function definitions
    if (trimmed.match(/def\s+(\w+)/)) {
        const funcName = trimmed.match(/def\s+(\w+)/)[1];
        return `Defines a Python function named '${funcName}'. This creates a reusable code block that can be called later.`;
    }

    // Arrow functions (JavaScript)
    if (trimmed.match(/(?:const|let|var)\s+(\w+)\s*=\s*\([^)]*\)\s*=>/)) {
        const funcName = trimmed.match(/(\w+)\s*=/)[1];
        return `Creates an arrow function assigned to '${funcName}'. Arrow functions are a concise way to write functions in JavaScript.`;
    }

    // Return statements
    if (trimmed.startsWith('return ')) {
        const returnValue = trimmed.replace('return ', '').replace(/;.*$/, '');
        if (returnValue.length < 30) {
            return `Returns the value: ${returnValue}. This exits the function and sends back the result to wherever it was called.`;
        }
        return `Returns a computed value back to the caller. This exits the current function and provides its result.`;
    }

    // Variable declarations with values
    if (trimmed.match(/(?:const|let|var)\s+(\w+)\s*=\s*(.+)/)) {
        const match = trimmed.match(/(?:const|let|var)\s+(\w+)\s*=\s*(.+)/);
        const varName = match[1];
        const value = match[2].replace(/;.*$/, '');
        const type = trimmed.startsWith('const') ? 'constant' : 'variable';

        if (value.includes('require(') || value.includes('import')) {
            return `Creates a ${type} '${varName}' that imports/requires an external module for use in this code.`;
        }
        if (value.match(/^\d+$/)) {
            return `Declares a ${type} '${varName}' and assigns it the numeric value ${value}.`;
        }
        if (value.match(/^['"`]/)) {
            return `Declares a ${type} '${varName}' and assigns it a string value.`;
        }
        if (value.includes('new ')) {
            const className = value.match(/new\s+(\w+)/)?.[1];
            return `Creates a new instance of ${className || 'a class'} and stores it in '${varName}'.`;
        }
        if (value.includes('=>') || value.includes('function')) {
            return `Assigns a function to the ${type} '${varName}', creating a callable reference.`;
        }
        return `Declares a ${type} '${varName}' and initializes it with a value.`;
    }

    // Conditional statements
    if (trimmed.match(/if\s*\(/)) {
        const condition = trimmed.match(/if\s*\((.*?)\)/)?.[1];
        if (condition && condition.length < 40) {
            return `Checks if the condition '${condition}' is true. If so, the following code block executes.`;
        }
        return `Evaluates a conditional statement. If the condition is true, it executes the code inside the if block.`;
    }

    if (trimmed.match(/else\s+if\s*\(/)) {
        return `Checks an alternative condition if the previous 'if' was false. Allows testing multiple conditions sequentially.`;
    }

    if (trimmed.trim() === 'else' || trimmed.startsWith('else {')) {
        return `Executes this code block if all previous 'if' and 'else if' conditions were false. Acts as a fallback option.`;
    }

    // Loops
    if (trimmed.match(/for\s*\(/)) {
        if (trimmed.includes(' of ')) {
            return `Iterates over each element in a collection using a for...of loop. Simpler than traditional for loops.`;
        }
        if (trimmed.includes(' in ')) {
            return `Iterates over object properties or array indices using a for...in loop.`;
        }
        return `Creates a loop that repeats code a specific number of times, typically using a counter variable.`;
    }

    if (trimmed.match(/while\s*\(/)) {
        return `Creates a loop that continues executing as long as the condition remains true. Use caution to avoid infinite loops.`;
    }

    // Array methods
    if (trimmed.includes('.map(')) {
        return `Transforms each element of an array using the provided function, creating a new array with the results.`;
    }

    if (trimmed.includes('.filter(')) {
        return `Creates a new array containing only elements that pass the test implemented by the provided function.`;
    }

    if (trimmed.includes('.reduce(')) {
        return `Reduces an array to a single value by executing a function on each element, accumulating the result.`;
    }

    if (trimmed.includes('.forEach(')) {
        return `Executes a function once for each array element. Similar to a for loop but more functional in style.`;
    }

    if (trimmed.includes('.find(')) {
        return `Searches the array and returns the first element that satisfies the provided testing function.`;
    }

    // Async/await
    if (trimmed.includes('async ') && trimmed.includes('function')) {
        return `Declares an asynchronous function that can use 'await' to pause execution until promises resolve.`;
    }

    if (trimmed.includes('await ')) {
        const awaitedValue = trimmed.match(/await\s+([^;]+)/)?.[1];
        return `Pauses execution until the promise resolves, then continues with the result. Makes async code read like synchronous code.`;
    }

    // Imports/requires
    if (trimmed.match(/import\s+.*\s+from/)) {
        const imported = trimmed.match(/import\s+(.+?)\s+from/)?.[1];
        return `Imports ${imported} from an external module, making it available for use in this file.`;
    }

    if (trimmed.includes('require(')) {
        const module = trimmed.match(/require\(['"](.+?)['"]\)/)?.[1];
        if (module) {
            return `Loads the '${module}' module using Node.js require system, making its exports available.`;
        }
        return `Loads an external module using the CommonJS require system.`;
    }

    // Class definitions
    if (trimmed.match(/class\s+(\w+)/)) {
        const className = trimmed.match(/class\s+(\w+)/)[1];
        const extendsMatch = trimmed.match(/extends\s+(\w+)/);
        if (extendsMatch) {
            return `Defines a class '${className}' that inherits from '${extendsMatch[1]}', gaining its properties and methods.`;
        }
        return `Defines a class named '${className}', which is a blueprint for creating objects with specific properties and methods.`;
    }

    // Console/print statements
    if (trimmed.includes('console.log(')) {
        return `Outputs information to the console for debugging or monitoring purposes. Useful for tracking code execution.`;
    }

    if (trimmed.includes('console.error(')) {
        return `Outputs an error message to the console, typically used for error handling and debugging.`;
    }

    if (trimmed.match(/print\s*\(/)) {
        return `Outputs text or values to the standard output (usually the screen or console).`;
    }

    // Try-catch
    if (trimmed.trim() === 'try {' || trimmed.startsWith('try {')) {
        return `Begins a try block to execute code that might throw an error. Allows graceful error handling.`;
    }

    if (trimmed.match(/catch\s*\(/)) {
        return `Catches and handles any errors thrown in the try block, preventing the program from crashing.`;
    }

    if (trimmed.trim() === 'finally {' || trimmed.startsWith('finally {')) {
        return `Executes code regardless of whether an error occurred, typically used for cleanup operations.`;
    }

    // Object/Array operations
    if (trimmed.includes('push(')) {
        return `Adds one or more elements to the end of an array, modifying the original array.`;
    }

    if (trimmed.includes('pop(')) {
        return `Removes and returns the last element from an array, modifying the original array.`;
    }

    // Method calls
    if (trimmed.match(/\.(\w+)\(/)) {
        const method = trimmed.match(/\.(\w+)\(/)[1];
        return `Calls the '${method}' method on an object, executing its associated functionality.`;
    }

    // Assignments
    if (trimmed.includes('=') && !trimmed.includes('==') && !trimmed.includes('===')) {
        const varName = trimmed.split('=')[0].trim();
        return `Assigns a new value to '${varName}', updating its stored data.`;
    }

    // Generic fallback with more context
    if (trimmed.endsWith('{')) {
        return `Opens a code block that groups related statements together.`;
    }

    if (trimmed === '}' || trimmed === '};') {
        return `Closes the current code block, ending the scope of the previous statement (function, loop, conditional, etc.).`;
    }

    return `Executes a statement that performs an operation or calculation as part of the program logic.`;
}

function generateSuggestions(code, language) {
    const suggestions = [];
    const lines = code.split('\n');
    const trimmedCode = code.trim();

    // Performance: Inefficient loops
    if (code.match(/for\s*\([^)]*\)\s*{[^}]*for\s*\(/s)) {
        suggestions.push({
            title: 'Optimize Nested Loops',
            description: 'Nested loops can have O(n²) complexity. Consider using hash maps, array methods like .find(), or refactoring to reduce iterations.',
            example: '// Instead of nested loops:\nconst item = array.find(x => x.id === targetId);\n// Or use a Map for O(1) lookups:\nconst map = new Map(items.map(i => [i.id, i]));'
        });
    }

    // Missing error handling for async operations
    if ((code.includes('fetch(') || code.includes('axios')) && !code.includes('catch') && !code.includes('try')) {
        suggestions.push({
            title: 'Add Error Handling for Network Requests',
            description: 'Network requests can fail due to connectivity issues, server errors, or timeouts. Always handle errors to provide a better user experience.',
            example: 'try {\n  const response = await fetch(url);\n  if (!response.ok) throw new Error(`HTTP ${response.status}`);\n  const data = await response.json();\n} catch (error) {\n  console.error("Failed to fetch:", error);\n  // Show error message to user\n}'
        });
    }

    // Missing error handling for async functions
    if (code.includes('async ') && !code.includes('catch') && !code.includes('try') && !code.includes('fetch')) {
        suggestions.push({
            title: 'Add Try-Catch for Async Operations',
            description: 'Async functions can reject/throw errors. Wrap await statements in try-catch to handle failures gracefully.',
            example: 'async function getData() {\n  try {\n    const result = await someAsyncOperation();\n    return result;\n  } catch (error) {\n    console.error("Operation failed:", error);\n    return null; // or throw with context\n  }\n}'
        });
    }

    // Using var instead of const/let
    if (language === 'javascript' && code.includes('var ')) {
        const varCount = (code.match(/\bvar\b/g) || []).length;
        suggestions.push({
            title: 'Replace "var" with "const" or "let"',
            description: `Found ${varCount} use(s) of "var". Use "const" for values that won't change, "let" for values that will. This provides better scoping (block vs function) and prevents hoisting issues.`,
            example: 'const API_URL = "https://api.example.com"; // won\'t change\nlet counter = 0; // will change\n\n// "var" has function scope and hoisting issues:\nvar x = 1; // can leak outside blocks'
        });
    }

    // Magic numbers/strings
    const magicNumbers = code.match(/(?<![a-zA-Z0-9_])\d{2,}(?![a-zA-Z0-9_])/g);
    if (magicNumbers && magicNumbers.length > 2 && !code.match(/const\s+[A-Z_]+\s*=/)) {
        suggestions.push({
            title: 'Extract Magic Numbers to Named Constants',
            description: 'Hard-coded values like ' + magicNumbers.slice(0, 3).join(', ') + ' make code harder to understand and maintain. Use descriptive constant names.',
            example: 'const MAX_RETRY_ATTEMPTS = 3;\nconst TIMEOUT_MILLISECONDS = 5000;\nconst MIN_PASSWORD_LENGTH = 8;\n\n// More readable:\nif (password.length < MIN_PASSWORD_LENGTH) { ... }'
        });
    }

    // Lack of input validation
    if (code.match(/function\s+\w+\s*\([^)]+\)/) && !code.includes('if') && !code.includes('throw') && !code.includes('assert')) {
        const funcMatch = code.match(/function\s+(\w+)\s*\(([^)]+)\)/);
        if (funcMatch) {
            suggestions.push({
                title: 'Add Input Validation',
                description: 'Functions should validate their inputs to fail fast with clear error messages rather than causing issues later in execution.',
                example: `function ${funcMatch[1]}(${funcMatch[2]}) {\n  if (!${funcMatch[2].split(',')[0].trim()}) {\n    throw new Error('${funcMatch[2].split(',')[0].trim()} is required');\n  }\n  // rest of function...\n}`
            });
        }
    }

    // Console.log in production code
    if (code.includes('console.log(')) {
        const logCount = (code.match(/console\.log\(/g) || []).length;
        suggestions.push({
            title: 'Use Proper Logging Instead of console.log',
            description: `Found ${logCount} console.log statement(s). Consider using a proper logging library or remove before production. For debugging, use console.debug() or a logger with levels.`,
            example: '// Development:\nif (process.env.NODE_ENV === "development") {\n  console.debug("Debug info:", data);\n}\n\n// Or use a logger:\nimport logger from "./logger";\nlogger.info("User logged in", { userId });'
        });
    }

    // Callback hell / Promise chains
    if (code.includes('.then(') && code.match(/\.then\([^)]*\.then\(/)) {
        suggestions.push({
            title: 'Refactor Promise Chains to Async/Await',
            description: 'Long .then() chains are harder to read and debug. Use async/await for cleaner, more maintainable asynchronous code.',
            example: '// Instead of:\n// fetch().then(r => r.json()).then(data => process(data)).then(...)\n\n// Use:\nasync function fetchData() {\n  const response = await fetch(url);\n  const data = await response.json();\n  return processData(data);\n}'
        });
    }

    // Missing documentation for complex functions
    const complexFunction = lines.length > 10 && code.includes('function') && !code.includes('/**');
    if (complexFunction) {
        suggestions.push({
            title: 'Add JSDoc Documentation',
            description: 'This function is complex enough to warrant documentation. Use JSDoc to describe parameters, return values, and purpose.',
            example: '/**\n * Processes user data and saves to database\n * @param {Object} userData - The user data object\n * @param {string} userData.email - User email address\n * @param {string} userData.name - User full name\n * @returns {Promise<Object>} The saved user object\n * @throws {ValidationError} If user data is invalid\n */\nasync function processUser(userData) { ... }'
        });
    }

    // Direct DOM manipulation without checks
    if (code.includes('document.getElementById') && !code.includes('if (')) {
        suggestions.push({
            title: 'Check DOM Elements Before Manipulating',
            description: 'Always verify DOM elements exist before manipulating them to avoid "Cannot read property of null" errors.',
            example: 'const element = document.getElementById("myId");\nif (element) {\n  element.textContent = "Updated";\n} else {\n  console.warn("Element not found: myId");\n}'
        });
    }

    // == instead of ===
    if (code.includes('==') && !code.includes('===')) {
        suggestions.push({
            title: 'Use Strict Equality (===)',
            description: 'Use === instead of == to avoid type coercion bugs. Strict equality checks both value and type.',
            example: '// Bad: Uses type coercion\nif (value == "5") // true for both "5" and 5\n\n// Good: Strict comparison\nif (value === "5") // only true for string "5"'
        });
    }

    // Large functions
    if (lines.length > 25 && code.includes('function')) {
        suggestions.push({
            title: 'Break Down Large Functions',
            description: 'This function is quite long. Consider breaking it into smaller, focused functions that each do one thing well. Aim for functions under 20-30 lines.',
            example: '// Instead of one large function:\nfunction processOrder(order) {\n  const validated = validateOrder(order);\n  const calculated = calculateTotal(validated);\n  const saved = saveOrder(calculated);\n  return notifyUser(saved);\n}'
        });
    }

    // Missing return type documentation
    if (language === 'javascript' && code.match(/function\s+\w+/) && code.includes('return ') && !code.includes('@returns') && !code.includes('@return')) {
        suggestions.push({
            title: 'Document Return Values',
            description: 'Functions that return values should document what they return using JSDoc @returns tag for better IDE support and clarity.',
            example: '/**\n * @returns {number} The calculated total price\n */\nfunction calculateTotal() { ... }'
        });
    }

    // No suggestions case
    if (suggestions.length === 0) {
        suggestions.push({
            title: 'Consider Adding Unit Tests',
            description: 'Well-tested code is more maintainable and reliable. Consider writing unit tests for your functions to catch bugs early.',
            example: '// Using Jest or similar:\ntest("should calculate total correctly", () => {\n  expect(calculateTotal(10, 5)).toBe(15);\n});'
        });

        suggestions.push({
            title: 'Add Type Safety with TypeScript',
            description: 'TypeScript catches type errors at compile time, improving code quality and developer experience with better autocomplete.',
            example: '// TypeScript version:\nfunction greet(name: string): string {\n  return `Hello, ${name}`;\n}\n// Editor will catch: greet(123) // Error: number not assignable to string'
        });
    }

    // Return max 3 most relevant suggestions
    return suggestions.slice(0, 3);
}

// ============================================
// UI DISPLAY FUNCTIONS
// ============================================
function displayResults(analysis) {
    // Show results section
    resultsSection.classList.remove('hidden');

    // Scroll to results
    setTimeout(() => {
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 300);

    // Display Overview
    overviewContent.innerHTML = `<p>${analysis.overview}</p>`;

    // Display Line-by-Line
    if (analysis.lineByLine.length > 0) {
        explanationContent.innerHTML = analysis.lineByLine.map(item => `
            <div class="line-item">
                <span class="line-number">Line ${item.lineNumber}</span>
                <code class="line-code">${escapeHtml(item.code)}</code>
                <p class="line-explanation">${item.explanation}</p>
            </div>
        `).join('');
    } else {
        explanationContent.innerHTML = '<p>No executable lines found to explain.</p>';
    }

    // Display Suggestions
    if (analysis.suggestions.length > 0) {
        suggestionsContent.innerHTML = analysis.suggestions.map(suggestion => `
            <div class="suggestion-item">
                <div class="suggestion-title">${suggestion.title}</div>
                <p class="suggestion-description">${suggestion.description}</p>
                ${suggestion.example ? `<code class="suggestion-example">${escapeHtml(suggestion.example)}</code>` : ''}
            </div>
        `).join('');
    } else {
        suggestionsContent.innerHTML = '<p>No specific suggestions found. Code looks good!</p>';
    }
}

function showLoading() {
    loadingOverlay.classList.remove('hidden');
    analyzeBtn.disabled = true;
}

function hideLoading() {
    loadingOverlay.classList.add('hidden');
    analyzeBtn.disabled = false;
}

// ============================================
// UTILITY FUNCTIONS
// ============================================
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// ============================================
// INTEGRATION GUIDE
// ============================================
/*
TO INTEGRATE WITH AN AI API (OpenAI, Anthropic, etc.):

1. Replace the getCodeAnalysis function with an API call:

async function getCodeAnalysis(code, language) {
    const response = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer YOUR_API_KEY'
        },
        body: JSON.stringify({
            model: 'gpt-4',
            messages: [{
                role: 'user',
                content: `Analyze this ${language} code and provide:
                1. What the code does (overview)
                2. Line-by-line explanation
                3. 2-3 suggestions to improve
                
                Code:
                ${code}
                
                Respond in JSON format with keys: overview, lineByLine (array of {lineNumber, code, explanation}), suggestions (array of {title, description, example})`
            }]
        })
    });
    
    const data = await response.json();
    return JSON.parse(data.choices[0].message.content);
}

2. For security, move your API key to environment variables or a backend service
3. Consider rate limiting and caching to optimize API usage
4. Add proper error handling for API failures
*/
