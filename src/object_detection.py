import os
import cv2
import torch
import logging
from ultralytics import YOLO

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Define input and output directories
INPUT_DIR = "data/processed/images/"
OUTPUT_DIR = "data/processed/detections/"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load YOLOv5 model (pretrained on COCO dataset)
model = YOLO("yolov5s.pt")  # Using YOLOv5 small model

def run_object_detection(input_dir=INPUT_DIR, output_dir=OUTPUT_DIR):
    """
    Run YOLO object detection on images and save results.

    Args:
        input_dir (str): Directory containing preprocessed images.
        output_dir (str): Directory to save detection results.
    """
    for filename in os.listdir(input_dir):
        if filename.endswith((".jpg", ".jpeg", ".png")):
            img_path = os.path.join(input_dir, filename)
            
            # Run YOLO detection
            results = model(img_path)
            
            # Save detections
            for result in results:
                result.save(output_dir)
                logger.info(f"Detection saved for {filename}")

if __name__ == "__main__":
    run_object_detection()
