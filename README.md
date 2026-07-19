An enterprise-grade, hybrid static analysis and AI-driven code auditing platform designed to optimize multi-language software workflows using AST scope-aware analysis and LLMs.

🚀 Key Features
Universal Multi-Language Engine: Syntax tree validation for Python, JavaScript, C, and Java.

True Scope-Aware AST Analyzer: Programmatically traces variable initialization lifetimes to prevent false alerts while catching real NameErrors.

Line-by-Line Security Guard: Flags dangerous sub-shell operations (like os.system) and suggests safe alternatives (subprocess.run).

Reactive UI & Auto-Fixer: Provides side-by-side original vs fixed code diff views along with technical documentation generation and Big-O efficiency profiling.

📁 Repository Structure
├── Backend/
│   ├── app_streamlit.py       # Main frontend UI dashboard & local AST engine
│   ├── .env                   # Gemini API credentials key file
│   └── venv/                  # Python localized virtual sandbox environment
└── README.md                  # Quick start instructions manual
