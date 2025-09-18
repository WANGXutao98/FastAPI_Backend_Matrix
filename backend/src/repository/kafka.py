from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from src.config.manager import settings

class KafkaManager:
    def __init__(self):
        self.bootstrap_servers = settings.KAFKA_BOOTSTRAP_SERVERS
        self.topic = settings.KAFKA_TOPIC

    async def get_producer(self):
        producer = AIOKafkaProducer(bootstrap_servers=self.bootstrap_servers)
        await producer.start()
        return producer

    async def get_consumer(self, group_id: str):
        consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id=group_id
        )
        await consumer.start()
        return consumer

kafka_manager: KafkaManager = KafkaManager()