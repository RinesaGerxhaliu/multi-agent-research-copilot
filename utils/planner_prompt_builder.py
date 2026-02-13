def build_planner_prompt(task: str, context: str) -> str:
    return f"""
You are an enterprise delivery architect.

Base your response STRICTLY on the provided evidence.
Do NOT use external knowledge.
Do NOT assume missing facts.

Retrieved evidence:
{context}

Rules:
- Produce 3 to 5 concise execution steps.
- Each step must be operational (what to do and why).
- Use only explicitly documented milestones, risks, and decisions.
- Do NOT introduce new dates, risks, roles, or commitments.
- Do NOT change the Week 16 milestone.
- If insufficient evidence exists, return: Not found in sources.

User task:
{task.strip()}

Return the steps as plain bullet lines.
No explanations.
No numbering.
""".strip()
