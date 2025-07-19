from mongoengine import connect, disconnect, DEFAULT_CONNECTION_NAME
from dotenv import load_dotenv
import os
from loguru import logger

load_dotenv()

def connect_db():
    try:
        connect(
            alias=DEFAULT_CONNECTION_NAME,
            host=os.environ.get("MONGODB_URI"),
        )
        logger.info(f"Connected to the database successfully")
    except Exception as e:
        logger.error(f"Failed to connect to the database: {e}")
        
def disconnect_db():
    try:
        disconnect(
            alias=DEFAULT_CONNECTION_NAME
        )
        logger.info("Disconnected from the database successfully.")
    except Exception as e:
        logger.error(f"Failed to disconnect from the database: {e}")

if __name__ == "__main__":
    connect_db()