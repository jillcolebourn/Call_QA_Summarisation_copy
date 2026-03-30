# System Analysis Report

## Scope
This review focuses on functional improvements and POC hardening, with emphasis on HITL behavior and the income verification review latency. Security, tests, and persistence are intentionally out of scope.

## HITL Flow Summary
- HITL tools live in `src/tools/ac_tools.py` and are invoked by `src/workflow/graph_autonomous.py` (ActionOrchestrator): `income_verification_review`, `finalize_proposal`, `update_account_details`.
- Approvals are processed in `api_backend.py` (`/api/workflows/{workflow_id}/approve`) and surfaced in the employee UI at `pages/employee/workflow.py`.
- Customer approval is a separate gate (`/api/workflows/{workflow_id}/customer-approve`) and is not HITL middleware.

## Findings (HITL + Functional)
1. **Income verification review is handled differently from other HITL points**  
   - In `api_backend.py`, income review approval triggers a second workflow continuation (`astream` restart) after resuming the interrupted node. Other HITL approvals do not.  
   - This adds extra LLM hops (router + action_orchestrator) before a proposal draft exists, increasing latency and variability.
2. **Approval state is overloaded**  
   - `hitl_approved` is used for both income review and compliance approval. The UI compensates with heuristics (`utils/components.py`), but the router and ActionOrchestrator still read `hitl_approved` for decisions, which can mislead control flow in edge cases.
3. **Resume context is inferred by parsing messages**  
   - `action_orchestrator_node` scans message content for `Command(resume=...)` to detect income-review resumes. This is brittle and can break if message formats change or tool calls are truncated.
4. **Router autonomy adds post-approval variance**  
   - After income review approval, the workflow is re-entered via the router, which can route to non-essential agents before proposal generation, adding avoidable cycles.

## Why Income Review Feels Slower
Income review is the only HITL gate that explicitly restarts the workflow after approval and requires additional agent passes to generate a proposal draft. Other HITL points (finalize proposal, system update) typically update state and complete without extra LLM-driven routing.

## Recommended Improvements (POC Hardening)
1. **Deterministic post-income-review path**  
   - After income review approval, bypass the router and route directly to ActionOrchestrator, or add a dedicated node that only calls `generate_proposal_draft`. This removes one LLM hop and reduces variance.
2. **Split approval flags**  
   - Replace `hitl_approved` with explicit fields (e.g., `income_review_approved`, `compliance_approved`, `system_update_approved`) or add `last_hitl_tool` to state. This removes ambiguity and makes routing deterministic.
3. **Persist HITL context in state**  
   - Store the active HITL tool name in state when interrupting, and read it on resume instead of parsing messages.
4. **Pre-generate drafts for income review**  
   - Generate and cache a proposal draft (or approval/denial variants) before the income review approval. After approval, promote the cached draft rather than invoking new agent passes.
5. **Fast-path ActionOrchestrator prompt**  
   - When `income_review_approved` is True and no proposal exists, use a minimal prompt (or direct tool call) that only generates the draft.
