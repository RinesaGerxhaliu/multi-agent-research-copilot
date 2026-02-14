from agents.planner_agent import PlannerAgent
from agents.research_agent import ResearchAgent
from agents.writer_agent import WriterAgent
from agents.verifier_agent import VerifierAgent
from shared_state import SharedState

if __name__ == "__main__":

    task_text = """
    Complete all migration scripts, finalize penetration testing,
    and track remediation of critical findings to meet documented
    milestones and security requirements for the Clinical Analytics Dashboard.
    """
    state = SharedState(task=task_text.strip())

    planner = PlannerAgent()
    state = planner.run(state)

    print("\n---- PLAN ----")
    if state.plan == ["Not found in sources."]:
        print("Planner failed: No grounded plan.")
        exit()
    for step in state.plan:
        print("-", step)

    researcher = ResearchAgent()
    state = researcher.run(state)

    print("\n---- RESEARCH NOTES (summary)----")
    for i, note in enumerate(state.research_notes, 1):
        owners = note.get("owners") or ["TBD"]
        dues = note.get("due") or ["TBD"]
        print(f"Note {i} | Confidence: {note['confidence']:.2f} | Owner: {owners[0]} | Due: {dues[0]}")

    writer = WriterAgent()
    state = writer.run(state)

    print("\n----FINAL DRAFT----\n")
    print(state.draft)

    verifier = VerifierAgent()
    state = verifier.run(state)

    print("\n---- VERIFIED OUTPUT ----\n")
    print(state.final_output)

    print("\n----TRACE LOGS ----")
    for row in state.trace:
        print(row)

    print("\n---- VERIFICATION NOTES ----")
    for note in state.verification_notes:
        print("-", note)
