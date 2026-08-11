# TaskFlow AI Concierge Agent

RAG-powered AI concierge agent with agent tools (book demo, create support ticket) and conversation memory. Built with LangChain, ChromaDB, HuggingFace embeddings, and Streamlit.

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Get a free HuggingFace API token: https://huggingface.co/settings/tokens

3. Create `.streamlit/secrets.toml` with:
   ```
   HUGGINGFACEHUB_API_TOKEN = "your_token_here"
   ```

4. Build the knowledge base (one-time, also runs automatically on first app launch):
   ```
   cd src && python ingest.py
   ```

5. Run the app:
   ```
   streamlit run app.py
   ```

## Deploy to Streamlit Cloud

1. Push this folder to a GitHub repo.
2. Go to share.streamlit.io, connect the repo, set main file to `app.py`.
3. Add `HUGGINGFACEHUB_API_TOKEN` under App Settings > Secrets.
4. Deploy.

## Architecture

- `data/` — knowledge base source docs (Notion product info)
- `src/ingest.py` — chunks docs, embeds with HuggingFace, stores in ChromaDB
- `src/tools.py` — agent tools: BookDemo, CreateTicket (logged to JSON files)
- `src/agent.py` — LangChain conversational agent combining RAG retrieval + tools + memory
- `app.py` — Streamlit chat interface

## Example prompts to test
- "What is Notion Agent?"
- "What are Notion's pricing plans?"
- "Book me a demo for tomorrow at 3pm"
- "Create a ticket — my workspace won't sync"
