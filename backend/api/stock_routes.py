from fastapi import APIRouter
from backend.services import data_fetcher

router = APIRouter()

@router.get("/stock/{ticker}")
def get_stock(ticker: str):
    data = data_fetcher.fetch_stock_data(ticker)
    return data