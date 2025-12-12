package main

import (
    "encoding/json"
    "log"
    "net/http"
    "path/filepath"
    "database/sql"
    _ "modernc.org/sqlite"
)


// Result represents one customer's intent summary
type Result struct {
	CustomerID     string `json:"customer_id"`
	IntentScore    int    `json:"intent_score"`
	ChurnScore     int    `json:"churn_score"`
	NextBestAction string `json:"next_best_action"`
}

func main() {
	http.HandleFunc("/healthz", healthHandler)
	http.HandleFunc("/intent", intentHandler)

	log.Println("LocalBoost API Gateway running on http://localhost:8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}

func healthHandler(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
	_, _ = w.Write([]byte("OK"))
}

func intentHandler(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Access-Control-Allow-Origin", "*")
    w.Header().Set("Content-Type", "application/json")

    dbPath := filepath.Join("..", "common", "localboost.db")

    db, err := sql.Open("sqlite", dbPath)
    if err != nil {
        http.Error(w, "Failed to open database", http.StatusInternalServerError)
        return
    }
    defer db.Close()

    rows, err := db.Query(`
        SELECT customer_id, intent_score, churn_score, next_best_action
        FROM analytics
        ORDER BY id DESC
        LIMIT 50
    `)
    if err != nil {
        http.Error(w, "Failed to query analytics table", http.StatusInternalServerError)
        return
    }
    defer rows.Close()

    var results []Result
    for rows.Next() {
        var r Result
        if err := rows.Scan(&r.CustomerID, &r.IntentScore, &r.ChurnScore, &r.NextBestAction); err != nil {
            http.Error(w, "Scan error", http.StatusInternalServerError)
            return
        }
        results = append(results, r)
    }

    json.NewEncoder(w).Encode(results)
}

