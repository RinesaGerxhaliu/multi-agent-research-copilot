from shared_state import SharedState

def validate_citations(state: SharedState) -> list[str]:

    issues = []

    for note in state.research_notes:
        citations = note.get("citations", [])

        if not citations:
            issues.append("Missing citations")
            continue

        for c in citations:
            if not c.get("document_name"):
                issues.append("Missing document_name")
            if c.get("chunk_id") is None:
                issues.append("Missing chunk_id")
            if c.get("similarity_score") is None:
                issues.append("Missing similarity_score")
            if not c.get("citation"):
                issues.append("Missing citation text")

    return issues


def collect_sources(state: SharedState) -> list[str]:

    sources = {
        f"{c['document_name']} (chunk {c['chunk_id']})"
        for note in state.research_notes
        for c in note.get("citations", [])
        if c.get("document_name") and c.get("chunk_id") is not None
    }

    return sorted(sources)[:5] if sources else ["No validated sources available."]


def assemble_output(draft: str, sources: list[str]) -> str:

    lines = [
        draft.strip(),
        "",
        "### Sources",
    ]

    lines.extend(f"- {s}" for s in sources)

    return "\n".join(lines)
