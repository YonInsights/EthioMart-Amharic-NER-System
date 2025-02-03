import logging
from sqlalchemy import text
from db_operations import get_engine

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def create_schema(schema_name="warehouse"):
    """Ensure the warehouse schema exists in PostgreSQL."""
    engine = get_engine()
    with engine.connect() as conn:
        conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema_name};"))
        logger.info(f"✅ Schema '{schema_name}' created or already exists.")

def create_warehouse_tables():
    """Create optimized tables for structured storage."""
    engine = get_engine()

    # Ensure schema exists
    create_schema()

    with engine.connect() as conn:
        # Ensure the table columns match `cleaned_telegram_messages`
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS warehouse.telegram_messages_dw (
                id SERIAL PRIMARY KEY,
                message TEXT NOT NULL,
                sentiment FLOAT,
                subjectivity FLOAT,
                hour_of_day INT,
                "day_of_week" TEXT,  -- Ensure column name is quoted
                is_weekend BOOLEAN,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))

        # Ensure the object detection table exists
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
                detection_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))

        logger.info("✅ Warehouse tables created successfully.")

def create_indexes():
    """Optimize tables with indexes for faster queries."""
    engine = get_engine()
    with engine.connect() as conn:
        # **Ensure tables exist before creating indexes**
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_telegram_messages_hour ON warehouse.telegram_messages_dw (hour_of_day);"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_day_of_week ON warehouse.telegram_messages_dw (day_of_week);"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_detection_class ON warehouse.object_detection_dw (class);"))

        logger.info("✅ Indexes created successfully.")

def load_data_into_warehouse(source_table, target_table):
    """Load cleaned data into warehouse tables with correct column names."""
    engine = get_engine()
    
    query = f"""
    INSERT INTO warehouse.{target_table} 
    (message, sentiment, subjectivity, hour_of_day, day_of_week, is_weekend)
    SELECT message, sentiment, subjectivity, hour_of_day,
        CASE 
            WHEN "day_Monday" THEN 'Monday'
            WHEN "day_Tuesday" THEN 'Tuesday'
            WHEN "day_Wednesday" THEN 'Wednesday'
            WHEN "day_Thursday" THEN 'Thursday'
            WHEN "day_Friday" THEN 'Friday'
            WHEN "day_Saturday" THEN 'Saturday'
            WHEN "day_Sunday" THEN 'Sunday'
            ELSE 'Unknown' 
        END AS day_of_week,  
        is_weekend 
    FROM public.{source_table};
    """

    with engine.connect() as conn:
        conn.execute(text(f"TRUNCATE TABLE warehouse.{target_table};"))  # Clear existing data
        conn.execute(text(query))
    
    print(f"✅ Data loaded into warehouse.{target_table} from {source_table}.")
