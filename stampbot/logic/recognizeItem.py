from typing import List
from logic.checkers.tokenCheck import token_check
from logic.checkers.stampCheck import waa_check
from logic.stamps_structures.tokenRecognize import Token
from logic.stamps_structures.stampRecognize import waa_recognize
import re


async def type_check(text: List [str], update, context):

    text_d = text.copy()

    if await waa_check(text):
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Распознано клеймо приемки военного имущества!")
        await waa_recognize(text, update, context)

    elif await token_check(text):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Распознан солдатский жетон (ЛОЗ)!")

        token = Token(text_d)
        await token.blood_check()
        await token.exception_check()
        await token.kompanie_check()
        await context.bot.send_message(chat_id=update.effective_chat.id, text=token.stamp)
        await token.extract_info()
        await token.responseGenerator()
        await context.bot.send_message(chat_id=update.effective_chat.id, text=token.response)

    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Тип клейма неопознан!")




