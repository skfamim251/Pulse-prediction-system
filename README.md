# Pulse Prediction System (Website)

A full-stack website for educational cardiovascular risk screening based on pulse (heart rate) and blood pressure.

## Features

- **Backend** built with Python standard library HTTP server (`pulse_prediction/web.py`)
  - `GET /` serves the frontend
  - `POST /api/assess` calculates risk level, score, and reasons
  - `GET /api/health` health-check endpoint
- **Frontend** in vanilla HTML/CSS/JavaScript
  - Input form for heart rate and BP
  - Calls backend asynchronously and renders results
- **Shared risk model** in Python (`pulse_prediction/model.py`)

## Run locally

```bash
python -m pulse_prediction.web
```

Then open: `http://localhost:5000`

## API example

```bash
curl -X POST http://localhost:5000/api/assess \
  -H 'Content-Type: application/json' \
  -d '{"heart_rate":112,"systolic_bp":168,"diastolic_bp":104}'
```

## Medical safety note

This project is for educational triage-style screening only and is **not a medical diagnosis**. If severe symptoms are present (chest pain, breathlessness, confusion, fainting), seek urgent medical care.
