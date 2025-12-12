import json
from collections import defaultdict, Counter
from pathlib import Path

# Find the project root (two levels up from this file)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
EVENT_FILE = PROJECT_ROOT / "simulator" / "simulated_events.json"


def load_events():
    """Read line-by-line JSON events from the simulator output file."""
    events = []
    if not EVENT_FILE.exists():
        print(f"⚠ No event file found at {EVENT_FILE}. Run the simulator first.")
        return events

    with EVENT_FILE.open("r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                # skip bad lines
                continue
    return events


def build_customer_stats(events):
    """Aggregate events per customer."""
    stats = defaultdict(lambda: {
        "events": [],
        "counts": Counter(),
        "has_purchase": False
    })

    for e in events:
        cid = e.get("customer_id", "unknown")
        etype = e.get("event_type", "unknown")

        stats[cid]["events"].append(e)
        stats[cid]["counts"][etype] += 1
        if etype == "purchase":
            stats[cid]["has_purchase"] = True

    return stats


def compute_intent_score(counts, has_purchase):
    """
    Very simple scoring:
    - page_view: 1
    - product_view: 2
    - add_to_cart: 3
    - email_opened: 1
    - email_clicked: 2
    - review_posted: 1
    - purchase: 5
    Then scale roughly to 0–100.
    """
    weights = {
        "page_view": 1,
        "product_view": 2,
        "add_to_cart": 3,
        "email_opened": 1,
        "email_clicked": 2,
        "review_posted": 1,
        "purchase": 5,
    }

    score = 0
    for etype, count in counts.items():
        score += weights.get(etype, 0) * count

    # boost if they already purchased at least once
    if has_purchase:
        score += 10

    # cap between 0 and 100
    score = max(0, min(score * 5, 100))
    return score


def compute_churn_score(counts, has_purchase):
    """
    Simple churn logic:
    - only page views, no add_to_cart / purchase → high churn
    - some engagement but no purchase → medium churn
    - has purchase and activity → low churn
    """
    total_events = sum(counts.values())
    add_to_cart = counts.get("add_to_cart", 0)
    purchases = counts.get("purchase", 0)

    if total_events == 0:
        return 50  # unknown, neutral

    if purchases > 0:
        # they bought, so churn is lower
        base = 20
        if add_to_cart > 0:
            base -= 5
        return max(0, base)

    # no purchases
    if add_to_cart == 0:
        # just browsing, risky
        return 75
    else:
        # they showed interest but didn't buy
        return 55


def suggest_next_action(intent_score, churn_score, counts):
    """
    Generate a simple recommendation string based on scores + behaviour.
    """
    if intent_score > 70 and churn_score < 40:
        return "Send a limited-time offer to close the sale."

    if churn_score >= 70:
        return "Reach out with a personal message or retention discount."

    if counts.get("add_to_cart", 0) > 0 and counts.get("purchase", 0) == 0:
        return "Send a cart reminder email with a small incentive."

    if counts.get("review_posted", 0) > 0:
        return "Thank them for their review and suggest a loyalty program."

    return "Send a helpful product recommendation email."


def run_intent_engine():
    print("Running LocalBoost Intent Engine...\n")

    events = load_events()
    if not events:
        print("No events to analyse. Did you run the simulator?")
        return

    stats = build_customer_stats(events)

    results = []

    for customer_id, s in stats.items():
        counts = s["counts"]
        has_purchase = s["has_purchase"]

        intent_score = compute_intent_score(counts, has_purchase)
        churn_score = compute_churn_score(counts, has_purchase)
        action = suggest_next_action(intent_score, churn_score, counts)

        result = {
            "customer_id": customer_id,
            "intent_score": intent_score,
            "churn_score": churn_score,
            "next_best_action": action
        }
        results.append(result)

        print(f"Customer: {customer_id}")
        print(f"  Events: {dict(counts)}")
        print(f"  Intent Score: {intent_score}")
        print(f"  Churn Score:  {churn_score}")
        print(f"  Next Action:  {action}")
        print("-" * 40)

    # Write results to a JSON file for the dashboard later
    output_path = Path(__file__).parent / "intent_results.json"
    with output_path.open("w") as f:
        json.dump(results, f, indent=2)

    print(f"\nSaved intent results to: {output_path}")


if __name__ == "__main__":
    run_intent_engine()
