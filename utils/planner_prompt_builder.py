def build_planner_prompt(task: str, context: str) -> str:

    task_lower = task.lower()

    if any(word in task_lower for word in ["risk", "threaten", "delay", "impact"]):

        return f"""
            You are an enterprise risk extraction analyst.

            Extract ONLY documented risk statements
            directly relevant to the user question.

            STRICT RULES:
            - Return ONLY explicit risk descriptions.
            - Do NOT return mitigation actions.
            - Do NOT return metadata fields.
            - Do NOT rephrase risk wording.
            - If no documented risks exist, return exactly:
            Not found in sources.

            Retrieved Evidence:
            {context}

            User Question:
            {task.strip()}

            Return bullet lines only.
            """.strip()

    return f"""
            You are an enterprise execution planner.

            Extract documented execution steps explicitly stated
            in the retrieved evidence and relevant to the task.

            STRICT RULES:
            - Use wording exactly as written.
            - Do NOT introduce assumptions.
            - Do NOT return metadata fields.
            - If insufficient evidence exists, return exactly:
            Not found in sources.

            Retrieved Evidence:
            {context}

            User Task:
            {task.strip()}

            Return bullet lines only.
            """.strip()
