import streamlit as st
import sys
from pathlib import Path
import time
from dataclasses import asdict, is_dataclass
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from shared_state import SharedState
from orchestration.graph import build_graph

st.set_page_config(
    page_title="Enterprise Multi-Agent",
    layout="wide",
)

st.title("Multi-Agent Enterprise Intelligence Platform")
st.caption("Plan → Research → Draft → Verify | Evidence-Grounded Governance Engine")
st.markdown("---")

graph = build_graph()


def normalize_result(raw_result):
    if isinstance(raw_result, dict):
        return raw_result
    if is_dataclass(raw_result):
        return asdict(raw_result)
    return {}

st.sidebar.markdown("Copy & paste any of the following tasks:")

st.sidebar.code(
    """Extract the documented owners and mitigation targets for Q2 risks impacting the Week 16 production release.""",
    language="text")

st.sidebar.code(
    """List the documented Q2 risks along with their mitigation targets and assigned owners.""",
    language="text")

st.sidebar.code(
    """Identify all documented migration and security risks and their mitigation targets for Q2.""",
    language="text")

st.sidebar.code(
    """Summarize the documented migration, security, and performance risks for the Week 16 release and their mitigation targets.""",
    language="text")

st.sidebar.markdown("---")
st.sidebar.caption("All tasks above are grounded in documented enterprise evidence.")

user_input = st.text_area(
    "Enterprise Task",
    height=130,
    key="task_input",
    placeholder="Enter your enterprise analysis task here..."
)

run_clicked = st.button("Run Multi-Agent Pipeline", use_container_width=True)

if run_clicked:

    if not user_input.strip():
        st.warning("Please enter a task.")
        st.stop()

    with st.spinner("Running enterprise multi-agent orchestration..."):
        start_time = time.time()
        initial_state = SharedState(task=user_input.strip())
        raw_result = graph.invoke(initial_state)
        duration = round(time.time() - start_time, 2)

    result = normalize_result(raw_result)

    final_output = result.get("final_output", "")
    trace = result.get("trace", [])
    verification_notes = result.get("verification_notes", [])
    research_notes = result.get("research_notes", [])
    metrics = result.get("metrics", [])

    st.success("Pipeline execution completed successfully.")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Research Notes", len(research_notes))

    with col2:
        st.metric("Runtime (sec)", duration)

    with col3:
        if research_notes:
            st.success("Evidence Found")
        else:
            st.error("No Evidence Found")

    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Output", "Notes", "Sources", "Observability"]
    )

    with tab1:
        if final_output:
            st.markdown(final_output)
        else:
            st.warning("No output generated.")

    with tab2:
        if research_notes:
            for i, note in enumerate(research_notes, 1):
                st.markdown(f"### Note {i}")
                st.markdown(note.get("insight", ""))
                st.markdown(f"**Confidence:** {note.get('confidence')}")
                st.markdown("---")
        else:
            st.info("No research notes available.")

    with tab3:

        unique_sources = set()

        for note in research_notes:
            for c in note.get("citations", []):
                doc = c.get("document_name")
                chunk = c.get("chunk_id")
                if doc and chunk is not None:
                    unique_sources.add(f"{doc} | chunk {chunk}")

        if unique_sources:
            for s in sorted(unique_sources):
                st.markdown(f"- `{s}`")
        else:
            st.info("No sources available.")

    with tab4:

        st.markdown("### Agent Observability")

        if metrics:
            df_metrics = pd.DataFrame(metrics)

            if "tokens" in df_metrics.columns:
                df_metrics["prompt_tokens"] = df_metrics["tokens"].apply(
                    lambda x: x.get("prompt_tokens") if isinstance(x, dict) else None
                )
                df_metrics["completion_tokens"] = df_metrics["tokens"].apply(
                    lambda x: x.get("completion_tokens") if isinstance(x, dict) else None
                )
                df_metrics["total_tokens"] = df_metrics["tokens"].apply(
                    lambda x: x.get("total_tokens") if isinstance(x, dict) else None
                )

            st.dataframe(
                df_metrics[
                    ["agent", "latency_sec", "prompt_tokens", "completion_tokens", "total_tokens"]
                ],
                use_container_width=True
            )
        else:
            st.info("No LLM metrics captured.")

        st.markdown("### Trace Log")

        if trace:
            df_trace = pd.DataFrame(trace)
            st.dataframe(df_trace, use_container_width=True)
        else:
            st.info("No trace available.")

        if verification_notes:
            st.markdown("### Verification Notes")
            for note in verification_notes:
                st.markdown(f"- {note}")
