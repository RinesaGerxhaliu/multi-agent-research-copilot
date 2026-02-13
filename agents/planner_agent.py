from __future__ import annotations

import os
from typing import List
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from shared_state import SharedState
from retrieval.retriever import Retriever
from utils.planner_prompt_builder import build_planner_prompt

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
        self.retriever = Retriever()

    def run(self, state: SharedState) -> SharedState:

        retrieved = self.retriever.search(state.task, k=5)

        if not retrieved:
            state.plan = ["Not found in sources."]
            state.trace.append({
                "step": "plan",
                "agent": "planner",
                "action": "No evidence retrieved",
                "outcome": "not-found",
            })
            return state
        context = "\n\n".join(r["snippet"] for r in retrieved)

        prompt = build_planner_prompt(
            task=state.task,
            context=context
        )

        response = self.llm.invoke(prompt)
        raw_text = (getattr(response, "content", "") or "").strip()

        if not raw_text:
            state.plan = ["Not found in sources."]
            state.trace.append({
                "step": "plan",
                "agent": "planner",
                "action": "Empty LLM response",
                "outcome": "empty",
            })
            return state

        lines = [ln.strip() for ln in raw_text.splitlines() if ln.strip()]
        steps: List[str] = []

        for ln in lines:
            cleaned = ln.lstrip("-• ").strip()
            if cleaned:
                steps.append(cleaned)

        if not steps:
            state.plan = ["Not found in sources."]
            state.trace.append({
                "step": "plan",
                "agent": "planner",
                "action": "No valid steps generated",
                "outcome": "invalid-structure",
            })
            return state

        steps = list(dict.fromkeys(steps))

        state.plan = steps[:5]   

        state.trace.append({
            "step": "plan",
            "agent": "planner",
            "action": f"Generated {len(state.plan)} execution steps",
            "outcome": "success",
        })

        return state
