from statistics import mean

def calculate_confidence(scores: list[float]) -> float:
    if not scores:
        return 0.0

    avg_distance = mean(scores)
    confidence = max(0.65, min(1.2 - avg_distance, 0.95))

    return round(confidence, 2)
