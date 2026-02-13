from agents.planner_agent import PlannerAgent
from shared_state import SharedState

if __name__ == "__main__":
    task_text = """
    Which actions should the engineering team prioritize during Q2
    to ensure timely and secure delivery of the Advanced Analytics Dashboard?
    """
    state = SharedState(task=task_text)

    planner = PlannerAgent()
    updated_state = planner.run(state)

    print("\nGenerated Plan:\n")

    for i, step in enumerate(updated_state.plan, start=1):
        print(f"{i}. {step}")

    print("\nTrace Log:")
    print(updated_state.trace)
