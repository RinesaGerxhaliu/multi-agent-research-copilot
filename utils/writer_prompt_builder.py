from __future__ import annotations
from typing import Tuple, List, Dict, Any
from statistics import mean

def build_writer_prompt(
    task: str,
    supported_notes: List[Dict[str, Any]],
    intent: str | None = None
) -> Tuple[str, float]:

    insights: List[str] = []
    actions: List[str] = []
    confidences: List[float] = []
    source_lines: List[str] = []

    for note in supported_notes:

        insight = note.get("insight")
        if not isinstance(insight, str):
            continue

        insight = insight.strip()
        if not insight or insight.lower() == "not found in sources.":
            continue

        confidence = float(note.get("confidence", 0.0))
        confidences.append(confidence)

        insights.append(insight)

        owner = "TBD"
        due = "TBD"

        owners = note.get("owners")
        if isinstance(owners, list) and owners:
            owner = owners[0]

        dues = note.get("due")
        if isinstance(dues, list) and dues:
            due = dues[0]

        short_action = insight.split("\n")[0][:150]

        actions.append(
            f"- Owner: {owner}\n"
            f"  | Due: {due}\n"
            f"  | Confidence: {round(confidence, 2)}\n"
            f"  | Action: {short_action}"
        )

        for c in note.get("citations", []):
            doc = c.get("document_name")
            chunk = c.get("chunk_id")
            if doc and chunk is not None:
                source_lines.append(f"- {doc} | chunk {chunk}")

    if not insights:
        return "Not found in sources.", 0.0

    avg_conf = round(mean(confidences), 2) if confidences else 0.0

    insights_text = " ".join(insights)
    actions_text = "\n\n".join(actions)
    sources_text = "\n".join(list(dict.fromkeys(source_lines)))

    if intent == "governance":

        prompt = f"""
            You are an enterprise governance analyst.

            Use ONLY the documented insights below.
            Do NOT introduce new information.

            User Question:
            {task}

            Documented Insights:
            {insights_text}

            Return EXACTLY:

            ### Executive Summary
            (Concise summary of documented governance constraints. Max 150 words.)

            ### Client-ready Email
            Subject: Documented Governance Constraints Update

            Dear Stakeholders,

            (Summarize documented governance constraints only.)

            Best regards,
            Your Name

            ### Action List
            {actions_text}

            """.strip()

        return prompt, avg_conf

    if intent == "risk_analysis":

        prompt = f"""
            You are an enterprise risk analyst.

            Use ONLY the documented risks and mitigation targets below.

            User Question:
            {task}

            Documented Evidence:
            {insights_text}

            Return EXACTLY:

            ### Executive Summary
            (Concise summary of documented risks. Max 150 words.)

            ### Client-ready Email
            Subject: Documented Risk & Mitigation Update

            Dear Stakeholders,

            (Summarize documented risks and mitigation targets only.)

            Best regards,
            Your Name

            ### Action List
            {actions_text}
            """
        return prompt, avg_conf

    prompt = f"""
        You are an enterprise delivery analyst.

        Use ONLY the documented insights below.
        Do NOT introduce new information.

        User Question:
        {task}

        Documented Insights:
        {insights_text}

        Return EXACTLY:

        ### Executive Summary
        Provide a concise executive-level summary (max 120 words).
        - List each documented risk.
        - Explicitly include Owner and Mitigation Target for each risk.
        - Do NOT mention impact levels unless explicitly requested.
        - Do NOT add interpretation or new information.
        - Keep tone formal and board-ready.

        ### Client-ready Email
        Subject: Documented Actions and Controls Update

        Dear Stakeholders,

        (Summarize documented findings only.)

        Best regards,
        Your Name

        ### Action List
        {actions_text}

        """.strip()

    return prompt, avg_conf
