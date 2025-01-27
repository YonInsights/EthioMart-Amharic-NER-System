import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection details
DB_NAME = os.getenv("DB_NAME", "medical_warehouse")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "your_password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

# File path for text data
DATA_PATH = r"D:\Kifya_training\Week 7\EthioMart-Amharic-NER-System\data\raw\text"

def connect_to_db():
    """Establishes a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def load_csv_to_db(file_path, conn):
    """Reads a CSV file and inserts the data into the raw_text_data table."""
    try:
        # Read CSV into DataFrame
        df = pd.read_csv(file_path)

        # Prepare SQL query
        insert_query = """
            INSERT INTO raw_text_data (message_date, message_text, channel_name, loaded_at)
            VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
        """

        # Insert data row by row
        with conn.cursor() as cursor:
            for _, row in df.iterrows():
                cursor.execute(
                    insert_query,
                    (row['date'], row['text'], row['channel'])
                )
        conn.commit()
        print(f"Data from {os.path.basename(file_path)} loaded successfully.")
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        conn.rollback()

def main():
    """Main function to load all CSV files into the database."""
    conn = connect_to_db()
    if not conn:
        return

    try:
        # List all CSV files in the directory
        csv_files = [f for f in os.listdir(DATA_PATH) if f.endswith('.csv')]

        for file in csv_files:
            file_path = os.path.join(DATA_PATH, file)
            load_csv_to_db(file_path, conn)
    finally:
        conn.close()

if __name__ == "__main__":
    main()
