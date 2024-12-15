from typing import List

async def token_check(text: List [str]):

    print(len(text))

    if len(text) <= 3:
        return False
    else:
        return True