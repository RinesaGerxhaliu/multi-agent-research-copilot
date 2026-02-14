from shared_state import SharedState

def validate_citations(state: SharedState) -> bool:
    issues_detected = False
    for note in state.research_notes:
        citations = note.get("citations", [])
        if not citations:
            issues_detected = True
            continue
        for c in citations:
            if not c.get("document_name") or c.get("chunk_id") is None or c.get("similarity_score") is None:
                issues_detected = True
    return issues_detected

def collect_sources(state: SharedState) -> list[str]:
    sources_set = set()
    for note in state.research_notes:
        for c in note.get("citations", []):
            if c.get("document_name") and c.get("chunk_id") is not None:
                sources_set.add(f"{c['document_name']} (chunk {c['chunk_id']})")
    if not sources_set:
        return ["No validated sources available."]
    return sorted(list(sources_set))[:5]

def assemble_output(draft: str, sources: list[str]) -> str:
    lines = [
        "Enterprise Risk & Operations Analysis",
        "--------------------------------------",
        "",
        draft.strip(),
        "",
        "Sources:",
    ]
    lines.extend(f"- {s}" for s in sources)
    return "\n".join(lines)
