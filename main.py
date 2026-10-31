
from etl.extract import extract_stock_data
from etl.transform import transform_stock_data
from etl.load import load_stock_data

from logs.logger import logger


def run_pipeline(symbol="IBM"):

    try:
        logger.info("================================")
        logger.info("STOCK ETL PIPELINE STARTED")
        logger.info("================================")

        logger.info("Starting data extraction for %s", symbol)

        raw_data = extract_stock_data(symbol)

        logger.info("Data extraction completed successfully")

        logger.info("Starting data transformation")

        processed_data = transform_stock_data(raw_data)

        logger.info("Data transformation completed successfully")

        logger.info("Starting data loading")

        loaded_count = load_stock_data(processed_data)

        logger.info("Data loading completed successfully")

        logger.info("Stock Symbol: %s", symbol)
        logger.info("Records Processed: %s", loaded_count)
        logger.info("ETL PIPELINE COMPLETED SUCCESSFULLY")

    except Exception:
        logger.exception("ETL PIPELINE FAILED")


if __name__ == "__main__":
    run_pipeline("IBM")
