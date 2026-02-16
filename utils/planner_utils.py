from typing import List

DISALLOWED_PREFIXES = (
    "owner:",
    "impact:",
    "status:",
    "target completion:",
    "requirement:",
    "risk:",
    "mitigation target:",
    "likelihood:",
)

def parse_planner_steps(raw_text: str) -> List[str]:

    if not raw_text:
        return []

    lines = [ln.strip() for ln in raw_text.splitlines() if ln.strip()]
    steps: List[str] = []

    for ln in lines:
        cleaned = ln.lstrip("-• ").strip()
        lower_cleaned = cleaned.lower()

        if lower_cleaned.startswith(DISALLOWED_PREFIXES):
            continue

        if lower_cleaned.startswith("r-"):
            continue

        if cleaned:
            steps.append(cleaned)

    return list(dict.fromkeys(steps))


def filter_steps_by_task_scope(task: str, steps: List[str]) -> List[str]:

    if not task or not steps:
        return []

    task_words = [w.lower() for w in task.split() if len(w) > 4]

    filtered = []

    for step in steps:
        step_lower = step.lower()

        if any(word in step_lower for word in task_words):
            filtered.append(step)

    return list(dict.fromkeys(filtered))
