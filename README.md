**📘 Local Offline AI Developer Assistant**

A fully offline, privacy-focused AI Developer Assistant built using DeepSeek Coder 1.3B and Ollama.
This tool can explain code, debug errors, search your entire project, read files, analyze functions, and answer coding questions all running locally on your machine without internet.



**🚀 Features**

🔹 1. Code Explanation

Explains any Python/JS/TS/text file

Summarizes logic, functions, classes

Highlights key operations and structure

🔹 2. Debugging Assistance

Analyzes code

Detects potential bugs

Explains why an error occurs

Suggests fixes with clear reasoning

🔹 3. Project-wide Code Search

Search for:

functions

variables

patterns

keywords

Shows file name + line number + matching text

🔹 4. Function Definition Locator

Find exactly where a function is defined inside the project.

🔹 5. File System Tools

Read files

List project files

Show metadata (size, extension, location)

Skip unwanted folders (__pycache__, .git, etc.)

🔹 6. Ask AI Questions

Ask general programming questions or questions with file context.

🔹 7. Completely Offline

No API keys

No cloud

No external dependency

100% privacy

All inference runs inside Ollama locally




**🧠 Why DeepSeek Coder 1.3B?**

DeepSeek Coder 1.3B was selected over Gemma-3-270M because:

Better code understanding

More accurate debugging

More reliable explanations

Larger training data

Still small enough to run offline on CPU

Excellent for Python + general coding tasks

This model gives high-quality output while staying fast and lightweight.




| Component                        | Purpose                       |
| -------------------------------- | ----------------------------- |
| **Python 3.10+**                 | Main CLI logic                |
| **Ollama**                       | Local LLM runtime             |
| **DeepSeek Coder 1.3B**          | Offline code-focused AI model |
| **Colorama**                     | Colored CLI output            |
| **Model Context Protocol (MCP)** | Tool wrapper system           |
| **Custom Tools**                 | File operations & code search |





**Project Structure **
Local-Offline-AI-Developer-Assistant/
│── cli.py                # Command-line interface
│── ollama_client.py      # Communication with DeepSeek Coder
│── mcp_server.py         # (Optional) MCP server file
│── config.json           # Allowed extensions, excluded folders
│── requirements.txt      # Python dependencies
│── test.py               # Sample file for testing
│── tools/
│   ├── file_ops.py       # File reading/listing helper
│   └── search.py         # Project-wide code search
└── .gitignore            # Ignore unnecessary files




**🔒 Offline Privacy Guarantee**

This project runs 100% on your local system.
No data is sent to any server.
No API keys or internet required.
Perfect for confidential codebases.



**🏁 Conclusion**

This project demonstrates that even a lightweight 1.3B model can serve as a powerful offline coding assistant.
It delivers useful code explanations, debugging, search, and project understanding—all without internet, and entirely on your local machine.
