import pandas as pd
import numpy as np

def calculate_indicators(df):
    df = df.copy()
    
    # 1. Simple Moving Average (SMA 20)
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    
    # 2. Relative Strength Index (RSI 14)
    delta = df['Close'].diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI_14'] = 100 - (100 / (1 + rs))

    # 3. MACD
    exp1 = df['Close'].ewm(span=12, adjust=False).mean()
    exp2 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp1 - exp2
    df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()

    # 4. Bollinger Bands (20 Days, 2 Standard Deviations)
    df['BB_Middle'] = df['Close'].rolling(window=20).mean()
    df['BB_Std'] = df['Close'].rolling(window=20).std()
    df['BB_Upper'] = df['BB_Middle'] + (df['BB_Std'] * 2)
    df['BB_Lower'] = df['BB_Middle'] - (df['BB_Std'] * 2)
    
    # NaN values ko None karna
    df = df.replace({np.nan: None})
    return df

def get_trading_signal(latest_data):
    if latest_data['RSI_14'] is None:
        return "Neutral", "Data insufficient"
        
    rsi = latest_data['RSI_14']
    macd = latest_data['MACD']
    signal = latest_data['Signal_Line']

    if rsi < 30:
        return "Buy", "Stock Oversold hai (RSI < 30)."
    elif rsi > 70:
        return "Sell", "Stock Overbought hai (RSI > 70)."
    elif macd > signal:
        return "Buy", "MACD ne Signal line ko upar cross kiya hai (Bullish trend)."
    else:
        return "Hold", "Market neutral hai. Abhi ruke rahein."