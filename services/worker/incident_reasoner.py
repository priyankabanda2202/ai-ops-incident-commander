import redis
import json
import requests

from services.worker.llm_reasoner import analyze_incident
from services.worker.decision_engine import decide

from memory.vector_store import store_incident, find_similar
from services.actions.remediation_engine import execute_action
from db.incident_store import save_incident


r = redis.Redis(host="localhost", port=6379, decode_responses=True)

print("🧠 GenAI Incident Commander running...")


while True:
    event_json = r.brpop("event_queue", timeout=5)
    if not event_json:
        continue

    _, data = event_json
    event = json.loads(data)

    # 1️⃣ AI reasoning (structured)
    ai_result = analyze_incident(event)
    root_cause = ai_result["root_cause"]

    # 🎯 2️⃣ Enterprise decision layer
    final_action = decide(ai_result)
    print("🤖 AI Decision:", final_action)

    incident_text = f"{event['service']} issue: {root_cause}"

    # 3️⃣ Memory lookup
    past = find_similar(incident_text)

    if past:
        print("📚 Similar past incident found:")
        print(past)

    # 4️⃣ Store knowledge
    store_incident(incident_text)

    # ⚙️ 5️⃣ Execute governed action
    action = execute_action(final_action)
    print("⚙️ Action executed:", action)

    # 6️⃣ Log incident
    print("\n🚨 NEW INCIDENT")
    print("Service:", event["service"])
    print("AI Root Cause:", root_cause)
    print("-" * 50)

    save_incident(event["service"], incident_text, action)

    # 📡 7️⃣ Stream live update
    payload = {
        "service": event["service"],
        "root_cause": root_cause,
        "decision": final_action,
        "action": action
    }

    requests.post("http://localhost:8000/push", json=payload)