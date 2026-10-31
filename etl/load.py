
import pandas as pd

from decimal import Decimal
from sqlalchemy import MetaData, Table, func
from sqlalchemy.dialects.mysql import insert as mysql_insert

from database.connection import engine

def load_stock_data(df):

    print("Starting data loading...")

    if df.empty:
        print("No records available to load.")
        return 0

    try:
        metadata = MetaData()

        stock_table = Table(
            "stock_prices",
            metadata,
            autoload_with=engine
        )
        records = df.to_dict(orient="records")

        cleaned_records = []

        for record in records:
            cleaned_record = {}
            for column, value in record.items():

                if pd.isna(value):
                    value = None

                elif isinstance(value, pd.Timestamp):
                    value = value.date()

                elif hasattr(value, "item"):
                    value = value.item()

                if column in [
                    "open_price",
                    "high_price",
                    "low_price",
                    "close_price"
                ] and value is not None:

                    value = Decimal(str(value))

                cleaned_record[column] = value

            cleaned_records.append(cleaned_record)

        batch_size = 500

        with engine.begin() as connection:

            for start in range(0, len(cleaned_records), batch_size):

                batch = cleaned_records[
                    start:start + batch_size
                ]

                statement = mysql_insert(
                    stock_table
                ).values(batch)

                update_statement = statement.on_duplicate_key_update(

                    open_price=statement.inserted.open_price,

                    high_price=statement.inserted.high_price,

                    low_price=statement.inserted.low_price,

                    close_price=statement.inserted.close_price,

                    volume=statement.inserted.volume,

                    updated_at=func.current_timestamp()
                )

                connection.execute(update_statement)

        print("Data loaded successfully!")
        print("Total records processed:", len(cleaned_records))

        return len(cleaned_records)

    except Exception as e:

        print("Data loading failed:", e)
        raise


if __name__ == "__main__":

    from config.config import PROCESSED_DATA_FILE

    processed_data = pd.read_csv(
        PROCESSED_DATA_FILE,
        parse_dates=["trade_date"]
    )

    loaded_records = load_stock_data(processed_data)

    print(f"\nSuccessfully processed {loaded_records} records.")
