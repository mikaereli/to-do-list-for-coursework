# import aio_pika
# import json
#
# RABBITMQ_URL = "amqp://guest:guest@localhost/"
#
# async def publish_task(number: int, title: str, description: str):
#     connection = await aio_pika.connect_robust(RABBITMQ_URL)
#     async with connection:
#         channel = await connection.channel()
#         queue = await channel.declare_queue("task_notifications", durable=True)
#
#         message_body = json.dumps({
#             "number": number,
#             "title": title,
#             "description": description
#         })
#
#         await channel.default_exchange.publish(
#             aio_pika.Message(body=message_body.encode()),
#             routing_key=queue.name
#         )
