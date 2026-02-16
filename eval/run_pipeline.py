from agents.planner_agent import PlannerAgent
from agents.research_agent import ResearchAgent
from agents.writer_agent import WriterAgent
from agents.verifier_agent import VerifierAgent
from shared_state import SharedState

def run_pipeline(task_text: str, verbose: bool = True):

    state = SharedState(task=task_text.strip())

    planner = PlannerAgent()
    researcher = ResearchAgent()
    writer = WriterAgent()
    verifier = VerifierAgent()

    state = planner.run(state)

    if verbose:
        print("\n---- PLAN ----")
        if state.plan:
            for step in state.plan:
                print("-", step)
        else:
            print("No plan generated.")

    state = researcher.run(state)

    if verbose:
        print("\n---- RESEARCH NOTES ----")
        if state.research_notes:
            for i, note in enumerate(state.research_notes, 1):
                print(f"\nNote {i}")
                print("Insight:", note.get("insight"))
                print("Confidence:", note.get("confidence"))
        else:
            print("No research evidence found.")

        print("\nDEBUG INTENT:", state.intent)
        print("DEBUG RESEARCH NOTES:", len(state.research_notes))

    state = writer.run(state)

    if verbose:
        print("\n---- DRAFT ----")
        print(state.draft if state.draft else "No draft generated.")

    state = verifier.run(state)

    if verbose:
        print("\n---- FINAL VERIFIED OUTPUT ----")
        print(state.final_output if state.final_output else "No final output.")

        print("\n---- TRACE LOGS ----")
        for row in state.trace:
            print(row)

        print("\n---- VERIFICATION NOTES ----")
        if state.verification_notes:
            for note in state.verification_notes:
                print("-", note)
        else:
            print("No verification notes.")

    return state

if __name__ == "__main__":

    task_text = """
    Summarize the documented Q2 risks that could threaten the Week 16 production release and identify their mitigation targets.
    """

    run_pipeline(task_text, verbose=True)
