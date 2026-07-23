

# Multi-Agent Research Assistant

An AI-powered research assistant that uses multiple agents working together to research any topic.

## Features

- **Multi-Agent System**: 4 specialized agents work together
- **Web Search**: Real-time web search using Tavily
- **RAG**: Document retrieval from uploaded PDFs
- **Self-Correction**: Verifies and improves research automatically
- **Professional Reports**: Well-structured research reports
- **Web Interface**: Easy-to-use Streamlit interface

## Architecture

```
User → Planner → Researcher → Verifier → Summarizer → Report
                ↑                          |
                └──── Self-Correction ─────┘
```

## Agents

1. **Planner**: Creates research plan
2. **Researcher**: Gathers information from web and documents
3. **Verifier**: Checks completeness and reliability
4. **Summarizer**: Writes professional reports

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd multi_agent_research
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. **Add documents (optional)**
   - Place PDF files in `documents/` folder
   - RAG will automatically index them

## Usage

### Web Interface (Streamlit)
```bash
streamlit run app.py
```

### Command Line
```bash
python main.py "Artificial Intelligence"
```

### Docker
```bash
docker build -t research-assistant .
docker run -p 8501:8501 research-assistant
```

## API Keys Required

- **OpenAI API Key**: For LLM capabilities
- **Tavily API Key**: For web search
- **LangSmith API Key**: (Optional) For tracing

## Technologies

- LangChain & LangGraph
- OpenAI GPT
- FAISS Vector Store
- Tavily Search
- Streamlit UI
- Docker

## Project Structure

```
multi_agent_research/
├── agents/          # AI agents
├── tools/           # Search and RAG tools
├── vectorstore/     # Vector database
├── documents/       # PDF documents
├── app.py          # Streamlit UI
├── graph.py        # LangGraph workflow
├── state.py        # Application state
├── prompts.py      # Prompt templates
├── config.py       # Configuration
└── main.py         # CLI interface
```

---
## Contributing

Contributions welcome! Please open an issue or pull request.
```

---

## Testing Your Setup

1. Make sure all API keys are set in `.env`
2. Run `streamlit run app.py`
3. Enter "Artificial Intelligence" as topic
4. Click "Start Research"
5. Watch the agents work!

---

The system will:
1. Plan the research
2. Search the web
3. Retrieve from documents
4. Verify completeness
5. Generate a report

---
