from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from pathlib import Path

app = FastAPI()

# enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"

@app.get("/api/revenue")
def get_revenue():
    df = pd.read_csv(PROCESSED_DIR / "monthly_revenue.csv")
    return df.to_dict(orient="records")

@app.get("/api/categories")
def get_categories():
    df = pd.read_csv(PROCESSED_DIR / "category_performance.csv")
    return df.to_dict(orient="records")

@app.get("/api/customers")
def get_top_customers():
    df = pd.read_csv(PROCESSED_DIR / "top_customers.csv")
    return df.to_dict(orient="records")

@app.get("/")
def health_check():
    return {"status": "active", "service": "analytics_api"}