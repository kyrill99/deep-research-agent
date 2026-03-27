# Deep Research Agent

An autonomous multi-agent research system that takes a topic, asks targeted clarifying questions, searches the web, summarizes findings into a detailed report, and delivers it to your inbox all orchestrated by an AI manager agent.

Built with the [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) and [Gradio](https://gradio.app/).

---

## How It Works

The system is a **manager agent coordinating specialised sub-agents as tools**. Rather than hardcoded Python orchestration, the manager LLM reasons about which tool to call next and in what order.

```
User enters topic
       │
       ▼
┌─────────────────┐
│ Clarifying Agent│  Generates 3 targeted questions to focus the research
└────────┬────────┘
         │  User answers
         ▼
┌─────────────────┐
│  Manager Agent  │  Orchestrates the full pipeline via agents-as-tools
└────────┬────────┘
         │
    ┌────┴──────────────────────────┐
    ▼                               │
┌──────────────┐                   │
│Planner Agent │  5 targeted        │
│              │  search queries    │
└──────┬───────┘                   │
       │                           │
       ▼                           │
┌──────────────┐  ×5               │
│ Search Agent │  Web search +     │
│              │  per-query summary│
└──────┬───────┘                   │
       │                           │
       ▼                           │
┌──────────────┐                   │
│ Writer Agent │  5–10 page        │
│              │  Markdown report  │
└──────┬───────┘                   │
       │                           │
       ▼                           │
┌──────────────┐                   │
│ Email Agent  │  HTML email via   │
│              │  SendGrid         │
└──────────────┘                   │
       │                           │
       └───────────────────────────┘
         Final report streamed to UI
```

---

## Features

- **Clarifying questions** — before any search begins, the system generates 3 questions to understand scope, depth, and angle, so the research is targeted rather than generic
- **Tuned search planning** — the planner agent incorporates the user's clarification answers to produce more precise queries
- **Manager as Agent** — the `ResearchManager` is a real LLM agent using the _agents-as-tools_ pattern; sub-agents are registered as callable tools and the manager decides the execution flow
- **Streaming UI** — live status updates appear in the chat as each tool is called (`plan_searches → web_search → write_report → send_email`)
- **Email delivery** — the final report is automatically converted to styled HTML and sent via SendGrid
- **OpenAI Traces** — every run is traced on the OpenAI platform for debugging and inspection

---

## Agent Architecture

| Agent             | Role                                                | Output                                         |
| ----------------- | --------------------------------------------------- | ---------------------------------------------- |
| `ClarifyingAgent` | Generates 3 questions to focus the research         | `ClarifyingQuestions`                          |
| `PlannerAgent`    | Creates 5 search queries with reasoning             | `WebSearchPlan`                                |
| `SearchAgent`     | Searches the web and summarises results             | Plain text summary                             |
| `WriterAgent`     | Synthesises all results into a full report          | `ReportData` (markdown + summary + follow-ups) |
| `EmailAgent`      | Converts report to HTML and sends via SendGrid      | Email delivery                                 |
| `ManagerAgent`    | Orchestrates the pipeline using sub-agents as tools | Final markdown report                          |

---

## Setup

### Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) package manager
- OpenAI API key
- SendGrid API key + verified sender address

### Installation

```bash
git clone https://github.com/your-username/deep-research-agent
cd deep-research-agent

uv venv
uv pip install openai-agents gradio python-dotenv sendgrid
```

### Configuration

Create a `.env` file:

```env
OPENAI_API_KEY=sk-...
SENDGRID_API_KEY=SG....
```

Create a `config.toml` file:

```toml
[email]
from_email = "you@example.com"
to_email   = "recipient@example.com"
```

### Run

```bash
python deep_research.py
```

The Gradio UI will open in your browser at `http://localhost:7860`.

---

## Usage

1. **Enter a topic** in the chat (e.g. _"The impact of large language models on software engineering"_)
2. **Answer the 3 clarifying questions** the agent asks (e.g. audience, depth, specific angle)
3. **Watch the agent work** — tool calls stream in real time as the manager delegates to each sub-agent
4. **Receive your report** — a detailed markdown report appears in the chat and lands in your inbox as a formatted HTML email

---

## Project Structure

```
deep-research-agent/
├── deep_research.py       # Gradio chat UI — multi-turn clarify → research flow
├── research_manager.py    # ResearchManager: clarify() and run() via manager agent
├── manager_agent.py       # Manager Agent with sub-agents registered as tools
├── clarifying_agent.py    # Generates 3 clarifying questions for a query
├── planner_agent.py       # Plans 5 targeted web search queries
├── search_agent.py        # Performs web search and summarises results
├── writer_agent.py        # Writes the final markdown research report
├── email_agent.py         # Sends HTML email via SendGrid
└── config.toml            # Email sender/recipient configuration
```

---

## Tech Stack

- **[OpenAI Agents SDK](https://github.com/openai/openai-agents-python)** — agent framework, tool use, agents-as-tools, tracing
- **GPT-4o-mini** — powers all agents
- **[Gradio](https://gradio.app/)** — streaming chat UI
- **[SendGrid](https://sendgrid.com/)** — email delivery
- **[Pydantic](https://docs.pydantic.dev/)** — structured agent outputs
- **[uv](https://github.com/astral-sh/uv)** — fast Python package management
