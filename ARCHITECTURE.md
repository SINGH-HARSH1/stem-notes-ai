
<img src="./docs/Final_arch_notes_ai.png" alt="STEM Notes AI Architecture" width="600" />

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