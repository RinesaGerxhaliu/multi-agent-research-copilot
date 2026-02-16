from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, TypedDict, Literal

class Citation(TypedDict):
    document_name: str
    chunk_id: int
    citation: str
    similarity_score: float


class EvidenceStatus(TypedDict):
    supported: bool
    reason: Optional[str]    

class ResearchNote(TypedDict):
    insight: str
    citations: List[Citation]
    evidence: EvidenceStatus
    confidence: float
    owners: Optional[List[str]]
    due: Optional[List[str]]

class ActionItem(TypedDict):
    description: str
    owner: str
    due_date: Optional[str]
    risk_impact: Optional[str]
    confidence: float
    source_citations: List[str]

class TraceLogRow(TypedDict):
    step: Literal["plan", "research", "draft", "verify", "deliver"]
    agent: Literal["planner", "researcher", "writer", "verifier"]
    action: str
    outcome: str

@dataclass
class SharedState:

    task: str

    intent: Optional[str] = None 

    plan: List[str] = field(default_factory=list)

    research_notes: List[ResearchNote] = field(default_factory=list)

    draft: Optional[str] = None

    verification_notes: List[str] = field(default_factory=list)

    final_output: Optional[str] = None
    action_items: List[ActionItem] = field(default_factory=list)

    trace: List[TraceLogRow] = field(default_factory=list)

    metrics: List[dict] = field(default_factory=list)
