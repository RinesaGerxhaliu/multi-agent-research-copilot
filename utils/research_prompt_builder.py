def build_research_prompt(step: str, snippets: list[str]) -> str:

    context = "\n\n".join(snippets)

    return f"""
        You are a strict evidence extraction analyst.

        Extract explicitly documented requirement lines
        that directly support the plan step.

        Rules:
        - Use wording from the excerpts.
        - Do NOT introduce new wording.
        - Do NOT interpret.
        - Do NOT summarize.
        - You may include closely related requirement lines
          if they appear together in the excerpt.
        - Do NOT include section headers.
        - If no direct requirement exists, return exactly:
        Not found in sources.

        Plan step:
        {step}

        Document excerpts:
        {context}

        Return ONLY the documented requirement text.
        If unsupported, return exactly:
        Not found in sources.
        """.strip()
