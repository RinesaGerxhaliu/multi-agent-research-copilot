from statistics import mean
from shared_state import SharedState
from utils.verifier_utils import validate_citations, collect_sources, assemble_output

class VerifierAgent:

    CONFIDENCE_THRESHOLD = 0.40

    def run(self, state: SharedState) -> SharedState:

        if not state.draft or not state.draft.strip():
            state.final_output = "Not found in sources."
            state.verification_notes.append("Draft missing — safe fallback triggered.")
            if avg_conf >= 0.60:
                outcome = "strong"
            elif avg_conf >= 0.40:
                outcome = "moderate"
            elif avg_conf >= 0.25:
                outcome = "weak"
            else:
                outcome = "blocked"

            state.trace.append({
                "step": "verify",
                "agent": "verifier",
                "action": f"Verification completed (avg_conf={avg_conf})",
                "outcome": outcome
            })

            return state

        draft_clean = state.draft.strip()
        if draft_clean.startswith("Not found in sources"):
            state.final_output = draft_clean
            state.trace.append({
                "step": "verify",
                "agent": "verifier",
                "action": "Upstream rejection propagated",
                "outcome": "not-found"
            })
            return state

        if not state.research_notes:
            state.final_output = "Not found in sources."
            state.verification_notes.append("No research evidence available — output blocked.")
            state.trace.append({
                "step": "verify",
                "agent": "verifier",
                "action": "Missing research evidence",
                "outcome": "blocked"
            })
            return state

        citation_issues = validate_citations(state)

        confidences = [note.get("confidence", 0.0) for note in state.research_notes]
        avg_conf = mean(confidences) if confidences else 0.0
        avg_conf = round(avg_conf, 2)

        if avg_conf < 0.25:
            state.final_output = "Not found in sources."
            state.verification_notes.append(
                f"Evidence confidence critically low (avg={avg_conf}) — output blocked."
            )
            state.trace.append({
                "step": "verify",
                "agent": "verifier",
                "action": "Confidence below critical threshold",
                "outcome": "blocked"
            })
            return state

        sources = collect_sources(state)

        state.final_output = assemble_output(draft_clean, sources)

        if 0.25 <= avg_conf < 0.40:
            state.verification_notes.append(
                f"Evidence confidence moderate (avg={avg_conf}). Manual review recommended."
            )
        elif 0.40 <= avg_conf < 0.60:
            state.verification_notes.append(
                f"Evidence confidence acceptable (avg={avg_conf})."
            )
        elif avg_conf >= 0.60:
            state.verification_notes.append(
                f"Evidence confidence strong (avg={avg_conf})."
            )


        if citation_issues:
            state.verification_notes.append(
                "Incomplete citation structures detected."
            )

        state.verification_notes.append("Verification completed.")

        state.trace.append({
            "step": "verify",
            "agent": "verifier",
            "action": f"Verification completed (avg_conf={avg_conf})",
            "outcome": "success" if avg_conf >= self.CONFIDENCE_THRESHOLD else "warning"
        })

        return state
