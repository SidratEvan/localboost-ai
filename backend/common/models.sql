-- LocalBoost AI Database Schema

-- Stores raw customer events (for future use)
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    timestamp TEXT NOT NULL
);

-- Stores aggregated analytics per customer
CREATE TABLE IF NOT EXISTS analytics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id TEXT NOT NULL,
    intent_score INTEGER NOT NULL,
    churn_score INTEGER NOT NULL,
    next_best_action TEXT NOT NULL,
    last_updated TEXT NOT NULL
);
