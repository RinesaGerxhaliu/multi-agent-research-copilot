from __future__ import annotations
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from shared_state import SharedState
from utils.security_utils import detect_prompt_injection
from utils.security_utils import observe_llm_call

load_dotenv()

class PlannerAgent:

    def __init__(self, model: str | None = None):

        model_name = (
            model
            or os.getenv("PLANNER_AGENT_MODEL")
            or os.getenv("OPENAI_MODEL")
        )

        if not model_name:
            raise EnvironmentError("Missing model configuration for PlannerAgent.")

        self.llm = ChatOpenAI(model=model_name, temperature=0.0)

    def run(self, state: SharedState) -> SharedState:

        if detect_prompt_injection(state.task):
            state.plan = ["Not found in sources."]
            state.trace.append({
                "step": "plan",
                "agent": "planner",
                "action": "Prompt injection detected",
                "outcome": "blocked"
            })
            return state

        task_lower = state.task.lower()

        if any(word in task_lower for word in ["risk", "mitigation", "owner"]):
            state.intent = "risk_analysis"

        elif any(word in task_lower for word in ["governance", "rule", "milestone"]):
            state.intent = "governance"

        elif any(word in task_lower for word in ["migration", "performance", "capacity"]):
            state.intent = "structured_extraction"

        else:
            state.intent = "risk_analysis"

        if state.intent in ["risk_analysis", "governance", "structured_extraction"]:
            state.plan = [state.task.strip()]
        else:
            prompt = f"""
                You are a senior enterprise planner.

                Decompose the following business task into 3 to 5 concise,
                execution-focused steps.

                STRICT RULES:
                - Do NOT invent new facts.
                - Do NOT introduce new dates or milestones.
                - Return bullet lines only.
                - If unclear, return exactly:
                Not found in sources.

                Task:
                {state.task.strip()}
                """
            response = observe_llm_call(
                state,
                "planner",
                lambda: self.llm.invoke(prompt)
            )
            raw_output = response.content.strip()

            if raw_output.lower() == "not found in sources.":
                state.plan = ["Not found in sources."]
                state.trace.append({
                    "step": "plan",
                    "agent": "planner",
                    "action": "LLM returned unsupported",
                    "outcome": "failed"
                })
                return state

            lines = [
                ln.strip().lstrip("-• ")
                for ln in raw_output.splitlines()
                if ln.strip()
            ]
            state.plan = list(dict.fromkeys(lines))

        state.trace.append({
            "step": "plan",
            "agent": "planner",
            "action": f"Intent classified as {state.intent} | {len(state.plan)} step(s)",
            "outcome": "success"
        })

        return state
