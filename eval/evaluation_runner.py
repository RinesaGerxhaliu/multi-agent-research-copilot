from eval.test_questions import EVALUATION_QUESTIONS
from eval.run_pipeline import run_pipeline
from statistics import mean

def classify_result(state):

    if any("Prompt injection detected" in t.get("action", "")
           for t in state.trace):
        return "blocked", 0.0

    if state.final_output and "Not found in sources" in state.final_output:
        return "not_found", 0.0

    confidences = [
        n.get("confidence", 0.0)
        for n in state.research_notes
        if n.get("evidence", {}).get("supported") is True
    ]

    avg_conf = round(mean(confidences), 2) if confidences else 0.0

    return "passed", avg_conf

def run_evaluation():

    print("**Enterprise Multi-Agent Evaluation**")

    passed = 0
    blocked = 0
    not_found = 0
    confidences = []

    for i, question in enumerate(EVALUATION_QUESTIONS, 1):

        print(f"Test {i}: {question}")

        state = run_pipeline(question, verbose=False)

        result, conf = classify_result(state)

        if result == "passed":
            print("Result: PASSED \n")
            passed += 1
            if conf > 0:
                confidences.append(conf)

        elif result == "blocked":
            print("Result: BLOCKED (Injection)\n")
            blocked += 1

        else:
            print("Result: NOT FOUND \n")
            not_found += 1

    total = len(EVALUATION_QUESTIONS)
    avg_conf = round(mean(confidences), 2) if confidences else 0.0

    print("--------------------")
    print(" Evaluation Summary ")
    print("--------------------")
    print(f"Total Tests: {total}")
    print(f"Passed: {passed} ")
    print(f"Blocked (Injection): {blocked}")
    print(f"Not Found: {not_found} ")
    print(f"Average Confidence: {avg_conf} ")

if __name__ == "__main__":
    run_evaluation()
