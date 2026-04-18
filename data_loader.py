import pandas as pd
import requests

class DataLoader:
    BASE_URL = "https://api.binance.com/api/v3/klines"

    def __init__(self, symbol, interval, start, end):
        self.symbol = symbol
        self.interval = interval
        self.start_ms = int(pd.Timestamp(start).timestamp() * 1000)
        self.end_ms = int(pd.Timestamp(end).timestamp() * 1000)

    def fetch(self):
        params = {
            "symbol": self.symbol,
            "interval": self.interval,
            "startTime": self.start_ms,
            "endTime": self.end_ms,
            "limit": 1000
        }
        all_candles = []
        while True:
            data = requests.get(self.BASE_URL, params=params).json()
            if not data:
                break
            all_candles.extend(data)
            if len(data) < 1000:
                break
            params["startTime"] = data[-1][0] + 1  # paginate: start after last candle

        df = pd.DataFrame(all_candles)
        df = df[[0, 4]].rename(columns={0: "time", 4: "close"})
        df["time"] = pd.to_datetime(df["time"], unit="ms")
        df["close"] = df["close"].astype(float)
        return df.set_index("time")