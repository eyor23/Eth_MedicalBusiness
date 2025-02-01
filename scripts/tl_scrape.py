from telethon import TelegramClient
import logging
import asyncio
import csv
import os
from urllib.parse import urlparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env')
TG_API_ID = os.getenv('TG_API_ID')
TG_API_HASH = os.getenv('TG_API_HASH')
phone = os.getenv('PHONE')

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to extract username from URL
def extract_username(url):
    parsed_url = urlparse(url)
    return parsed_url.path.strip('/')

# Function to scrape data from a single channel
async def scrape_channel(client, channel_url, writer, media_dir):
    channel_username = extract_username(channel_url)
    entity = await client.get_entity(channel_username)
    channel_title = getattr(entity, 'title', channel_username)  # Extract the channel's title if it exists, otherwise use the username
    logging.info(f"Scraping data from channel: {channel_title}")

    message_count = 0
    async for message in client.iter_messages(entity, limit=200):  # Limit to 100 messages
        if message_count >= 100:
            break  # Stop after 100 messages
        media_path = None
        
        if message.media and hasattr(message.media, 'photo'):
            # Create a unique filename for the photo
            filename = f"{channel_username}_{message.id}.jpg"
            media_path = os.path.join(media_dir, filename)
            # Download the media to the specified directory if it's a photo
            await client.download_media(message.media, media_path)

        # Write the channel title along with other data
        writer.writerow([channel_title, channel_username, message.id, message.message, message.date, media_path])
        message_count += 1  # Increment the message count

    logging.info(f"Finished scraping data from channel: {channel_title}")

async def main():
    async with client:
        await client.start()
        logging.info("Telegram client started.")
        
        # Create a directory for media files
        media_dir = 'photos'
        os.makedirs(media_dir, exist_ok=True)
        logging.info("Media directory created.")
        
        # Open the CSV file and prepare the writer
        with open('telegram_data.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Channel Title', 'Channel Username', 'ID', 'Message', 'Date', 'Media Path'])  # Include channel title in the header
            
            # List of channels to scrape
            channels = [
                'https://t.me/DoctorsET',
                'https://t.me/Chemed',
                'https://t.me/lobelia4cosmetics',
                'https://t.me/yetenaweg',
                'https://t.me/EAHCI'
                # Add more channels here from https://et.tgstat.com/medicine
            ]
            
            # Iterate over channels and scrape data into the single CSV file
            for channel in channels:
                await scrape_channel(client, channel, writer, media_dir)
                logging.info(f"Scraped data from {channel}")

# Initialize the client once
client = TelegramClient('scraping_session', TG_API_ID, TG_API_HASH)

# If running inside an existing event loop, use await
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError:
        # If there is an event loop already running, use await
        asyncio.ensure_future(main())