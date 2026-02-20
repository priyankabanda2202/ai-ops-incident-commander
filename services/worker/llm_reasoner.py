import ollama
import json

def analyze_incident(event):
    prompt = f"""
You are an enterprise SRE AI.

Analyze this incident and return ONLY valid JSON:

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

    return json.loads(response["message"]["content"])