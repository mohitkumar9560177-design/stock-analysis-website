import yfinance as yf
from backend.services import analyzer

def fetch_stock_data(ticker: str):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="3mo")
        
        if hist.empty:
            return {"status": "error", "message": "Stock ticker galat hai ya data nahi mila."}

        hist = analyzer.calculate_indicators(hist)
        
        # Latest data (aakhri din ka) nikal rahe hain signal ke liye
        latest_row = hist.iloc[-1].to_dict()
        signal_type, signal_reason = analyzer.get_trading_signal(latest_row)

        data = hist.reset_index().to_dict(orient="records")
        
        for row in data:
            row['Date'] = str(row['Date'])[:10] 

        # Response mein signal bhi bhej rahe hain
        return {
            "status": "success", 
            "ticker": ticker, 
            "signal_type": signal_type,
            "signal_reason": signal_reason,
            "data": data
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}