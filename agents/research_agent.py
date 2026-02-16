from __future__ import annotations
from shared_state import SharedState
from research.evidence_processor import process_step
from utils.security_utils import detect_prompt_injection

class ResearchAgent:

    def run(self, state: SharedState) -> SharedState:

        if not state.plan:
            return state

        if detect_prompt_injection(state.task):
            state.trace.append({
                "step": "research",
                "agent": "researcher",
                "action": "Prompt injection detected",
                "outcome": "blocked"
            })
            return state

        research_notes = []

        for step in state.plan:

            note, outcome = process_step(step)

            if outcome == "supported" and note:
                if any(existing["insight"] == note["insight"]
                       for existing in research_notes):
                    continue

                research_notes.append(note)

        state.research_notes = research_notes

        state.trace.append({
            "step": "research",
            "agent": "researcher",
            "action": f"{len(research_notes)} evidence entries extracted",
            "outcome": "success" if research_notes else "not-found"
        })

        return state
