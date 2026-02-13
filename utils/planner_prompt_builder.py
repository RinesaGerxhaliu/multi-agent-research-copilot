def build_planner_prompt(task: str, context: str) -> str:
    return f"""
        You are an enterprise execution planner.

        Based STRICTLY on the retrieved evidence below,
        extract explicitly documented execution requirements
        relevant to the user task.

        STRICT RULES:
        - Use wording from the evidence.
        - Do NOT introduce new assumptions.
        - Do NOT rephrase milestone dates.
        - Do NOT extract partial fragments.
        - If insufficient evidence exists, return exactly:
        Not found in sources.

        Retrieved evidence:
        {context}

        User task:
        {task.strip()}

        Return bullet lines only.
        """.strip()
