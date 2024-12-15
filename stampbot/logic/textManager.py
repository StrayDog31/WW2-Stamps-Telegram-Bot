
from logic.recognizeItem import type_check
async def remove_duplicates(text):
    seen = set()
    result = []

    for line in text:
        if line not in seen:
            seen.add(line)
            result.append(line)

    return result

async def modify_text(text):
    contains_slash = '/' in text
    contains_kp = 'Kp' in text

    if contains_slash and contains_kp:
        return [s for s in text if s != '/']
    elif contains_slash:
        return [s if s != '/' else 'Kp' for s in text]

    return text

async def refactor(text):

    text = await remove_duplicates(text)
    text = await modify_text(text)

    return text

async def text_manager(text, update, context):

    text = await refactor(text)

    await type_check(text, update, context)