from statistics import mean
from shared_state import SharedState
from utils.verifier_utils import validate_citations, collect_sources, assemble_output

class VerifierAgent:

    CONFIDENCE_THRESHOLD = 0.50

    def run(self, state: SharedState) -> SharedState:

        if not state.draft or not state.draft.strip():
            return self._block(state, "Draft missing")

        draft_clean = state.draft.strip()

        if draft_clean.startswith("Not found in sources"):
            state.final_output = draft_clean
            self._trace(state, "Upstream rejection propagated", "not-found")
            return state

        if not draft_clean.startswith("### Executive Summary"):
            return self._block(state, "Invalid draft structure")

        supported_notes = [
            n for n in state.research_notes
            if n.get("evidence", {}).get("supported") is True
        ]

        if not supported_notes:
            return self._block(state, "No supported research evidence")

        confidences = [n.get("confidence", 0.0) for n in supported_notes]
        avg_conf = round(mean(confidences), 2) if confidences else 0.0

        if avg_conf < self.CONFIDENCE_THRESHOLD:
            return self._block(
                state,
                f"Evidence confidence below threshold (avg={avg_conf})"
            )

        citation_issues = validate_citations(state)
        if citation_issues:
            return self._block(state, "Citation validation failed")

        sources = collect_sources(state)
        state.final_output = assemble_output(draft_clean, sources)

        state.verification_notes.append(
            f"Verification successful (avg_conf={avg_conf})."
        )

        self._trace(state, f"Verification completed (avg_conf={avg_conf})", "success")

        return state

    def _block(self, state: SharedState, reason: str) -> SharedState:

        state.final_output = """### Executive Summary
            Not found in sources.

            The requested information is not explicitly documented in the currently indexed enterprise records.

            ### Suggested Next Steps
            - Verify that the requested risks, owners, mitigation targets, or governance rules are formally documented.
            - Ensure all relevant project documents are included in the indexed knowledge base.
            - Refine the task to reference a specific risk ID, milestone, or governance section.
            """

        state.verification_notes.append(reason)

        self._trace(state, reason, "blocked")
        return state

    def _trace(self, state: SharedState, action: str, outcome: str):
        state.trace.append({
            "step": "verify",
            "agent": "verifier",
            "action": action,
            "outcome": outcome
        })
