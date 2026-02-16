from __future__ import annotations
import os
from langchain_openai import ChatOpenAI
from shared_state import SharedState
from utils.writer_prompt_builder import build_writer_prompt
from utils.security_utils import observe_llm_call

class WriterAgent:

    def __init__(self, model: str | None = None):
        model_name = (
            model
            or os.getenv("WRITER_AGENT_MODEL")
            or os.getenv("OPENAI_MODEL")
            or "gpt-4o-mini"
        )

        if not model_name:
            raise EnvironmentError("Missing model configuration for WriterAgent.")

        self.llm = ChatOpenAI(model=model_name, temperature=0.0)

    def run(self, state: SharedState) -> SharedState:

        if not state.research_notes:
            return self._reject(state, "No research notes available")

        supported_notes = [
            note for note in state.research_notes
            if isinstance(note, dict)
            and note.get("evidence", {}).get("supported") is True
        ]

        if not supported_notes:
            return self._reject(state, "No supported evidence notes")

        usable_notes = [
            note for note in supported_notes
            if isinstance(note.get("insight"), str)
            and note.get("insight").strip()
            and note.get("insight").strip().lower() != "not found in sources."
        ]

        if not usable_notes:
            return self._reject(state, "Supported notes had no usable insights")
        
        if state.intent == "governance":
            usable_notes = [
                {**note, "owners": None, "due": None}
                for note in usable_notes
            ]

        prompt, avg_conf = build_writer_prompt(
            state.task,
            usable_notes,
            intent=state.intent
        )

        if prompt == "Not found in sources.":
            return self._reject(state, "Writer prompt returned no evidence")

        response = observe_llm_call(
            state,
            "writer",
            lambda: self.llm.invoke(prompt)
        )
        draft_text = (getattr(response, "content", "") or "").strip()

        if not draft_text:
            return self._reject(state, "Empty LLM response")

        if "### Executive Summary" not in draft_text:
            return self._reject(state, "Structured format missing")

        state.draft = draft_text

        state.trace.append({
            "step": "draft",
            "agent": "writer",
            "action": f"Generated structured deliverable (avg_conf={avg_conf})",
            "outcome": "success",
        })

        return state

    def _reject(self, state: SharedState, reason: str) -> SharedState:

        suggestion = ""

        if reason == "No research notes available":
            suggestion = "Suggested next step: Provide more specific task details or ensure relevant documentation is indexed."

        elif reason == "No supported evidence notes":
            suggestion = "Suggested next step: Verify that the requested risks or governance rules are documented in the source files."

        elif reason == "Supported notes had no usable insights":
            suggestion = "Suggested next step: Refine the query to reference specific documented risks, owners, or mitigation targets."

        else:
            suggestion = "Suggested next step: Confirm that relevant documented evidence exists for this request."

        state.draft = f"""
            ### Executive Summary
            Not found in sources.

            {suggestion}
            """.strip()

        state.trace.append({
            "step": "draft",
            "agent": "writer",
            "action": f"Generation blocked ({reason})",
            "outcome": "not-found",
        })

        return state
