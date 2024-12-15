import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from config import TOKEN
from handlers.handleImage import image_handle
from handlers.handleInfo import info
from handlers.handleText import text_handle

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

if __name__ == '__main__':

    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', info)
    help_handler = CommandHandler('help', info)
    image_handler = CommandHandler('image', image_handle)
    text_handler = CommandHandler('text', text_handle)

    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(MessageHandler(filters.PHOTO, image_handle))
    application.add_handler(MessageHandler(filters.TEXT, text_handle))

    application.run_polling()