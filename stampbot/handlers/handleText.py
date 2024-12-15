import re
from PIL import Image
from config import MAX_TEXT_LENGTH, Delimiters
from logic.textManager import text_manager

async def text_length_check(text: str) -> bool:
    return len(text) <= MAX_TEXT_LENGTH
async def text_handle(update, context):

    text = update.message.text

    if not await text_length_check(text):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Введен слишком длинный текст!")
        return

    pattern = r'[' + re.escape(''.join(Delimiters)) + r']+'
    text = re.sub(pattern, '|', text)
    text = text.split("|")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    try:
        await text_manager(text, update, context)

    except (Image.UnidentifiedImageError, OSError) as e:

        await context.bot.send_message(chat_id=update.effective_chat.id, text="Что-то пошло не так. Отправьте клеймо еще раз!".format(str(e)))