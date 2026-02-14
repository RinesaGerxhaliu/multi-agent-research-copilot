from __future__ import annotations
import os
from langchain_openai import ChatOpenAI
from shared_state import SharedState
from utils.writer_prompt_builder import build_writer_prompt

class WriterAgent:

    def __init__(self, model: str | None = None):
        model_name = (
            model
            or os.getenv("WRITER_AGENT_MODEL")
            or os.getenv("OPENAI_MODEL")
            or "gpt-4o-mini"
        )

        self.llm = ChatOpenAI(model=model_name, temperature=0.0)

    def run(self, state: SharedState) -> SharedState:

        if not state.research_notes:
            return self._reject_no_evidence(state, reason="No research notes available")

        supported_notes = [
            note for note in state.research_notes
            if isinstance(note, dict)
            and note.get("evidence", {}).get("supported") is True
        ]

        if not supported_notes:
            return self._reject_no_evidence(state, reason="No supported evidence notes")

        usable_notes = []
        for note in supported_notes:
            insight = note.get("insight")

            if isinstance(insight, str):
                cleaned = insight.strip()
                if cleaned and cleaned.lower() != "not found in sources.":
                    usable_notes.append(note)

        if not usable_notes:
            return self._reject_no_evidence(state, reason="Supported notes had no usable insights")

        prompt, avg_conf = build_writer_prompt(state.task, usable_notes)

        response = self.llm.invoke(prompt)
        draft_text = (getattr(response, "content", "") or "").strip()

        if not draft_text:
            return self._reject_no_evidence(state, reason="Empty LLM response")

        state.draft = draft_text

        state.trace.append({
            "step": "draft",
            "agent": "writer",
            "action": f"Generated structured deliverable (avg_conf={avg_conf:.2f})",
            "outcome": "success",
        })

        return state

    def _reject_no_evidence(self, state: SharedState, reason: str) -> SharedState:
        message = (
            "Not found in sources.\n\n"
            "The provided documentation does not contain relevant evidence "
            "to answer this request."
        )

        state.draft = message

        state.trace.append({
            "step": "draft",
            "agent": "writer",
            "action": f"Generation blocked due to insufficient evidence ({reason})",
            "outcome": "not-found",
        })

        return state
