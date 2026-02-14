# utils/writer_prompt_builder.py

from __future__ import annotations

from typing import Tuple, List, Dict, Any
from statistics import mean


def build_writer_prompt(task: str, supported_notes: List[Dict[str, Any]]) -> Tuple[str, float]:
    insights: list[str] = []
    actions: list[str] = []
    confidences: list[float] = []

    for note in supported_notes:
        insight = note.get("insight")

        if not isinstance(insight, str):
            continue
        insight_clean = insight.strip()
        if not insight_clean:
            continue
        if insight_clean.lower() == "not found in sources.":
            continue

        owner = "TBD"
        owners = note.get("owners")
        if isinstance(owners, list) and owners and isinstance(owners[0], str) and owners[0].strip():
            owner = owners[0].strip()

        due = "TBD"
        dues = note.get("due")
        if isinstance(dues, list) and dues and isinstance(dues[0], str) and dues[0].strip():
            due = dues[0].strip()

        confidence = float(note.get("confidence", 0.0))
        confidences.append(confidence)

        insights.append(insight_clean)

        action_text = " ".join(insight_clean.split())

        actions.append(
            f"- Owner: {owner}\n"
            f"  | Due: {due}\n"
            f"  | Confidence: {confidence:.2f}\n"
            f"  | Action: {action_text}"
        )

    avg_conf = round(mean(confidences), 2) if confidences else 0.0

    insights_text = "\n".join(f"- {i}" for i in insights) if insights else "- None documented"
    actions_text = "\n\n".join(actions) if actions else "- None documented"

    prompt = f"""
            You are an enterprise delivery strategist.

            STRICT RULES:
            - Use ONLY the documented insights provided.
            - Do NOT introduce new risks.
            - Do NOT introduce new actions.
            - Do NOT expand beyond the documented insights.
            - If the insights do not answer the question, respond exactly: Not found in sources.

            User Question:
            {task.strip()}

            Documented Insights:
            {insights_text}

            Return exactly in this structure:

            ### Executive Summary
            Maximum 140 words.
            Strictly grounded in the documented insights.

            ### Client-ready Email
            Subject: Q2 Delivery Priorities - Clinical Analytics Dashboard

            Dear Stakeholders,

            Write a concise professional message strictly based on the documented insights.

            Best regards,
            Rinesa Gerxhaliu

            ### Action List
            {actions_text}
            """.strip()

    return prompt, avg_conf
