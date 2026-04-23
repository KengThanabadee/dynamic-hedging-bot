import pandas as pd
import requests

class DataLoader:
    BASE_URL = "https://api.binance.com/api/v3/klines"

    VALID_INTERVALS = {"1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M"}

    def __init__(self, symbol, interval, start, end):
        if interval not in self.VALID_INTERVALS:
            raise ValueError(f"interval must be one of {self.VALID_INTERVALS}, got '{interval}'")
        start_ms = int(pd.Timestamp(start, tz="UTC").timestamp() * 1000)
        end_ms = int(pd.Timestamp(end, tz="UTC").timestamp() * 1000)
        if start_ms >= end_ms:
            raise ValueError(f"start must be before end, got start={start}, end={end}")
        self.symbol = symbol
        self.interval = interval
        self.start_ms = start_ms
        self.end_ms = end_ms

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
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            if not data:
                break
            if not isinstance(data, list):
                raise ValueError(f"Unexpected response from Binance: {data}")
            all_candles.extend(data)
            if len(data) < 1000:
                break
            params["startTime"] = data[-1][0] + 1  # paginate: start after last candle

        if not all_candles:
            raise ValueError(f"No data returned for symbol={self.symbol}, interval={self.interval}")
        df = pd.DataFrame(all_candles)
        df = df[[0, 4]].rename(columns={0: "time", 4: "close"})
        df["time"] = pd.to_datetime(df["time"], unit="ms")
        df["close"] = df["close"].astype(float)
        return df.set_index("time")