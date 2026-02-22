# 🧠 STEM-Notes AI

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Transforming passive STEM video consumption into active, high-fidelity learning through Agentic RAG and automated visualization.**

STEM-Notes AI is an intelligent backend ecosystem designed to handle the rigorous demands of technical learning. It goes beyond standard transcription by using **Computer Vision** to extract diagrams, **LaTeX** to render math, and **Agentic RAG** to allow students to "talk" to their lectures with the precision of a personalized teaching assistant.

---

## ✨ Key Features

* 🎬 **Multi-Modal Processing:** Automatically extracts audio and key visual frames (e.g., slide changes, whiteboard math) from STEM video URLs using `yt-dlp` and `OpenCV`.
* 🤖 **Agentic RAG:** A reasoning loop powered by **LangGraph** that doesn't just search your notes—it verifies, fact-checks, and refines answers using both local databases and external web tools.
* 🔌 **MCP Native:** Built-in support for the **Model Context Protocol (MCP)**, allowing the application to connect to specialized STEM tools (like Wolfram Alpha) or act as a data provider for other AI agents.
* 📐 **STEM-First Rendering:** Native support for professional **LaTeX** math formatting and automated **Mermaid.js** flowchart generation for complex logical processes.
* ⚡ **High-Performance Backend:** An asynchronous **FastAPI** architecture paired with **Celery** task queuing to seamlessly handle heavy media processing in the background.


---

## 🏗️ Repository Architecture

The project follows a modular, scalable, service-oriented structure designed for AI workflows:

```text
stem-notes-ai/
├── app/
│   ├── api/          # 🌐 Web Layer: FastAPI routes and HTTP logic
│   ├── core/         # ⚙️ Config Layer: Env variables and security
│   ├── mcp/          # 🔌 Protocol Layer: MCP Servers and Clients
│   ├── tools/        # 🧰 Action Layer: Atomic tools for the AI Agent 
│   ├── services/     # 🧠 Logic Layer: AI orchestration and media processing
│   ├── models/       # 🏛️ Data Layer: SQLAlchemy database definitions
│   ├── schemas/      # 🛡️ Validation Layer: Pydantic input/output models
│   ├── db/           # 🗄️ Connection Layer: Postgres and Vector store management
│   └── utils/        # 🛠️ Helper Layer: LaTeX parsing and text cleanup
├── tests/            # 🧪 Automated test suites (Pytest)
├── .env.example      # 🔑 Template for environment variables
└── requirements.txt  # 📦 Project dependencies
```

---

### 🛠️ Tech Stack

* Core Framework: Python 3.10+, FastAPI, Uvicorn

* AI & Orchestration: LangGraph, LangChain, OpenAI/Gemini APIs

* Databases: PostgreSQL (Relational Data), ChromaDB / Pinecone (Vector Store)

* Media Processing: OpenAI Whisper (Transcription), OpenCV (Vision), yt-dlp (Extraction)

* Task Management: Celery + Redis

---


## 🚦 Getting Started

### 1. Prerequisites
Ensure you have the following installed on your system:
* Python 3.10 or higher
* `ffmpeg` (Required for video/audio processing)
* Git

### 2. Installation
Clone the repository and set up your virtual environment:

```bash
git clone https://github.com/your-username/stem-notes-ai.git
cd stem-notes-ai

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration
Copy the environment template and add your API keys:

```bash
cp .env .env
```

Edit .env to include your specific credentials:
* OPENAI_API_KEY=your_openai_api_key_here
* DATABASE_URL=sqlite:///./stem_notes.db  # Use PostgreSQL for production
* REDIS_URL=redis://localhost:6379/0

### 4. Running the Server
Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

Navigate to http://127.0.0.1:8000/docs in your browser to interact with the auto-generated Swagger UI documentation.

---


## 🗺️ Development Roadmap

- [x] **Phase 1:** Core FastAPI skeleton and layered folder architecture.
- [ ] **Phase 2:** Video processing pipeline (Whisper integration + Frame extraction).
- [ ] **Phase 3:** RAG implementation with ChromaDB (Ingestion & Retrieval).
- [ ] **Phase 4:** Agentic intelligence layer with LangGraph and MCP Tools.
- [ ] **Phase 5:** Interactive frontend dashboard and Browser Extension.

---

## 🤝 Contributing

Contributions are welcome! If you'd like to help improve the agent's reasoning capabilities, add new MCP integrations, or refine the mathematical parsing, please follow these steps:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
