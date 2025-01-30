import os
import cv2
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Define input and output directories
INPUT_DIR = "data/raw/images/"
OUTPUT_DIR = "data/processed/images/"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def preprocess_images(input_dir=INPUT_DIR, output_dir=OUTPUT_DIR, target_size=(640, 640)):
    """
    Preprocess images by resizing and converting them to JPEG format.

    Args:
        input_dir (str): Directory containing raw images.
        output_dir (str): Directory to save preprocessed images.
        target_size (tuple): Target size for YOLO model (default: 640x640).
    """
    for filename in os.listdir(input_dir):
        if filename.endswith((".jpg", ".jpeg", ".png")):
            img_path = os.path.join(input_dir, filename)
            img = cv2.imread(img_path)

            if img is None:
                logger.warning(f"Skipping invalid image: {img_path}")
                continue

            # Resize the image
            img_resized = cv2.resize(img, target_size)

            # Save the preprocessed image
            output_path = os.path.join(output_dir, filename)
            cv2.imwrite(output_path, img_resized)
            logger.info(f"Processed and saved: {output_path}")

if __name__ == "__main__":
    preprocess_images()
