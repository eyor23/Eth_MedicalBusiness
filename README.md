# Data Management Project

This project involves scraping Telegram messages, detecting objects in images, storing data in a PostgreSQL database, exposing the data using FastAPI, and providing a user-friendly interface using Streamlit.

## Task 1: Telegram Scraping

I start by scraping messages from Telegram channels. The scraped data includes channel title, channel username, message ID, message content, message date, media path, emojis used, and YouTube links. The data is saved in a PostgreSQL database.

## Task 2: Object Detection and Data Storage

I perform object detection on images and store the detection results in the PostgreSQL database. Each detection includes bounding box coordinates (xmin, ymin, xmax, ymax), confidence score, and class label. The bounding box coordinates are stored as a comma-separated string for easy management.

## Task 3: Exposing Data using FastAPI

I set up a FastAPI application to expose the data through RESTful API endpoints. The API provides CRUD operations for both the `detections` and `telegram_messages` tables.

### Detections Endpoints
- **Create Detection**: `POST /detections/`
- **Read All Detections**: `GET /detections/`
- **Read Detection by ID**: `GET /detections/{detection_id}`
- **Update Detection**: `PUT /detections/{detection_id}`
- **Delete Detection**: `DELETE /detections/{detection_id}`

### Telegram Messages Endpoints
- **Create Message**: `POST /messages/`
- **Read All Messages**: `GET /messages/`
- **Read Message by ID**: `GET /messages/{message_id}`
- **Update Message**: `PUT /messages/{message_id}`
- **Delete Message**: `DELETE /messages/{message_id}`

## Task 4: Streamlit Interface

I create a simple Streamlit app to manage the data. The app provides an interface for creating, reading, and deleting records in both the `detections` and `telegram_messages` tables.

### Running the Project

1. **Install Dependencies**:
   ```sh
   pip install -r requirements.txt
2. **Run FastAPI Server**:
    ```sh
    uvicorn main:app --reload
3. **Run Streamlit App:**:
    ```sh
    streamlit run streamlit.py

## License

This `README.md` file provides a concise summary of the project, including the steps involved, endpoints exposed, and instructions for running the project. Let me know if you need any further modifications or additional details!

