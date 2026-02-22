
### System Architecture
```mermaid
graph TD
    graph TD
    %% Custom Styling matching Draw.io colors and borders
    classDef redBox fill:#f8cecc,stroke:#b85450,stroke-width:1px,color:#000
    classDef blueBox fill:#dae8fc,stroke:#6c8ebf,stroke-width:1px,color:#000
    classDef greenBox fill:#d5e8d4,stroke:#82b366,stroke-width:1px,color:#000
    classDef yellowBox fill:#ffcd28,stroke:#d79b00,stroke-width:1px,color:#000
    classDef purpleHex fill:#e6d0de,stroke:#996185,stroke-width:1px,color:#000
    classDef yellowCyl fill:#fff2cc,stroke:#d6b656,stroke-width:1px,color:#000

    %% Subgraph 1: The Agentic Tutor
    subgraph Tutor ["<b>The Agentic Tutor</b>"]
        User["<b>User/Student</b>"]:::redBox
        LangGraph["<b>LangGraph Orchestrator</b>"]:::greenBox
        MCP["<b>MCP Interface</b>"]:::blueBox
    end

    %% Subgraph 2: The Extraction Factory
    subgraph Factory ["<b>The Extraction Factory</b>"]
        FastAPI["<b>FastAPI Gateway</b>"]:::blueBox
        Worker["<b>Celery/Redis Worker</b>"]:::blueBox
        YTDLP["<b>yt-dlp Engine</b>"]:::blueBox
        OpenCV["<b>OpenCV Vision</b>"]:::blueBox
        Whisper["<b>Open AI Whisper</b>"]:::blueBox
    end

    %% Subgraph 3: Synthesis Engine
    subgraph Synthesis ["<b>Synthesis Engine</b>"]
        Scribe["<b>LLM Note Scribe</b>"]:::yellowBox
        Notes{{"<b>Master Study Notes</b><br/><b>PDF/MD File</b>"}}:::purpleHex
    end

    %% Subgraph 4: The Knowledge Vault
    subgraph Vault ["<b>The Knowledge Vault</b>"]
        SQL[("<b>SQL DB</b>")]:::yellowCyl
        VecEmb["<b>Vector Embeddings</b>"]:::blueBox
        VecDB[("<b>Vector Database</b><br/><i>Chroma/Pinecone<br/>or Milvus</i>")]:::yellowCyl
    end

    %% Diagram Flows (Edges) with exact labels
    User == "<b>Request</b><br/><b>YouTube Url/Video</b>" ==> FastAPI
    FastAPI --> Worker
    Worker --> YTDLP

    YTDLP -->|"<b>Video Stream</b>"| OpenCV
    YTDLP -->|"<b>Audio<br/>Stream</b>"| Whisper

    OpenCV -->|"<b>Visual Math</b>"| Scribe
    Whisper -->|"<b>Timestamps</b>"| Scribe

    Scribe -->|"<b>Markdown/LaTex</b>"| Notes

    Notes == "<b>Response</b><br/><b>Notes</b><br/><i>(Pdf/Md files)</i>" ==> User

    Notes -->|"<b>Metadata</b>"| SQL
    Notes -->|"<b>Chunking</b>"| VecEmb
    VecEmb --> VecDB

    User -->|"<b>Query</b>"| LangGraph
    LangGraph -->|"<b>Structured Response</b>"| User

    LangGraph <-->|"<b>Tools: Wolfram/Tavily</b>"| MCP

    VecDB -->|"<b>Context Retrieval</b>"| LangGraph
    Notes -->|"<b>Source of Truth</b>"| LangGraph

```

# 📖 STEM-Notes AI: Folder Manifest

## 📁 `app/api/`
**The Front Desk (Web Layer)**
* **Purpose:** This is the only part of the app that talks to the outside world. It handles HTTP requests, URLs, and status codes.
* **Intent:** Keep this "thin." It shouldn't contain AI logic; it should just receive data and hand it off to a Service.
* **Key File:** `dependencies.py` handles things like "Is the user logged in?" before the request hits the endpoint.

## 📁 `app/mcp/`
**The Universal Translator (Model Context Protocol)**
* **Purpose:** Standardizes how your AI connects to external data and how external AIs connect to your data.
* **Intent:** To make your notes "portable" across the AI ecosystem and to use world-class tools (like Wolfram Alpha) without writing complex custom integrations.

## 📁 `app/tools/`
**The Agent's Hands (Action Layer)**
* **Purpose:** Contains small, isolated functions that the AI Agent can "pick up" and use to solve a problem.
* **Intent:** Each file here should do exactly one thing (e.g., `web_scraper.py` only scrapes; it doesn't summarize). This makes the tools reliable and easy for the LLM to understand.

## 📁 `app/services/`
**The Brain (Logic Layer)**
* **Purpose:** This is where the heavy lifting happens. It coordinates the tools, the databases, and the AI models.
* **Intent:** Orchestration. For example, `processor.py` manages the sequence of: "Download video -> Extract audio -> Start transcription."

## 📁 `app/models/`
**The Filing Cabinet (Storage Definition)**
* **Purpose:** Defines how data looks inside your Database (PostgreSQL).
* **Intent:** These are your "Source of Truth" for saved data. If you want to add a "Video Duration" field to your database, you define it here.

## 📁 `app/schemas/`
**The Bouncer (Validation Layer)**
* **Purpose:** Defines how data looks when it is moving (in an API request or response).
* **Intent:** Uses Pydantic to ensure that if the app expects a URL, it actually gets a URL and not a random string. This prevents the app from crashing due to bad input.

## 📁 `app/db/`
**The Infrastructure (Connection Layer)**
* **Purpose:** Manages the literal connection to your databases (Postgres and ChromaDB).
* **Intent:** Handles "Sessions"—opening the door to the database, doing the work, and making sure the door is locked afterward.

## 📁 `app/utils/`
**The Swiss Army Knife (Helpers)**
* **Purpose:** Contains generic code that doesn't fit into "Business Logic."
* **Intent:** Things like formatting a timestamp, cleaning up LaTeX strings, or parsing math symbols. If you find yourself writing the same 5 lines of code in multiple places, move it here.

## 📁 `tests/`
**The Safety Net (Quality Assurance)**
* **Purpose:** Contains scripts that automatically "attack" your code to see if it breaks.
* **Intent:** To ensure that when you add a new feature, you haven't accidentally broken an old one.