import logging
from sqlalchemy import text
import pandas as pd
from db_operations import get_engine
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def load_data_into_warehouse(source_table, target_table):
    """Load cleaned data from source tables into warehouse tables."""
    engine = get_engine()
    query = f"INSERT INTO warehouse.{target_table} SELECT * FROM public.{source_table}"
    with engine.connect() as conn:
        conn.execute(text(f"TRUNCATE TABLE warehouse.{target_table};"))  # Clear existing data
        conn.execute(text(query))
    print(f"Data loaded into warehouse.{target_table} from {source_table}.")
def create_schema(schema_name="warehouse"):
    """Create a new schema in PostgreSQL if it doesn't exist."""
    engine = get_engine()
    with engine.connect() as conn:
        conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema_name};"))
        logger.info(f"Schema '{schema_name}' created or already exists.")

def create_warehouse_tables():
    """Create optimized tables for structured storage."""
    engine = get_engine()
    with engine.connect() as conn:
        # Table for structured Telegram messages
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS warehouse.telegram_messages_dw (
                id SERIAL PRIMARY KEY,
                message TEXT NOT NULL,
                sentiment FLOAT,
                subjectivity FLOAT,
                hour_of_day INT,
                day_of_week TEXT,
                is_weekend BOOLEAN,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))

        # Table for structured object detection results
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS warehouse.object_detection_dw (
                id SERIAL PRIMARY KEY,
                image_file TEXT NOT NULL,
                box_xmin FLOAT,
                box_ymin FLOAT,
                box_xmax FLOAT,
                box_ymax FLOAT,
                confidence FLOAT,
                class TEXT,
                detection_time TIMESTAMP
            );
        """))
        
        logger.info("Warehouse tables created successfully.")

def create_indexes():
    """Optimize tables with indexes for faster queries."""
    engine = get_engine()
    with engine.connect() as conn:
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_telegram_messages_hour ON warehouse.telegram_messages_dw (hour_of_day);"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_detection_class ON warehouse.object_detection_dw (class);"))
        logger.info("Indexes created successfully.")
