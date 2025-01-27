import os
import psycopg2
import csv

# Database connection details
db_config = {
    'dbname': 'ethiopian_medical_db',  # database name
    'user': 'postgres',               # PostgreSQL username
    'password': '1212',               # PostgreSQL password (string required)
    'host': 'localhost',              # database host
    'port': '5432'                    # database port
}

# Folder containing CSV files
csv_folder = 'D:/Kifya_training/Week 7/EthioMart-Amharic-NER-System/data/raw'

# Connect to the database
conn = psycopg2.connect(**db_config)
cur = conn.cursor()

# Function to validate and clean data
def validate_row(row):
    try:
        # Convert views to integer if not None
        row[3] = int(float(row[3])) if row[3] else None
        # Other transformations can be added here if needed
        return row
    except (ValueError, IndexError) as e:
        print(f"Invalid row skipped: {row} | Error: {e}")
        return None

# Function to insert data from a CSV file into the database
def insert_csv_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip the header row
            for row in reader:
                row = validate_row(row)  # Clean and validate row
                if row:
                    cur.execute(
                        "INSERT INTO telegram_messages (id, date, message, views, media) VALUES (%s, %s, %s, %s, %s)",
                        row
                    )
        conn.commit()
        print(f"Data from {os.path.basename(file_path)} has been loaded into the database.")
    except Exception as e:
        conn.rollback()  # Rollback in case of an error
        print(f"Error loading {os.path.basename(file_path)}: {e}")

# Loop through all CSV files in the folder
for filename in os.listdir(csv_folder):
    if filename.endswith('.csv'):
        file_path = os.path.join(csv_folder, filename)
        insert_csv_data(file_path)

# Close the connection
cur.close()
conn.close()

print("All CSV files have been processed.")
