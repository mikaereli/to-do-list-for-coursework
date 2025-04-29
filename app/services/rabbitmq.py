import aio_pika
import json

RABBITMQ_URL = "amqp://guest:guest@rabbitmq:5672/"

async def publish_task(number: int, title: str, description: str, chat_id: int = None):
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("telegram_notifications", durable=True)

        message_body = {
            "number": number,
            "title": title,
            "description": description
        }
        if chat_id:
            message_body["chat_id"] = chat_id

        await channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps(message_body).encode()),
            routing_key=queue.name
        )
