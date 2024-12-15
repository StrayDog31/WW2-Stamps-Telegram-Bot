from easyocr import easyocr
from PIL import Image
import re
import numpy as np
from config import Delimiters
from logic.textManager import text_manager


def split_text(input_text):
    pattern = r'[' + re.escape(''.join(Delimiters)) + r']+|/'
    transformed_text = re.sub(pattern, lambda m: '|' + m.group() + '|' if m.group() == '/' else '|', input_text)
    transformed_text = re.sub(r'\|{2,}', '|', transformed_text)
    return transformed_text.strip('|')

async def find_common_substring(text1: str, text2: str) -> str:
    m, n = len(text1), len(text2)
    longest = 0
    end_index = 0
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                if dp[i][j] > longest:
                    longest = dp[i][j]
                    end_index = i
            else:
                dp[i][j] = 0

    if longest < len(text1)/2 - 2:
        return text1

    return text1[end_index - longest:end_index]

async def remove_rotated(image: Image.Image):

    reader = easyocr.Reader(['en'])

    result1 = reader.readtext(image, paragraph=True)
    text1 = ' '.join([res[1] for res in result1])

    rotated_image = image.rotate(180, expand=True)

    result2 = reader.readtext(np.array(rotated_image), paragraph=True)
    text2 = ' '.join([res[1] for res in result2])

    text1 = split_text(text1)
    text2 = split_text(text2)

    text = await find_common_substring(text1, text2)

    if text[len(text)-1] == "|":
        text = text[:-1]

    return text.split("|")

async def image_manager(image: Image.Image, update, context):

    try:
        reader = easyocr.Reader(['en'])
        result = reader.readtext(image)
        text = ' '.join([res[1] for res in result])

        if text.strip():

            text = await remove_rotated(image)

            await text_manager(text, update, context)

        else:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="Текст не найден в изображении. Сделайте фото еще раз!")

    except (Image.UnidentifiedImageError, OSError) as e:

        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Ошибка в распознании текста!".format(str(e)))




