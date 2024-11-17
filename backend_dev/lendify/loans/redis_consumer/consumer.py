import json
import redis
import logging
from django.conf import settings
from django.db import transaction
from time import sleep
from typing import Dict, Any

logger = logging.getLogger(__name__)

class RedisStreamConsumer:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True
        )
        self.stream_key = 'accepted_loan_applications'
        self.last_id = '0'  # Start reading from beginning of stream

    def run(self):
        """Main loop to consume messages"""
        logger.info(f"Starting Redis Stream consumer for {self.stream_key}")
        
        while True:
            try:
                # Read new messages from the stream
                messages = self.redis_client.xread(
                    streams={self.stream_key: self.last_id},
                    count=1,  # Read one message at a time
                    block=5000  # Block for 5 seconds if no messages
                )
                
                if not messages:
                    continue

                # Process messages
                for stream_name, stream_messages in messages:
                    for message_id, data in stream_messages:
                        print("\n=== New Message Received ===")
                        print(f"Message ID: {message_id}")
                        print("Data:")
                        for key, value in data.items():
                            print(f"  {key}: {value}")
                        print("========================\n")
                        
                        # Update last_id to get next message
                        self.last_id = message_id
                
            except Exception as e:
                print(f"Error: {str(e)}")
                sleep(1)  # Wait before retrying