def decide(ai_output):
    severity = ai_output["severity"]
    confidence = ai_output["confidence"]
    action = ai_output["recommended_action"]

    # Safety threshold (enterprise standard)
    if confidence < 0.6:
        return "notify"

    if severity == "LOW":
        return "monitor"

    if severity == "MEDIUM":
        return "notify"

    if severity == "HIGH":
        return action if action in ["scale", "restart"] else "scale"

    if severity == "CRITICAL":
        return "restart"

    return "notify"