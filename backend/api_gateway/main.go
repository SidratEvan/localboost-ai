package main

import (
	"encoding/json"
	"log"
	"net/http"
	"os"
	"path/filepath"
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
	// Relative path from where the server is run:
	// backend/api_gateway -> ../analytics/intent_results.json
	intentPath := filepath.Join("..", "analytics", "intent_results.json")

	data, err := os.ReadFile(intentPath)
	if err != nil {
		http.Error(w, "could not read intent_results.json. Did you run the intent engine?", http.StatusInternalServerError)
		return
	}

	var results []Result
	if err := json.Unmarshal(data, &results); err != nil {
		http.Error(w, "invalid JSON in intent_results.json", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Content-Type", "application/json")

	if err := json.NewEncoder(w).Encode(results); err != nil {
		http.Error(w, "failed to encode response", http.StatusInternalServerError)
		return
	}
}

