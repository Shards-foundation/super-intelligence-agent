# Super-Intelligence Autonomous Agentic AI System

**Status:** Experimental. Two unit-test modules, a local Docker sketch, and no production deployment.

## Overview
This project is an early scaffold for a modular autonomous agent system. It wires several LLM providers and agent frameworks together. It is not a finished or production system.

## Features
- **Multi-Agent Orchestration**: Leverage frameworks like LangGraph, CrewAI, and AutoGen for complex, collaborative agent workflows.
- **Model Agnostic LLM Integration**: Seamlessly switch between various LLM providers including Kimi K2, Qwen, Mistral, Llama, DeepSeek, Minimax, and GLM (Zhipu AI) via LiteLLM.
- **Memory**: `memory/vector_memory.py` talks to Qdrant. Semantic memory, episodic memory, and a retrieval pipeline are not implemented.
- **Tooling**: `tools/` has a DuckDuckGo search helper, an in-process Python `exec` helper, and an OpenClaw stub. Web browsing is not implemented.
- **Local containers**: `deploy/Dockerfile` and `deploy/docker-compose.yml` can run the API and Qdrant on one machine. There are no Kubernetes manifests.
- **Observability**: Not included. This repository has no metrics or tracing stack.

## Architecture

### Repository Structure
```text
super-intelligence-agent/
├── agents/             # CrewAI, LangGraph, AutoGen, and PydanticAI wrappers
├── core/               # LLM manager and provider routing
├── memory/             # Qdrant helper
├── tools/              # Search helper, in-process exec, OpenClaw stub
├── api/                # FastAPI app
├── deploy/             # Dockerfile and Compose file
├── tests/unit/         # Two unit-test modules
└── docs/               # Design notes
```

### Core Components

#### Agent Orchestration Layer
This layer is responsible for coordinating the activities of various AI agents, enabling complex task decomposition, planning, and multi-agent collaboration. We utilize:
- **LangGraph**: For defining stateful, cyclic agent workflows, allowing for sophisticated decision-making processes.
- **CrewAI**: For creating role-based multi-agent systems, where each agent has a specific role, goal, and backstory, fostering collaborative problem-solving.
- **AutoGen**: For building conversational AI agents that can interact with each other to solve tasks, particularly useful for code-centric and research-oriented tasks.
- **PydanticAI**: Ensures type-safe agent definitions and structured outputs, enhancing reliability and maintainability.

#### LLM Integration Layer
To ensure flexibility and access to the best available models, this layer provides a unified interface to various LLM providers:
- **LiteLLM**: Acts as a universal API wrapper, standardizing calls to different LLMs such as Kimi K2 (Moonshot AI), Qwen (Alibaba Cloud), Mistral, Llama (via Groq or local deployment), DeepSeek, Minimax, and GLM (Zhipu AI). This abstraction allows for easy swapping of models and reduces vendor lock-in.

#### Memory & Knowledge Layer
`memory/vector_memory.py` can upsert and search vectors in Qdrant. Semantic memory, episodic memory, and a retrieval pipeline are not implemented.

#### Tools & Skills Layer
Agents gain their autonomy through the ability to interact with the external world. This layer provides a suite of tools and integrations:
- **OpenClaw Integration**: A placeholder for integrating with OpenClaw (formerly Clawdbot), enabling the agent to interact with users through various messaging applications.
- **Browser automation**: Not implemented. Playwright is listed in `requirements.txt` but no module imports it.
- **Code execution**: `tools/custom_tools.py` runs Python with `exec` inside the API process. That is not a sandbox.
- **Custom Tools**: A framework for defining and integrating specialized tools tailored to specific tasks or domains, leveraging the tool ecosystems of LangChain and CrewAI.

#### Infrastructure & Deployment
What is actually in the repository:
- **Docker & Docker Compose**: `deploy/Dockerfile` and `deploy/docker-compose.yml` package the API and a Qdrant service for local use.
- **Kubernetes**: No manifests are included.
- **Monitoring**: No Prometheus or Grafana configuration is included.

## Getting Started

### Prerequisites
- Python 3.11+
- Docker
- Git
- GitHub CLI (for repository management)

### Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/Shards-foundation/super-intelligence-agent.git
   cd super-intelligence-agent
   ```
2. **Set up environment variables:**
   Copy the example environment file and fill in your API keys:
   ```bash
   cp .env.example .env
   # Open .env and add your LLM API keys and other configurations
   ```
3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Start Qdrant (Vector Database):**
   ```bash
   docker compose -f deploy/docker-compose.yml up -d qdrant
   ```
5. **Run the FastAPI application:**
   ```bash
   uvicorn api.main:app --host 0.0.0.0 --port 8000
   ```
   Alternatively, use Docker Compose to run the entire stack:
   ```bash
   docker compose -f deploy/docker-compose.yml up -d
   ```

## Usage

### API Endpoints
The agent system exposes a FastAPI endpoint for interaction:

- **GET /**: Checks the API status.
- **POST /chat**: Sends a query to the agent system. 
  - **Request Body Example:**
    ```json
    {
      "query": "What is the capital of France?",
      "agent_type": "crewai",
      "model": "mistral/mistral-large-latest"
    }
    ```
  - `agent_type` can be `crewai` or `langgraph`.
  - `model` is optional and defaults to `gpt-4o` if not specified.

## Contributing
We welcome contributions to this project! Please see `CONTRIBUTING.md` for details on how to get started.

## License
This project is licensed under the MIT License - see the `LICENSE` file for details.

## References
[1] CrewAI Documentation: [https://docs.crewai.com/](https://docs.crewai.com/)
[2] LangGraph Documentation: [https://langchain-ai.github.io/langgraph/](https://langchain-ai.github.io/langgraph/)
[3] LiteLLM Documentation: [https://litellm.ai/](https://litellm.ai/)
[4] Qdrant Documentation: [https://qdrant.tech/](https://qdrant.tech/)
[5] OpenClaw GitHub: [https://github.com/OpenClaw/OpenClaw](https://github.com/OpenClaw/OpenClaw)
