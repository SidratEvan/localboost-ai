import random
import json
import time
from datetime import datetime

# Simple list of fake customers
CUSTOMERS = ["c001", "c002", "c003", "c004"]

# Possible event types
EVENT_TYPES = [
    "page_view",
    "product_view",
    "add_to_cart",
    "purchase",
    "review_posted",
    "email_opened",
    "email_clicked"
]

def generate_event():
    event = {
        "customer_id": random.choice(CUSTOMERS),
        "event_type": random.choice(EVENT_TYPES),
        "timestamp": datetime.utcnow().isoformat()
    }
    return event

def run_simulator():
    print("Starting LocalBoost Event Simulator...\n")

    # Generate 10 sample events for now
    for _ in range(10):
        event = generate_event()
        print("Generated Event:", event)

        # Save events to a JSON file (so your AI engine can read it later)
        with open("simulated_events.json", "a") as f:
            f.write(json.dumps(event) + "\n")

        time.sleep(0.5)  # pause to simulate real-time behavior

if __name__ == "__main__":
    run_simulator()
