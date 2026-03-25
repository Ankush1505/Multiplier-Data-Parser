# Multiplier AI - Data Pipeline & Analytics Dashboard

Candidate: Ankush

## Project Overview

This project processes raw e-commerce data, calculates business metrics, and serves the results via a FastAPI backend to a real-time HTML/JS dashboard.

## 1. Setup Environment

Open your terminal in the root project folder and install the required Python libraries:

pip install -r backend/requirements.txt

## 2. Run the Data Pipeline

Execute the data cleaning script to handle missing values and format dates:

python Clean_data.py

Execute the analysis script to generate the business metrics (creates CSVs in data/processed):

python analyze.py

## 3. Start the Backend Server

Run the FastAPI server using uvicorn:

uvicorn backend.main:app

## 4. View the Dashboard

Open the `frontend/index.html` file directly in your web browser (Chrome, Safari, etc.) to view the interactive Chart.js dashboard.
