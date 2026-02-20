import time

def execute_action(incident_text):
    if "cpu" in incident_text.lower() or "overload" in incident_text.lower():
        action = "Scale service resources"
    elif "memory leak" in incident_text.lower():
        action = "Restart affected service"
    else:
        action = "Notify engineering team"

    print("⚙️ ACTION TAKEN:", action)
    time.sleep(1)

    return action
