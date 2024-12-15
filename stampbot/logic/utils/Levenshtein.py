

async def levenshtein_distance(text1, text2):

    len1 = len(text1)
    len2 = len(text2)

    if len1 < len1:
        return levenshtein_distance(text2, text1)
    if len2 == 0:
        return len1

    current_row = range(len1 + 1)
    for i in range(1, len2 + 1):
        previous_row, current_row = current_row, [i] + [0] * len2
        for j in range(1, len1 + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if text1[j - 1] != text2[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[len1]