# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Banking AI Lab is a **hybrid autonomous multi-agent workflow system** for mortgage arrears capitalization. It uses LangGraph to orchestrate three specialized AI agents (DataGatherer, DecisionMaker, ActionOrchestrator) with an LLM-based router that makes autonomous routing decisions.

**Key characteristics:**
- FastAPI backend + Streamlit frontend (employee + customer portals)
- LangGraph workflow with Human-in-the-Loop (HITL) approval gates
- Config-driven: ~75-80% of system behavior configurable via YAML + prompt templates
- Uses OpenAI GPT-4o-mini for agent reasoning

## Commands

### Development

```bash
# Install dependencies (using uv)
uv sync

# Run API backend (default port 8000)
uvicorn api_backend:app --reload

# Run Streamlit frontend (default port 8501)
streamlit run streamlit_app.py

# Run both services with Docker
docker-compose up --build
```

### Environment Setup

```bash
# Copy environment template and add OpenAI API key
cp .env.example .env
# Edit .env: OPENAI_API_KEY=your-key
```

### API Testing

```bash
# Health check
curl http://localhost:8000/health

# Start a workflow
curl -X POST http://localhost:8000/api/workflows \
  -H "Content-Type: application/json" \
  -d '{"client_id": 31567, "initiated_by": "Test"}'
```

## Architecture

### Core Workflow Flow

```
Router (LLM) → DataGatherer → Router → DecisionMaker → Router → ActionOrchestrator → HITL → Customer Approval → END
```

The router makes autonomous routing decisions (not hardcoded if-then rules) based on workflow state. Two safety overrides exist:
1. Force income verification after affordability passes
2. Force system update before completion

### Key Directories

- `src/workflow/` - LangGraph workflow definition
  - `graph_autonomous.py` - Main workflow graph with router + agent nodes
  - `state.py` - WorkflowState TypedDict definition
- `src/tools/` - Agent tools
  - `dg_tools.py` - DataGatherer tools (get_client_profile, extract_payslip, etc.)
  - `dm_tools.py` - DecisionMaker tools (pre_qualification_checks, affordability_check, etc.)
  - `ac_tools.py` - ActionOrchestrator tools (generate_proposal_draft, finalize_proposal, etc.)
- `src/agents/specialised_agents.py` - Agent creation functions
- `src/config/config_loader.py` - Loads config.yaml into POLICIES, PATHS, LLM_CONFIG dicts
- `src/utils/template_loader.py` - Template loader with variable substitution

### Configuration Files

- `config.yaml` - Business rules (LTV/LTI thresholds), LLM settings, file paths
- `prompts/*.txt` - Agent system prompts (personality/behavior)
- `prompts/router_prompts/` - Router decision-making prompts
- `prompts/task_templates/` - Agent task instructions per task type

### Frontend Structure

- `streamlit_app.py` - Main app entry, page navigation
- `pages/employee/` - Employee portal (dashboard, workflow management, support)
- `pages/customer/` - Customer portal (account view, approval page)
- `pages/agent_coaching.py` - QA/coaching page for transcript analysis
- `utils/` - Shared utilities (api_client, styles, components)

### API Backend

- `api_backend.py` - FastAPI app with workflow endpoints
  - `POST /api/workflows` - Start workflow
  - `POST /api/workflows/{id}/approve` - Employee HITL approval
  - `POST /api/workflows/{id}/customer-approve` - Customer approval
  - `GET /api/workflows/{id}` - Get workflow status

## HITL (Human-in-the-Loop) Checkpoints

1. **Income Review** (conditional) - Only if verification fails
2. **Proposal Finalization** (mandatory) - Employee approval required
3. **Customer Approval** (mandatory) - Customer must accept terms
4. **System Update** (implicit) - Requires both approvals

## Making Changes

### Modifying Business Rules
Edit `config.yaml` under `policies:` - changes take effect immediately without code changes.

### Modifying Agent Behavior
Edit prompt files in `prompts/` or task templates in `prompts/task_templates/`.

### Adding New Tools
1. Add tool function with `@tool` decorator in appropriate `src/tools/*.py`
2. Import and add to agent's tool list in `src/workflow/graph_autonomous.py`
3. Update agent system prompt if needed

### Modifying Workflow State
Edit `src/workflow/state.py` - add fields to `WorkflowState` TypedDict. Ensure router context building in `graph_autonomous.py` uses new fields.

## Data Files

- `data/Client_mortgage_data_synth.csv` - Mortgage account data
- `data/Customer_provided_data_synth.csv` - Customer financial data
- `data/customer_upload/` - Income verification PDFs (payslips, bank statements)
- `data/new_proposal_template.txt` - Proposal document template
