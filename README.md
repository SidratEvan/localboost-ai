# LocalBoost AI — Customer Intent Pulse

This is a small project I built to understand how real platforms track customer behavior and turn that data into helpful insights for small businesses. The system simulates customer activity, analyzes it, saves the results into a database, exposes it through an API, and then displays everything on a simple dashboard.

The whole idea is to make a tiny version of how real companies (like SaaS/AI platforms) understand customer intent and churn.


## What this project does
### 1. Event Simulator (Python)
---
Creates fake customer activity such as:

-page views

-product views

-add-to-cart

-purchases

r-eviews

-email opens / clicks

Each event is written line-by-line into a JSON file called simulated_events.json.


### 2. Intent Engine (Python + SQLite)
---
The intent engine reads all the simulated events and calculates:

-intent score (how likely a customer is to buy)

-churn score (how likely they are to leave)

-next best action (a simple recommendation)

The scoring model is intentionally simple and beginner-friendly.
After the analysis:

-The results are saved into intent_results.json

-The same results are also written into a real SQLite database (localboost.db)

-The database has two tables (defined in backend/common/models.sql):

--events

--analytics


### 3. API Gateway (Go)
---
I built a small Go HTTP server that reads the analytics results from the SQLite database and exposes them through API endpoints:
GET /healthz     -> returns OK
GET /intent      -> returns analytics rows from SQLite as JSON

The Go service acts as a mini microservice that the frontend or other systems can call.



### 4. Dashboard (HTML + JavaScript)
---
The dashboard is a simple webpage that:

-calls the Go /intent API

-loads customer intent + churn data

-displays a clean table showing:

--customer ID

--intent score

--churn score

--next best action

The scores have color badges so it’s easier to read at a glance.

This turns the backend data into something visual.

---
### How the pieces connect:
[Python Event Simulator] → simulated_events.json
            ↓
[Python Intent Engine] → intent_results.json + SQLite database
            ↓
[Go API Gateway] → reads from SQLite and serves /intent
            ↓
[Dashboard] → fetches /intent and shows it visually



## How to run it:
---
1. Generate customer events
cd simulator
python event_simulator.py
2. Analyze events (writes to JSON + SQLite)
cd backend/analytics
python intent_engine.py
3. Start the Go API server
cd backend/api_gateway
go run main.go
4. Open the dashboard
Open this file in any browser:
frontend/dashboard/index.html
Then click Refresh Data to load the latest customer analytics.



## Why I built this:
---
-I wanted hands-on practice with:

-Python scripting

-Go backend basics

-SQL databases (SQLite)

-simple analytics logic

-working with multiple folders/services

-connecting everything through an API

-showing the final output on a webpage

This project helped me understand how customer analytics systems work behind the scenes and how different parts of a platform communicate with each other.



##Future improvements
---
-If I continue this project, I want to:

-switch from SQLite to PostgreSQL

-stream events using Pub/Sub

-add more advanced scoring models

-improve the UI using React

-deploy the Go API to the cloud

-visualize trends over time


## Author
---
SK Sidratul Islam Priyo

University of Saskatchewan

GitHub: SidratEvan

## Summary
---
This project is beginner-friendly, but it shows how Python, Go, SQL, and a frontend dashboard can work together to build a small analytics system.
It simulates a real-world flow: events → analytics → database → API → dashboard, which is commonly used in modern SaaS and AI platforms.
