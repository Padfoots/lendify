from django.core.management.base import BaseCommand
from loans.redis_consumer.consumer import RedisStreamConsumer

class Command(BaseCommand):
    help = 'Runs the Redis Stream consumer'

    def handle(self, *args, **options):
        consumer = RedisStreamConsumer()
        consumer.run()