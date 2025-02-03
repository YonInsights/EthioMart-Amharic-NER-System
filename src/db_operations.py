import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Database configuration
DB_NAME = "ethiopian_medical_db"
DB_USER = "postgres"
DB_PASSWORD = "1212"
DB_HOST = "localhost"
DB_PORT = "5432"

# Create SQLAlchemy engine
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency for FastAPI
def get_db():
    """Provide a database session to FastAPI routes."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# Create SQLAlchemy engine
def get_engine():
    """Create and return a SQLAlchemy database engine."""
    try:
        engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
        print("SQLAlchemy engine created successfully!")
        return engine
    except Exception as e:
        print(f"Error creating SQLAlchemy engine: {e}")
        return None

def read_data_from_table(table_name):
    """Read data from a specified PostgreSQL table into a Pandas DataFrame."""
    engine = get_engine()
    if engine:
        try:
            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql(query, engine)
            print(f"Data read from table '{table_name}' successfully!")
            return df
        except Exception as e:
            print(f"Error reading data from table '{table_name}': {e}")
            return None
    else:
        print("Failed to connect to the database.")
        return None

def write_data_to_table(df, table_name):
    """Write a Pandas DataFrame to a PostgreSQL table using SQLAlchemy."""
    engine = get_engine()
    if engine:
        try:
            df.to_sql(table_name, engine, if_exists='replace', index=False, method='multi')
            print(f"Data written successfully to '{table_name}'")
        except Exception as e:
            print(f"Error writing data to table '{table_name}': {e}")
    else:
        print("Failed to connect to the database.")
