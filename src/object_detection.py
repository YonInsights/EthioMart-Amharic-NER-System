import os
import cv2
import torch
import pandas as pd
import logging
from datetime import datetime

# Set up logger (using your logging_utils or a basic config)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def load_model():
    """
    Load the pre-trained YOLOv5 model from PyTorch Hub.
    """
    try:
        model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        logger.info("YOLOv5 model loaded successfully.")
        return model
    except Exception as e:
        logger.error(f"Error loading YOLOv5 model: {str(e)}")
        raise

def preprocess_image(image_path):
    """
    Preprocess the image if needed (here we simply read it).
    """
    try:
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Unable to load image at {image_path}")
        # Convert BGR to RGB for YOLO model compatibility
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return img
    except Exception as e:
        logger.error(f"Error preprocessing image {image_path}: {str(e)}")
        raise

def detect_objects_in_images(input_dir):
    """
    Run YOLO object detection on all images in the input_dir.
    Returns a Pandas DataFrame with detection results.
    """
    model = load_model()
    results_list = []

    # List all image files in input directory
    image_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    logger.info(f"Found {len(image_files)} images in {input_dir}")

    for image_file in image_files:
        image_path = os.path.join(input_dir, image_file)
        try:
            img = preprocess_image(image_path)
            results = model(img)
            # Parse results: results.xyxy[0] returns bounding boxes with 
            # [xmin, ymin, xmax, ymax, confidence, class]
            for *box, conf, cls in results.xyxy[0].tolist():
                class_name = results.names[int(cls)]
                results_list.append({
                    "image_file": image_file,
                    "box_xmin": box[0],
                    "box_ymin": box[1],
                    "box_xmax": box[2],
                    "box_ymax": box[3],
                    "confidence": conf,
                    "class": class_name,
                    "detection_time": datetime.now()
                })
            logger.info(f"Processed image: {image_file}")
        except Exception as e:
            logger.error(f"Error processing image {image_file}: {str(e)}")
            continue

    df_results = pd.DataFrame(results_list)
    return df_results

def save_detection_results(df, output_path):
    """
    Save the detection results DataFrame to a CSV file.
    """
    try:
        df.to_csv(output_path, index=False)
        logger.info(f"Detection results saved to {output_path}")
    except Exception as e:
        logger.error(f"Error saving detection results: {str(e)}")
        raise

# If you need a function to store results into a database,
# you can integrate with db_operations.write_data_to_table as shown below:
def store_detection_results_in_db(df, write_function, table_name):
    """
    Store detection results in the database using the provided write function.
    'write_function' should be a callable that takes (DataFrame, table_name).
    """
    try:
        write_function(df, table_name)
        logger.info(f"Detection results stored in database table: {table_name}")
    except Exception as e:
        logger.error(f"Error storing detection results in database: {str(e)}")
        raise
