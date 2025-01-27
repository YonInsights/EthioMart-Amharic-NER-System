import os
import logging
from datetime import datetime
from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaPhoto
from telethon.errors import ChannelPrivateError, FloodWaitError
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    filename='results/logs/scraping.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class TelegramScraper:
    def __init__(self):
        self.api_id = os.getenv("API_ID")
        self.api_hash = os.getenv("API_HASH")
        self.client = TelegramClient('anon', self.api_id, self.api_hash)
        
        # Channels to scrape (update this list)
        self.text_channels = [
            "DoctorsET",        # Medical professionals
            "CheMed123",        # Chemed Channel
            "lobelia4cosmetics",# Cosmetic products
            "yetenaweg",        # Ethiopian healthcare
            "EAHCI"             # Ethiopian health org
        ]
        
        self.image_channels = [
            "CheMed123",        # For object detection
            "lobelia4cosmetics" # For product images
        ]

    async def download_image(self, message, channel_name):
        """Download images from messages"""
        try:
            date_str = message.date.strftime("%Y%m%d_%H%M%S")
            filename = f"data/raw/images/{channel_name}_{date_str}.jpg"
            await message.download_media(file=filename)
            logging.info(f"Saved image: {filename}")
        except Exception as e:
            logging.error(f"Failed to download image: {str(e)}")

    async def scrape_channel(self, channel_name: str, limit: int = 50):
        """Scrape both text and images from a channel"""
        try:
            text_data = []
            async with self.client:
                async for message in self.client.iter_messages(channel_name, limit=limit):
                    # Collect text data
                    text_data.append({
                        "date": message.date,
                        "text": message.text,
                        "channel": channel_name
                    })
                    
                    # Download images if in image channels
                    if channel_name in self.image_channels and isinstance(message.media, MessageMediaPhoto):
                        await self.download_image(message, channel_name)
            
            return pd.DataFrame(text_data)
            
        except (ChannelPrivateError, FloodWaitError) as e:
            logging.error(f"Error in {channel_name}: {str(e)}")
            return pd.DataFrame()

    def save_text_data(self, df: pd.DataFrame, channel_name: str):
        """Save text data to CSV"""
        if not df.empty:
            filepath = f"data/raw/text/{channel_name}_{datetime.now().strftime('%Y%m%d')}.csv"
            df.to_csv(filepath, index=False)
            logging.info(f"Saved {len(df)} messages from {channel_name}")

    async def run_scraper(self):
        """Main scraping function"""
        for channel in self.text_channels + self.image_channels:
            df = await self.scrape_channel(channel, limit=20)  # Start with 20 messages/channel
            if channel in self.text_channels:
                self.save_text_data(df, channel)

if __name__ == "__main__":
    scraper = TelegramScraper()
    
    # Create necessary folders
    os.makedirs("data/raw/text", exist_ok=True)
    os.makedirs("data/raw/images", exist_ok=True)
    
    # Run the scraper
    with scraper.client:
        scraper.client.loop.run_until_complete(scraper.run_scraper())