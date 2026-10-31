
import json
import numpy as np
import pandas as pd

from config.config import (
    RAW_DATA_FILE,
    PROCESSED_DATA_FILE
)


def transform_stock_data(raw_data):

    print("Starting data transformation...")

    symbol = raw_data["Meta Data"]["2. Symbol"]

    time_series = raw_data["Time Series (Daily)"]

    df = pd.DataFrame.from_dict(
        time_series,
        orient="index"
    )

    df.index.name = "trade_date"
    df = df.reset_index()

    df = df.rename(columns={
        "1. open": "open_price",
        "2. high": "high_price",
        "3. low": "low_price",
        "4. close": "close_price",
        "5. volume": "volume"
    })

    df["symbol"] = symbol

    df["trade_date"] = pd.to_datetime(
        df["trade_date"],
        errors="coerce"
    )

    numeric_columns = [
        "open_price",
        "high_price",
        "low_price",
        "close_price",
        "volume"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    df[numeric_columns] = df[numeric_columns].replace(
        [np.inf, -np.inf],
        np.nan
    )

    df = df.dropna(
        subset=[
            "trade_date",
            "open_price",
            "high_price",
            "low_price",
            "close_price",
            "volume"
        ]
    )

    df["volume"] = df["volume"].astype("int64")

    df = df.drop_duplicates(
        subset=["symbol", "trade_date"]
    )

    df = df.sort_values(
        by="trade_date"
    )
    df = df.reset_index(drop=True)

    df = df[
        [
            "symbol",
            "trade_date",
            "open_price",
            "high_price",
            "low_price",
            "close_price",
            "volume"
        ]
    ]

    df.to_csv(
        PROCESSED_DATA_FILE,
        index=False
    )

    print("Data transformation completed!")
    print("Total records:", len(df))
    print("Processed data saved:", PROCESSED_DATA_FILE)

    return df

if __name__ == "__main__":

    with open(RAW_DATA_FILE, "r", encoding="utf-8") as file:
        raw_data = json.load(file)

    processed_data = transform_stock_data(raw_data)

    print("\nProcessed Data:")
    print(processed_data.head())
