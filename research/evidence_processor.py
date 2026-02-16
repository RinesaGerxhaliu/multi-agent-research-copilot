from typing import Tuple, Dict, Any, List
from retrieval.retriever import Retriever
from utils.confidence_utils import calculate_confidence
import re

retriever = Retriever()

from typing import Tuple, Dict, Any, List
from retrieval.retriever import Retriever
from utils.confidence_utils import calculate_confidence
import re

retriever = Retriever()

SIMILARITY_THRESHOLD = 0.90  


def process_step(step: str) -> Tuple[Dict[str, Any] | None, str]:

    if not step:
        return None, "not-found"

    results = retriever.search(step, k=5)

    if not results:
        return None, "not-found"

    citations: List[Dict[str, Any]] = []
    scores: List[float] = []
    cleaned_snippets: List[str] = []

    for r in results:

        snippet = r.get("snippet")
        score = float(r.get("distance_score", 0.8))

        if score > SIMILARITY_THRESHOLD:
            continue

        if not snippet:
            continue

        snippet_clean = snippet.strip()

        cleaned_snippets.append(snippet_clean)
        scores.append(score)

        citations.append({
            "document_name": r.get("document_name"),
            "chunk_id": r.get("chunk_id"),
            "similarity_score": score,
            "citation": snippet_clean
        })

    if not cleaned_snippets:
        return None, "not-found"

    combined_insight = "\n".join(cleaned_snippets[:2]).strip()

    confidence = round(calculate_confidence(scores), 2)

    owners = re.findall(
        r"Owner:\s*([A-Za-z &\-]+)",
        combined_insight
    )

    due_dates = re.findall(
        r"(?:Mitigation Target|Target Completion|Target Date):\s*(Week\s*\d+|Ongoing\s*\(.*?\))",
        combined_insight
    )

    owners = list(dict.fromkeys([o.strip() for o in owners]))
    due_dates = list(dict.fromkeys([d.strip() for d in due_dates]))

    return {
        "insight": combined_insight,
        "citations": citations,
        "confidence": confidence,
        "owners": owners if owners else None,
        "due": due_dates if due_dates else None,
        "evidence": {
            "supported": True,
            "reason": None
        }
    }, "supported"

