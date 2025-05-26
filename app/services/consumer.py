import asyncio
import json
import aio_pika
from telegram import Bot, Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.error import TelegramError

RABBITMQ_URL = "amqp://guest:guest@rabbitmq:5672/"
TELEGRAM_BOT_TOKEN = "7866422786:AAFRyIUIp734dKU3UEMG8e9R7ExvhLmcCMY"

chat_id_storage = set()

async def send_telegram_message(bot: Bot, chat_id: int, number: int, title: str, description: str):
    try:
        message = (
            f"Create new task:\n"
            f"<b>Task #{number}</b>\n"
            f"<b>Title:</b> {title}\n"
            f"<b>Description:</b> {description}"
        )
        await bot.send_message(chat_id=chat_id, text=message, parse_mode=ParseMode.HTML)
    except TelegramError as e:
        print(f"Error sending message to Telegram: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    chat_id_storage.add(chat_id)
    await update.message.reply_text("✅ Бот активирован! Теперь вы будете получать уведомления.")

async def consume_rabbitmq(bot: Bot):
    while True:
        try:
            connection = await aio_pika.connect_robust(RABBITMQ_URL)
            async with connection:
                channel = await connection.channel()
                queue = await channel.declare_queue("telegram_notifications", durable=True)

                async with queue.iterator() as queue_iter:
                    async for message in queue_iter:
                        async with message.process():
                            try:
                                body = json.loads(message.body.decode())
                                number = body.get("number")
                                title = body.get("title")
                                description = body.get("description")
                                target_chat_id = body.get("chat_id")

                                if target_chat_id:
                                    await send_telegram_message(bot, target_chat_id, number, title, description)
                                else:
                                    for chat_id in chat_id_storage:
                                        await send_telegram_message(bot, chat_id, number, title, description)

                            except Exception as e:
                                print(f"Error processing message: {e}")

        except Exception as e:
            print(f"Error connecting to RabbitMQ: {e}")
            await asyncio.sleep(5)

async def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))

    await application.initialize()
    await application.start()
    print("Бот запущен!")

    rabbitmq_task = asyncio.create_task(consume_rabbitmq(application.bot))

    await application.updater.start_polling()
    await rabbitmq_task

if __name__ == "__main__":
    asyncio.run(main())
