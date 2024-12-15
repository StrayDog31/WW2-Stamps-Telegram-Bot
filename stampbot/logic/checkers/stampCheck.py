from typing import List
async def waa_check(text: List [str]):
    abbreviation = "waa"
    correct = 0
    index = 0

    for s in text:
        if s.isdigit(): break
        else:
            for char in s:
                if char.lower() == abbreviation[index]:
                    correct += 1
                index += 1
            if index == 3:
                if correct >= 2: return True
                else: return False

    if index == 3:
        if correct >= 2:
            return True
        else:
            return False
    return False
