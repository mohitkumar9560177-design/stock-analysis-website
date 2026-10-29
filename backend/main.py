import os
import sqlite3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api import stock_routes

app = FastAPI(title="Stock Analysis API")

origins = os.getenv("ALLOWED_ORIGINS", "http://127.0.0.1:5500,http://localhost:5500").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stock_routes.router)

# --- Database Setup (Watchlist ke liye) ---
DB_FILE = "watchlist.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS watchlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

# App start hote hi database table ban jayega
init_db()

# Watchlist dekhne ke liye API
@app.get("/watchlist")
def get_watchlist():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT ticker FROM watchlist")
    tickers = [row[0] for row in cursor.fetchall()]
    conn.close()
    return {"watchlist": tickers}

# Watchlist mein naya stock add karne ke liye API
@app.post("/watchlist/{ticker}")
def add_to_watchlist(ticker: str):
    ticker = ticker.upper()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO watchlist (ticker) VALUES (?)", (ticker,))
        conn.commit()
        return {"status": "success", "message": f"{ticker} added to watchlist."}
    except sqlite3.IntegrityError:
        return {"status": "error", "message": "Stock already in watchlist."}
    finally:
        conn.close()

# Watchlist se stock hatane ke liye API
@app.delete("/watchlist/{ticker}")
def remove_from_watchlist(ticker: str):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM watchlist WHERE ticker = ?", (ticker.upper(),))
    conn.commit()
    conn.close()
    return {"status": "success", "message": f"{ticker} removed from watchlist."}

@app.get("/")
def home():
    return {"message": "Welcome to Stock Analysis API! Backend is working."}