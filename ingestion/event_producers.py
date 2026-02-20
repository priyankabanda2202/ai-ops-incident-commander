import requests
import random
import time

SERVICES = ["auth-service", "payments", "recommendation", "api-gateway"]

while True:
    payload = {
        "service": random.choice(SERVICES),
        "metric": "cpu_usage",
        "value": random.uniform(30, 95),
        "severity": "critical" if random.random() > 0.8 else "normal"
    }

    requests.post("http://localhost:8000/event", json=payload)
    time.sleep(2)
