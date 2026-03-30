# Repository Guidelines

## Project Structure & Module Organization
- `api_backend.py` hosts the FastAPI backend; `streamlit_app.py` is the Streamlit entrypoint.
- `src/` contains core logic: `src/workflow/` (LangGraph flow + state), `src/agents/`, `src/tools/`, and `src/config/` for config loading.
- `pages/` holds Streamlit pages split by portal (`pages/employee/`, `pages/customer/`).
- `utils/` provides UI helpers, styling, API client utilities, and visualization helpers.
- `prompts/` contains agent system prompts and task templates; prefer updating templates over editing code for prompt changes.
- `data/` stores sample CSV/PDF inputs and templates; keep any new samples anonymized.
- Docker assets live in `Dockerfile`, `Dockerfile.streamlit`, and `docker-compose.yml`.

## Build, Test, and Development Commands
- `uvicorn api_backend:app --reload --port 8000`: run the FastAPI backend locally.
- `streamlit run streamlit_app.py`: run the Streamlit dashboard locally.
- `docker-compose up --build`: build and run all services with Docker.
- `curl http://localhost:8000/health`: quick backend health check.

## Coding Style & Naming Conventions
- Python 3.11 codebase; use 4-space indentation and PEP 8 naming.
- Functions and variables use `snake_case`; classes use `PascalCase`; modules are lowercase.
- Business rules and paths live in `config.yaml`; keep policy changes there.
- Prompt content should live in `prompts/` and be referenced by loaders rather than inlined.

## Testing Guidelines
- No dedicated test suite is present yet.
- Validate changes with a backend health check and a sample workflow request.
- If you add tests, place them in `tests/` and name files `test_*.py` (pytest-friendly).

## Commit & Pull Request Guidelines
- Recent history uses short, lowercase summaries (e.g., "added graph visualisation"); follow this concise style.
- PRs should include a clear description, run steps, and linked issues if applicable.
- For UI changes, attach screenshots of the Streamlit pages affected.

## Security & Configuration Tips
- Store secrets in `.env` (e.g., `OPENAI_API_KEY`) and never commit real keys.
- Review `ARCHITECTURE.md` for system context before large workflow changes.
