# src/cldb_operations.py

import psycopg2
import pandas as pd
from psycopg2 import sql

# Database connection details
db_config = {
    'dbname': 'ethiopian_medical_db',
    'user': 'postgres',
    'password': '1212',
    'host': 'localhost',
    'port': '5432'
}

def connect_to_db():
    """Connect to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(**db_config)
        print("Connected to the database successfully!")
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

def close_connection(conn):
    """Close the database connection."""
    if conn:
        conn.close()
        print("Database connection closed.")

def read_data_from_table(table_name):
    """Read data from a specified table into a Pandas DataFrame."""
    conn = connect_to_db()
    if conn:
        try:
            # Construct the query as a string
            query = f"SELECT * FROM {table_name}"
            print(f"Executing query: {query}")  # Debug: Print the query
            df = pd.read_sql(query, conn)  # Pass the string query to pandas
            print(f"Data read from table '{table_name}' successfully!")
            return df
        except Exception as e:
            print(f"Error reading data from table '{table_name}': {e}")
            return None
        finally:
            close_connection(conn)
    else:
        print("Failed to connect to the database.")
        return None
