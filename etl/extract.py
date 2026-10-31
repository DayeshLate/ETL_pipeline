
import requests
import json

from config.config import (
    API_KEY,
    API_URL,
    RAW_DATA_FILE
)

def extract_stock_data(symbol="IBM"):

    print(f"Starting data extraction for {symbol}...")
    if not API_KEY:
        raise ValueError("API_KEY is missing in .env file")

    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "outputsize": "compact",
        "apikey": API_KEY
    }

    try:

        response = requests.get(
            API_URL,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        if "Error Message" in data:
            raise ValueError(data["Error Message"])

        if "Note" in data or "Information" in data:
            raise ValueError(
                data.get("Note") or data.get("Information")
            )

        if "Time Series (Daily)" not in data:
            raise ValueError("Stock market data not found in API response")

        with open(RAW_DATA_FILE, "w", encoding="utf-8") as file:

            json.dump(
                data,
                file,
                indent=4
            )

        print("Data extracted successfully!")
        print(f"Raw data saved at: {RAW_DATA_FILE}")

        return data

    except requests.exceptions.RequestException as e:

        print("API request failed:", e)
        raise

    except (ValueError, json.JSONDecodeError) as e:

        print("Data extraction failed:", e)
        raise

if __name__ == "__main__":

    stock_data = extract_stock_data("IBM")

    print("\nExtraction completed!")
    print("Stock:", stock_data["Meta Data"]["2. Symbol"])
    print(
        "Available records:",
        len(stock_data["Time Series (Daily)"])
    )
