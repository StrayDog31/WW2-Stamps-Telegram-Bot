from io import BytesIO
import requests
from PIL import Image
from config import MAX_IMAGE_WEIGHT
from logic.image_logic.imageManager import image_manager

async def check_image_weight(update):
    file_size = update.message.photo[-1].file_size
    return file_size <= MAX_IMAGE_WEIGHT

async def downloader(update, context):

    if not await check_image_weight(update):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Ошибка: изображение слишком велико! Максимальный размер — {(MAX_IMAGE_WEIGHT/1024)/1024} MB.")
        return

    file_data = await update.message.photo[-1].get_file()
    path_to_image = file_data.file_path

    response = requests.get(path_to_image)

    if response.status_code == 200:
        try:
            image = Image.open(BytesIO(response.content))
            image.load()

            await context.bot.send_message(chat_id=update.effective_chat.id, text="Изображение успешно получено!")

            return image

        except (Image.UnidentifiedImageError, OSError) as e:

            await context.bot.send_message(chat_id=update.effective_chat.id, text="Ошибка в получении изображения!".format(str(e)))
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,  text="Ошибка загрузки файла!".format(response.status_code))

async def image_handle(update, context):
    image = await downloader(update, context)

    if image is None:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Ошибка загрузки изображения.")
        return

    await image_manager(image, update, context)


