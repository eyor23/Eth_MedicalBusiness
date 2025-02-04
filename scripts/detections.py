import os
import torch
import cv2
import psycopg2
from dotenv import load_dotenv
import logging
from pathlib import Path

# Load environment variables
load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_password = os.getenv('DB_password')

# Setup logging
logging.basicConfig(level=logging.INFO, filename='scraping.log', 
                    format='%(asctime)s %(levelname)s:%(message)s')

# Connect to PostgreSQL database
conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_password
)

cur = conn.cursor()

# Create table if not exists
cur.execute('''
CREATE TABLE IF NOT EXISTS detections (
    id SERIAL PRIMARY KEY,
    bbox TEXT,
    confidence FLOAT,
    class_label TEXT
)
''')
conn.commit()

# Load YOLO model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

def process_image(image_path):
    image = cv2.imread(image_path)
    results = model(image)
    return results

def extract_detection_data(results):
    detection_data = []
    for result in results.xyxy[0].cpu().numpy():
        bbox = result[:4].tolist()
        confidence = float(result[4])  # Convert numpy.float32 to native float
        class_label = model.names[int(result[5])]
        detection_data.append((bbox, confidence, class_label))
    return detection_data

def store_to_database(detection_data):
    for bbox, confidence, class_label in detection_data:
        cur.execute(
            'INSERT INTO detections (bbox, confidence, class_label) VALUES (%s, %s, %s)',
            (str(bbox), confidence, class_label)
        )
    conn.commit()

def log_detection(detection_data):
    for data in detection_data:
        logging.info(f'Detected {data[2]} with confidence {data[1]} at {data[0]}')

def process_image_directory(directory_path):
    detection_data = []
    for filename in os.listdir(directory_path):
        image_path = os.path.join(directory_path, filename)
        if os.path.isfile(image_path):
            image = cv2.imread(image_path)
            if image is not None:
                results = process_image(image_path)
                data = extract_detection_data(results)
                detection_data.extend(data)
            else:
                print(f"Warning: Couldn't read image {image_path}")
    return detection_data

def main():
    directory_path = 'C:\\Users\\user\\Desktop\\Kifiya\\Eth_MedicalBusiness\\data\\lobelia4cosmetics photos'
    detection_data = process_image_directory(directory_path)
    store_to_database(detection_data)
    log_detection(detection_data)

if __name__ == '__main__':
    main()

# Close the database connection
cur.close()
conn.close()