import os
import cv2
import torch
import logging
import psycopg2
from dotenv import load_dotenv
from ultralytics import YOLO

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Define input directory
INPUT_DIR = r"D:\Kifya_training\Week 7\EthioMart-Amharic-NER-System\data\processed\images"

# Database credentials
DB_NAME = os.getenv("DB_NAME", "medical_warehouse")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "your_password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

# Load YOLOv5 model
model = YOLO("yolov5s.pt")

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
        logger.error(f"Database connection error: {e}")
        return None

def store_detection_results(image_name, detections):
    """Store YOLO detection results in PostgreSQL."""
    conn = connect_to_db()
    if not conn:
        return

    insert_query = """
        INSERT INTO object_detection_results 
        (image_name, class_label, confidence, bbox_x, bbox_y, bbox_width, bbox_height) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    try:
        with conn.cursor() as cursor:
            for detection in detections:
                class_label, confidence, bbox = detection
                cursor.execute(insert_query, (image_name, class_label, confidence, *bbox))
        conn.commit()
        logger.info(f"Stored detection results for {image_name}")
    except Exception as e:
        logger.error(f"Error saving results: {e}")
        conn.rollback()
    finally:
        conn.close()

def run_object_detection(input_dir=INPUT_DIR):
    """Run YOLO object detection and store results."""
    for filename in os.listdir(input_dir):
        if filename.endswith((".jpg", ".jpeg", ".png")):
            img_path = os.path.join(input_dir, filename)
            results = model(img_path)
            
            detections = []
            for result in results:
                for box in result.boxes:
                    class_label = model.names[int(box.cls)]
                    confidence = float(box.conf)
                    bbox = [float(coord) for coord in box.xywh[0]]  # x, y, width, height
                    detections.append((class_label, confidence, bbox))
            
            store_detection_results(filename, detections)

if __name__ == "__main__":
    run_object_detection()
