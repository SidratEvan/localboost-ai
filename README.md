LocalBoost AI — Customer Intent Pulse

This is a small project I built to learn how real platforms track customer behavior and use it to help businesses understand what their customers might do next.

The idea is simple:

simulate customer activity

analyze the activity

give each customer an “intent score” (how likely they are to buy)

give a “churn score” (how likely they are to leave)

show a “next best action”

display everything on a small dashboard

I wanted to make something that feels like a tiny version of a real system used by companies that help small businesses grow.

What this project does
1. Event Simulator (Python)

Creates fake customer events like:

page views

product views

add to cart

purchases

reviews

email opens

These events get saved into a JSON file.

2. Intent Engine (Python)

Reads the events and calculates:

intent score

churn score

next best action

The math is simple on purpose. I just used weights and conditions to make it understandable and beginner-friendly.

The results are saved into intent_results.json.

3. API Gateway (Go)

I made a small Go HTTP server with two routes:

GET /healthz    -> returns OK  
GET /intent     -> returns the intent results as JSON  


This makes the project feel like a real backend service.

4. Dashboard (HTML + JavaScript)

A simple webpage that:

calls the Go API

loads the intent data

shows a table with:

customer ID

intent score

churn score

next best action

The colors change depending on the score so it’s easy to read.

Example screenshot:



🏗️ How the pieces connect
[Python Event Simulator] → simulated_events.json
        ↓
[Python Intent Engine] → intent_results.json
        ↓
[Go API Gateway] → serves /intent
        ↓
[Dashboard] → shows everything visually




How to run it
1. Run the simulator
cd simulator
python event_simulator.py

2. Run the intent engine
cd backend/analytics
python intent_engine.py

3. Run the Go API server
cd backend/api_gateway
go run main.go

4. Open the dashboard

Open this file in a browser:

frontend/dashboard/index.html


Click Refresh Data, and you’ll see the customer scores.

Why I built this

I wanted to practice:

Python scripting

Go backend basics

frontend + API calls

simple data analysis

working with multiple folders/services

thinking about how real systems fit together

This project helped me understand how customer analytics works and how different parts of a platform communicate.

Future improvements (if I continue)

use a real database instead of JSON

use real Pub/Sub message passing

use React for the dashboard

try deploying the Go API to the cloud

improve the scoring model

Author

SK Sidratul Islam Priyo
University of Saskatchewan
GitHub: SidratEvan

Summary

This project is beginner-friendly, but it shows how multiple services—Python, Go, and frontend—can work together to create a small analytics system.