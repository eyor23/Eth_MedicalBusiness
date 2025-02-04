import streamlit as st
import requests
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

# Set up the Streamlit interface
st.title("Data Management App")

# Create sidebar
option = st.sidebar.selectbox(
    "Choose a table to manage",
    ("Detections", "Telegram Messages")
)

# Detections management
if option == "Detections":
    st.header("Detections")

    # Create a new detection
    st.subheader("Create a new detection")
    xmin = st.number_input("xmin", min_value=0.0, step=0.1)
    ymin = st.number_input("ymin", min_value=0.0, step=0.1)
    xmax = st.number_input("xmax", min_value=0.0, step=0.1)
    ymax = st.number_input("ymax", min_value=0.0, step=0.1)
    confidence = st.number_input("Confidence", min_value=0.0, max_value=1.0, step=0.01)
    class_label = st.text_input("Class Label")

    if st.button("Create Detection"):
        bbox = [xmin, ymin, xmax, ymax]
        response = requests.post(f"{BASE_URL}/detections/", json={
            "bbox": bbox,
            "confidence": confidence,
            "class_label": class_label
        })
        if response.status_code == 200:
            st.success("Detection created successfully!")
        else:
            st.error(f"Error: {response.text}")

    # Read all detections
    st.subheader("Read all detections")
    if st.button("Get Detections"):
        response = requests.get(f"{BASE_URL}/detections/")
        if response.status_code == 200:
            detections = response.json()
            for detection in detections:
                st.write(detection)
        else:
            st.error(f"Error: {response.text}")

    # Delete a detection
    st.subheader("Delete a detection")
    delete_detection_id = st.number_input("Detection ID to delete", min_value=0)
    if st.button("Delete Detection"):
        response = requests.delete(f"{BASE_URL}/detections/{delete_detection_id}")
        if response.status_code == 200:
            st.success("Detection deleted successfully!")
        else:
            st.error(f"Error: {response.text}")

# Telegram Messages management
elif option == "Telegram Messages":
    st.header("Telegram Messages")

    # Create a new message
    st.subheader("Create a new message")
    channel_title = st.text_input("Channel Title")
    channel_username = st.text_input("Channel Username")
    message_id = st.number_input("Message ID", min_value=0)
    message = st.text_area("Message")
    message_date = st.date_input("Message Date")
    message_time = st.time_input("Message Time")
    media_path = st.text_input("Media Path")
    emoji_used = st.text_input("Emoji Used")
    youtube_links = st.text_input("YouTube Links")

    if st.button("Create Message"):
        message_datetime = datetime.combine(message_date, message_time)
        response = requests.post(f"{BASE_URL}/messages/", json={
            "channel_title": channel_title,
            "channel_username": channel_username,
            "message_id": message_id,
            "message": message,
            "message_date": message_datetime.isoformat(),
            "media_path": media_path,
            "emoji_used": emoji_used,
            "youtube_links": youtube_links
        })
        if response.status_code == 200:
            st.success("Message created successfully!")
        else:
            st.error(f"Error: {response.text}")

    # Read all messages
    st.subheader("Read all messages")
    if st.button("Get Messages"):
        response = requests.get(f"{BASE_URL}/messages/")
        if response.status_code == 200:
            messages = response.json()
            for message in messages:
                st.write(message)
        else:
            st.error(f"Error: {response.text}")

    # Delete a message
    st.subheader("Delete a message")
    delete_message_id = st.number_input("Message ID to delete", min_value=0)
    if st.button("Delete Message"):
        response = requests.delete(f"{BASE_URL}/messages/{delete_message_id}")
        if response.status_code == 200:
            st.success("Message deleted successfully!")
        else:
            st.error(f"Error: {response.text}")

# Running the Streamlit App
# Run this command in your terminal: streamlit run streamlit_app.py
