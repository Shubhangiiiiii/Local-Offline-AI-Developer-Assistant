# AI Developer Assistant (Windows)

Local AI-powered coding assistant using **DeepSeek Coder 1.3B** via **Ollama**, running completely on your Windows machine.

---

## 🚀 Setup (Windows)

### 1. Install Ollama

Download from:

- https://ollama.com/download/windows  

Run the installer (**OllamaSetup.exe**) and let it finish.  
Ollama should start automatically in the background.

### 2. Pull DeepSeek Coder 1.3B

Open the VS Code terminal inside your project (`ai-dev-assistant`) and run:

```powershell
ollama pull deepseek-coder:1.3b
