from collections import defaultdict
from statistics import mean
from retrieval.retriever import Retriever
from utils.research_prompt_builder import build_research_prompt
from utils.confidence_utils import calculate_confidence
from langchain_openai import ChatOpenAI
import os
import re

retriever = Retriever()

model_name = os.getenv("RESEARCH_AGENT_MODEL") or os.getenv("OPENAI_MODEL")
llm = ChatOpenAI(model=model_name, temperature=0.0)

def extract_owner_due(snippet: str):

    owner_match = re.search(r"Owner:\s*(.+)", snippet, re.IGNORECASE)
    due_match = re.search(r"(?:Due|Target Completion|Milestone|Date):\s*(.+)", snippet, re.IGNORECASE)
    owner = owner_match.group(1).strip() if owner_match else None
    due = due_match.group(1).strip() if due_match else None
    return owner, due

def process_step(step: str):

    results = retriever.search(step, k=4)

    print("\n-------------------------")
    print("DEBUG QUERY:", step)
    print("Retrieved results:", len(results))

    for r in results:
        print("DOC:", r["document_name"], "| Chunk:", r["chunk_id"])
    print("---------------------------\n")


    if not results:
        return None, "not-found"

    scores = []
    snippets = []
    citations = []
    owners = set()
    dues = set()

    for r in results:
        score = float(r["distance_score"])
        scores.append(score)

        raw_snippet = r["snippet"]

        clean_lines = []
        for line in raw_snippet.splitlines():
            line = line.strip()
            if not line:
                continue
            if line.startswith("#"):
                continue
            if line.startswith("---"):
                continue
            clean_lines.append(line)

        snippet_text = " ".join(clean_lines)

        snippets.append(snippet_text)

        citations.append({
            "document_name": r["document_name"],
            "chunk_id": r["chunk_id"],
            "citation": snippet_text[:200],
            "similarity_score": score,
        })

        owner_match = re.search(r"Owner:\s*([^\n|]+)", snippet_text)

        due_match = re.search(
            r"(Target Completion|Mitigation Target|Due|Date):\s*(Week\s*\d+)",
            snippet_text
        )


        if owner_match:
            owner = owner_match.group(1).strip()
            owner = owner.split("Impact")[0].strip()
            owners.add(owner)

        if due_match:
            dues.add(due_match.group(2).strip())

    prompt = build_research_prompt(step, snippets)
    response = llm.invoke(prompt)
    raw_insight = (getattr(response, "content", "") or "").strip()

    if not raw_insight:
        return None, "not-found"

    if raw_insight.strip().lower() == "not found in sources.":
        return None, "not-found"

    confidence = calculate_confidence(scores)

    action_entry = {
        "owner": list(owners)[0] if owners else "TBD",
        "due": list(dues)[0] if dues else "TBD",
        "confidence": round(confidence, 2),
        "action": raw_insight,
        "evidence": [c["citation"] for c in citations]
    }

    return {
        "insight": raw_insight,
        "citations": citations,
        "confidence": confidence,
        "owners": list(owners) if owners else None,
        "due": list(dues) if dues else None,
        "evidence": {
            "supported": True,
            "reason": None
        },
        "action_json": [action_entry]
    }, "supported"

