from shared_state import SharedState
from research.evidence_processor_research_agent import process_step

class ResearchAgent:

    def run(self, state: SharedState) -> SharedState:

        if not state.plan or state.plan == ["Not found in sources."]:
            return state

        research_notes = []

        supported_count = 0

        for step in state.plan:
            note, outcome = process_step(step)

            if note:
                research_notes.append(note)

            if outcome == "supported":
                supported_count += 1

            state.trace.append({
                "step": "research",
                "agent": "researcher",
                "action": f"Processed step: {step[:40]}",
                "outcome": outcome,
            })

        total_steps = len(state.plan)
        coverage = round(supported_count / total_steps, 2) if total_steps else 0.0

        state.trace.append({
            "step": "research",
            "agent": "researcher",
            "action": f"Coverage: {supported_count}/{total_steps}",
            "outcome": f"{coverage*100}%"
        })

        state.research_notes = research_notes
        return state


