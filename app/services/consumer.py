# import asyncio
# import json
# import os
#
#
# import aio_pika
# from telegram import Bot
# from telegram.constants import ParseMode
# from telegram.error import TelegramError
#
#
# RABBITMQ_URL = os.environ.get("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")
# TELEGRAM_BOT_TOKEN = 'так уж и быть скажу будто бы, а env мне лень было писать и отдельный конфиг файл так что простите'
#
# # Initialize the bot
# bot = Bot(token=TELEGRAM_BOT_TOKEN)
#
# async def main():
#     try:
#         connection = await aio_pika.connect_robust(RABBITMQ_URL)
#
#         async with connection:
#             channel = await connection.channel()
#             queue = await channel.declare_queue("telegram_notifications", durable=True)
#
#             async with queue.iterator() as queue_iter:
#                 async for message in queue_iter:
#                     async with message.process():
#                         try:
#                             # Parse the message body
#                             body = json.loads(message.body.decode())
#                             number = body.get("number")
#                             title = body.get("title")
#                             description = body.get("description")
#                             chat_id = body.get("chat_id")
#
#                             # Send the message to Telegram
#                             await send_telegram_message(number, title, description, chat_id)
#                         except Exception as e:
#                             print(f"Error processing message: {e}")
#     except Exception as e:
#         print(f"Error connecting to RabbitMQ: {e}")
#         await asyncio.sleep(5)
#         await main()  # Retry connecting
#
# async def send_telegram_message(number: int, title: str, description: str, chat_id=None):
#     try:
#         message = f"<b>Task #{number}</b>\n<b>Title:</b> {title}\n<b>Description:</b> {description}"
#
#         await bot.send_message(chat_id=chat_id, text=message, parse_mode=ParseMode.HTML)
#
# if __name__ == "__main__":
#     asyncio.run(main())
