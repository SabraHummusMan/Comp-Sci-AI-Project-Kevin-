# Pocket DM

A locally-run AI Dungeon Master that generates full D&D campaigns and lets you chat with your DM — all powered by Ollama running on your own machine.

---

## Requirements

### 3rd Party Applications (install these first)

| Application | Version | Download |
|-------------|---------|----------|
| **Python** | 3.10+ | [python.org/downloads](https://www.python.org/downloads/) |
| **Ollama** | Latest | [ollama.com/download](https://ollama.com/download) |

> During Python installation on Windows, make sure to check **"Add Python to PATH"**.

---

### Ollama Model

After installing Ollama, pull the required model by running this in your terminal:

```bash
ollama pull llama3.2
```

---

### Python Packages

| Package | Purpose |
|---------|---------|
| `ollama` | Python client for communicating with Ollama |

Install the required package with:

```bash
pip install ollama
```

---

## Setup & Running

1. **Clone the repo**
   ```powershell
   git clone <your-repo-url>
   cd <your-repo-folder>
   ```

2. **Create and activate a virtual environment** (recommended)
   ```powershell
   python -m venv venv
   venv\Scripts\activate
   ```

   If you get a script execution error, run this first:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

3. **Install dependencies**
   ```powershell
   pip install ollama
   ```

4. **Make sure Ollama is running** — it should start automatically after install, or you can launch it from your system tray.

5. **Run the app**
   ```powershell
   python main.py
   ```

---

## How to Use

- **New Campaign** — Enter a theme (e.g. "dark fantasy", "pirate adventure") and the AI will generate a full campaign with NPCs, quests, factions, and locations.
- **View Campaign** — Opens a detailed tabbed window showing all campaign information.
- **Load Campaign** — Load a previously saved campaign and continue your session.
- Campaigns and chat history are automatically saved to a `campaigns/` folder as JSON files.

---

## Project Structure

```
├── main.py          # Main application
├── requirements.txt # Python dependencies
├── README.md        # This file
└── campaigns/       # Auto-created — stores your saved campaigns (not committed to git)
```

---

## Notes

- All AI inference runs **locally** on your machine via Ollama — no internet connection or API key required.
- Performance depends on your hardware. A GPU will significantly speed up response times. On CPU only, responses may take 30–60 seconds.
- Chat history is saved automatically after every message.
