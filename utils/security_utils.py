import time

INJECTION_PATTERNS = [
    "ignore previous instructions",
    "bypass security",
    "skip validation",
    "override governance",
    "change milestone",
    "disable verification",
    "ignore governance rules",
]

def detect_prompt_injection(task: str) -> bool:
    task_lower = task.lower()
    return any(p in task_lower for p in INJECTION_PATTERNS)

def observe_llm_call(state, agent_name: str, llm_callable):
    start_time = time.time()

    try:
        response = llm_callable()
    except Exception as e:
        state.metrics.append({
            "agent": agent_name,
            "latency_sec": round(time.time() - start_time, 2),
            "tokens": {},
            "error": str(e)
        })
        raise

    latency = round(time.time() - start_time, 2)

    token_usage = {}
    if hasattr(response, "response_metadata"):
        token_usage = response.response_metadata.get("token_usage", {})

    if not hasattr(state, "metrics"):
        state.metrics = []

    state.metrics.append({
        "agent": agent_name,
        "latency_sec": latency,
        "prompt_tokens": token_usage.get("prompt_tokens"),
        "completion_tokens": token_usage.get("completion_tokens"),
        "total_tokens": token_usage.get("total_tokens"),
    })

    return response