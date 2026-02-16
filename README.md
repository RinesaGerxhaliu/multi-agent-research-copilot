# Enterprise Multi-Agent Copilot

### Healthcare Governance & Risk Intelligence Engine

------------------------------------------------------------------------

## Project Overview

Enterprise Multi-Agent Copilot is a production-style multi-agent AI
system that transforms enterprise business requests into structured,
decision-ready deliverables using coordinated AI agents.

The system implements the required workflow:

Plan → Research → Draft → Verify → Deliver

It simulates a regulated Healthcare Clinical Analytics Dashboard program
operating under strict governance, compliance, performance, and
release-readiness constraints.

------------------------------------------------------------------------

## Live Demo

A working demo of the **Enterprise Multi-Agent Research Copilot** is available at:

**[https://multi-agent-research-copilot-malixszgcna4bviabvsowf.streamlit.app/](https://multi-agent-research-copilot-malixszgcna4bviabvsowf.streamlit.app/)**

The application is deployed using **Streamlit Community Cloud** and demonstrates:

- Multi-agent orchestration (Planner → Researcher → Writer → Verifier)
- Evidence-grounded governance and risk intelligence
- FAISS-based semantic retrieval over enterprise documents
- Structured executive-ready deliverables
- Citation validation and confidence scoring
- Prompt injection detection and security enforcement
- Full observability (latency, token usage, trace logs)

All outputs are strictly grounded in documented enterprise evidence.  
If no supporting documentation exists, the system safely returns:

> **"Not found in sources."**

---------------------------------------------------------------

## Core Features

-   Multi-agent orchestration (Planner, Researcher, Writer, Verifier)
-   LangGraph-based execution workflow
-   FAISS semantic vector retrieval (Top-K)
-   Evidence-grounded research notes with citations
-   Structured executive-ready output format
-   Confidence scoring mechanism
-   Hallucination blocking via Verifier Agent
-   Governance rule enforcement
-   Transparent trace logging
-   Streamlit user interface

------------------------------------------------------------------------

## Nice-to-Have Features Implemented

### Prompt Injection Protection

The system detects and blocks: - Milestone override attempts - Security
bypass attempts - Governance manipulation - Undocumented risk
introduction - Scope expansion requests

If detected: - Execution is controlled - Incident logged in trace -
Output safely returns: "Not found in sources."

------------------------------------------------------------------------

### Observability & Transparency

-   Agent-by-agent trace log
-   Confidence scoring
-   Evidence visibility
-   Deterministic execution flow
-   Structured state tracking via shared_state.py

------------------------------------------------------------------------

### Evaluation Test Suite

Located in:

eval/

Includes: - 10 structured enterprise test questions - Governance
validation tests - Risk extraction validation - Injection defense
tests - Evidence-grounding verification

Ensures: - Verifier blocks unsupported claims - Citations are always
present - Governance rules cannot be violated

------------------------------------------------------------------------

## Industry Scenario

Healthcare & Life Sciences

The system simulates a Clinical Analytics Dashboard program with:

-   Fixed Week 16 production milestone
-   Mandatory HIPAA & security validation
-   Migration & infrastructure dependencies
-   Performance targets (\<350ms API, 99.9% uptime)
-   Capacity constraints
-   Escalation rules

All outputs are strictly grounded in synthetic enterprise documentation.

------------------------------------------------------------------------

## Knowledge Base

Location:

data/sample_docs/

Detailed dataset documentation:

data/README.md

Documents include: - Program delivery overview - Risk & mitigation
register - Security & compliance summary - Data governance controls -
Performance & availability targets - Capacity allocation - Change &
release readiness documentation

------------------------------------------------------------------------

## Project Structure

    multi-agent-research-copilot/
    │
    ├── app/
    │   └── streamlit_app.py
    │
    ├── agents/
    │   ├── planner_agent.py
    │   ├── research_agent.py
    │   ├── writer_agent.py
    │   └── verifier_agent.py
    │
    ├── retrieval/
    │   ├── document_loader.py
    │   ├── vector_store.py
    │   └── retriever.py
    │
    ├── orchestration/
    │   └── graph.py
    │
    ├── utils/
    │   ├── research_prompt_builder.py
    │   ├── writer_prompt_builder.py
    │   ├── verifier_utils.py
    │   └── confidence_utils.py
    │
    ├── data/
    │   ├── sample_docs/
    │   ├── index/
    │   └── README.md
    │
    ├── eval/
    ├── shared_state.py
    ├── run_local.py
    ├── requirements.txt
    ├── .env
    └── README.md

------------------------------------------------------------------------

## Technical Stack

-   LangGraph
-   LangChain
-   langchain-openai
-   langchain-community
-   FAISS (faiss-cpu)
-   OpenAI API
-   Streamlit
-   Python 3.10+

------------------------------------------------------------------------

## Requirements

Dependencies used in this project:

-   langgraph
-   typing_extensions
-   langchain
-   langchain-community
-   langchain-openai
-   faiss-cpu
-   pandas
-   numpy
-   rank-bm25
-   python-dotenv
-   tiktoken
-   streamlit

Install using:

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

## Setup Instructions

### 1. Clone Repository & Create Virtual Environment

``` bash
git clone https://github.com/RinesaGerxhaliu/multi-agent-research-copilot.git
cd multi-agent-research-copilot
python -m venv venv
```

Activate:

Windows:

``` bash
venv\Scripts\activate
```

macOS/Linux:

``` bash
source venv/bin/activate
```

------------------------------------------------------------------------

### 2. Install Dependencies

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

### 3. Configure Environment Variables

Create a `.env` file in project root:

OPENAI_API_KEY=your_openai_api_key_here 
OPENAI_MODEL=gpt-4o-mini

------------------------------------------------------------------------

### 4. Run Locally (CLI Mode)

``` bash
python -m run_local
```

------------------------------------------------------------------------

### 5. Run Streamlit UI

``` bash
streamlit run app/streamlit_app.py
```

Open:

http://localhost:8501

Project runs locally within 5 minutes.

------------------------------------------------------------------------

## Output Format

Each execution produces:

-   Executive Summary (≤150 words)
-   Client-ready Email
-   Action List (Owner \| Due \| Confidence)
-   Sources & Citations
-   Full Trace Log

Structured and decision-ready output.

------------------------------------------------------------------------

## Safety & Guardrails

-   No external knowledge usage
-   No undocumented assumptions
-   Governance constraints enforced
-   Security review cannot be bypassed
-   Milestone cannot be changed
-   Unsupported claims replaced with: "Not found in sources."

------------------------------------------------------------------------

## Acceptance Criteria

✔ End-to-end multi-agent routing\
✔ Output includes citations\
✔ Verifier blocks hallucinations\
✔ Governance rules enforced\
✔ Trace log visible\
✔ Evaluation suite included\
✔ Prompt injection defense implemented\
✔ Observability features included\
✔ Runs locally under 5 minutes

------------------------------------------------------------------------

## Author

Rinesa Gerxhaliu\
AI Engineering -- Giga Academy Cohort IV
