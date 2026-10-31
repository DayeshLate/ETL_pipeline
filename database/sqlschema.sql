CREATE DATABASE IF NOT EXISTS etl_db;

USE etl_db;

CREATE TABLE IF NOT EXISTS stock_prices (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    trade_date DATE NOT NULL,
    open_price DECIMAL(15, 4),
    high_price DECIMAL(15, 4),
    low_price DECIMAL(15, 4),
    close_price DECIMAL(15, 4),
    volume BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_stock_date (symbol, trade_date)

);


CREATE INDEX idx_symbol
ON stock_prices(symbol);

CREATE INDEX idx_trade_date
ON stock_prices(trade_date);

DESCRIBE stock_prices;

SELECT * FROM stock_prices;
