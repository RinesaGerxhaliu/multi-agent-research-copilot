from statistics import mean

def calculate_confidence(scores: list[float]) -> float:

    if not scores:
        return 0.0

    avg_distance = mean(scores)

    confidence = max(0.0, min(1.0, 1.5 - avg_distance))

    return round(confidence, 2)
