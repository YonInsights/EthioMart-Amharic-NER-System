import os
import logging
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import MessageMediaPhoto
import pandas as pd

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Telegram API credentials
API_ID = os.getenv('TELEGRAM_API_ID')
API_HASH = os.getenv('TELEGRAM_API_HASH')
PHONE_NUMBER = os.getenv('TELEGRAM_PHONE_NUMBER')

# Define the output directories for scraped data
OUTPUT_DIR = os.path.join(os.getcwd(), 'data', 'raw')
IMAGE_DIR = os.path.join(OUTPUT_DIR, 'images')
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(IMAGE_DIR, exist_ok=True)

# Initialize the Telegram client
client = TelegramClient('session_name', API_ID, API_HASH)

async def scrape_channel(channel_username, limit=100):
    """
    Scrape messages and images from a Telegram channel.
    
    Args:
        channel_username (str): The username of the Telegram channel.
        limit (int): The number of messages to scrape.
    """
    try:
        logger.info(f"Scraping messages from channel: {channel_username}")
        
        # Connect to Telegram
        await client.start(PHONE_NUMBER)
        
        # Get the channel entity
        channel = await client.get_entity(channel_username)
        
        # Scrape messages
        messages = await client(GetHistoryRequest(
            peer=channel,
            limit=limit,
            offset_date=None,
            offset_id=0,
            max_id=0,
            min_id=0,
            add_offset=0,
            hash=0
        ))
        
        # Extract relevant data from messages
        data = []
        for message in messages.messages:
            message_data = {
                'id': message.id,
                'date': message.date,
                'message': message.message,
                'views': message.views if hasattr(message, 'views') else None,
                'media': bool(message.media)
            }
            data.append(message_data)
            
            # Download images if present
            if isinstance(message.media, MessageMediaPhoto):
                image_path = os.path.join(IMAGE_DIR, f"{channel_username}_{message.id}.jpg")
                await client.download_media(message, file=image_path)
                logger.info(f"Saved image: {image_path}")
        
        # Save the data to a CSV file
        df = pd.DataFrame(data)
        output_file = os.path.join(OUTPUT_DIR, f'{channel_username}_messages.csv')
        df.to_csv(output_file, index=False)
        logger.info(f"Saved {len(data)} messages to {output_file}")
    
    except Exception as e:
        logger.error(f"Error scraping channel {channel_username}: {e}")

async def main():
    """
    Main function to scrape multiple Telegram channels.
    """
    channels = [
        'DoctorsET',  
        'CheMed123',
        'lobelia4cosmetics', 
        'yetenaweg',
        'EAHCI'  
    ]
    
    for channel in channels:
        await scrape_channel(channel, limit=100)  # Scrape 100 messages per channel

# Run the scraper
if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())
