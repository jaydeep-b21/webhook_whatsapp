import httpx
import logging
import os
from webhook_app.models import Message
import asyncio
from datetime import datetime
 
 
 
# Create a file handler to log to 'app.log' file
file_handler = logging.FileHandler(f'logs/app.log')
 
# Create a console handler for real-time logging on the console
console_handler = logging.StreamHandler()
 
# Create a formatter and set it for both handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)
 
# Set up the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
 
# Add both file and console handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)
# Set up logging
logger = logging.getLogger(__name__)
 
class WhatsAppService:
    BASE_URL = "https://graph.facebook.com/v21.0/552952211226957/messages"
    ACCESS_TOKEN = "EAAHwhtJUljUBO7VqLQzHAY7l6eWgfJzR7zHSXGZCtgkfvT2hC9om6LJe89Fj2fmX9ZCBqrP9IFgH5Q7SikQcsOmhrAQqV3NZCZC4qNUFwVzL9ZBQFx6dIUygZAiZBimaKQdBqUJa9EiiyAJDDl23DjqX42Xfuj8zZBihS5qz5oM82hrfOARBkrzl5Xh0RGIJIdrZAzkKgUjouibCDXVvmACJPsgSd6wAZD"
 
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {self.ACCESS_TOKEN}",
            "Content-Type": "application/json",
        }
 
    async def send_message(self, mobile_no, message):
        """
        Sends a message asynchronously via the WhatsApp Business API.
        :param mobile_no: Recipient's phone number
        :param message: Message content
        :return: Tuple (success: bool, response: dict)
        """
        payload = {
            "messaging_product": "whatsapp",
            "to": mobile_no,
            "text": {"body": message},
        }
 
        try:
            logger.info(f"Sending message to {mobile_no}: {message}")
            async with httpx.AsyncClient() as client:
                response = await client.post(self.BASE_URL, json=payload, headers=self.headers)
            print(response.json())
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            await asyncio.to_thread(
                                Message.objects.create,
                                sender="Jaydeep",
                                receiver=mobile_no,
                                content=message,
                                timestamp=timestamp,
                                status="Sent",
                            )
            if response.status_code == 200:
                logger.info(f"Message successfully sent to {mobile_no}")
                return True, response.json()  # Returns a tuple of success and response data
            else:
                logger.error(f"Failed to send message: {response.text}")
                return False, response.json()
           
 
        except Exception as e:
            logger.exception("An error occurred while sending the message.")
            return False, {"error": str(e)}