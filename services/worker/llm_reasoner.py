import json
import re
import ollama

def analyze_incident(event):
    prompt = f"""
You are an enterprise SRE AI.

Analyze this incident and return ONLY valid JSON.

Service: {event['service']}
Metric: {event['metric']}
Value: {event['value']}
Severity flag: {event['severity']}

JSON format:
{{
  "root_cause": "...",
  "severity": "LOW|MEDIUM|HIGH|CRITICAL",
  "confidence": 0.0,
  "recommended_action": "monitor|notify|scale|restart"
}}
"""

    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response["message"]["content"]

    # 🔥 Extract JSON safely (enterprise pattern)
    try:
        json_match = re.search(r'\{.*\}', raw, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        else:
            raise ValueError("No JSON found")

    except Exception:
        # fallback safe structure
        return {
            "root_cause": raw.strip(),
            "severity": "MEDIUM",
            "confidence": 0.5,
            "recommended_action": "notify"
        }