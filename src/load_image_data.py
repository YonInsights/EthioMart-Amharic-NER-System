import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection details
DB_NAME = os.getenv("DB_NAME", "medical_warehouse")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "1212")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

# Image directory
IMAGE_DIR = r"D:\Kifya_training\Week 7\EthioMart-Amharic-NER-System\data\raw\images"

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

def load_images_to_db(conn):
    """Inserts image metadata into the image_data table."""
    try:
        cursor = conn.cursor()
        insert_query = """
            INSERT INTO image_data (image_name, image_path, channel_name)
            VALUES (%s, %s, %s)
        """

        # Scan the image directory
        for image_file in os.listdir(IMAGE_DIR):
            if image_file.endswith((".jpg", ".png", ".jpeg")):  # Check for image files
                channel_name = image_file.split('_')[0]  # Extract channel name from file name
                image_path = os.path.join(IMAGE_DIR, image_file)

                # Insert into database
                cursor.execute(insert_query, (image_file, image_path, channel_name))
        
        conn.commit()
        print("Image metadata loaded successfully.")
    except Exception as e:
        print(f"Error loading image data: {e}")
        conn.rollback()

def main():
    """Main function to load image metadata."""
    conn = connect_to_db()
    if not conn:
        return

    try:
        load_images_to_db(conn)
    finally:
        conn.close()

if __name__ == "__main__":
    main()
