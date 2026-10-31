
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from config.config import DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    echo=False
)

def test_connection():

    try:
        with engine.connect() as connection:
            result = connection.execute(
                text("SELECT 1")
            )
            print("MySQL connection successful!")
            print("Test result:", result.scalar())
            return True

    except SQLAlchemyError as e:

        print("Database connection failed!")
        print("Error:", e)

        return False

def close_connection():
    engine.dispose()
    print("Database connections closed.")


if __name__ == "__main__":

    if test_connection():
        print("Database is ready for ETL operations.")
