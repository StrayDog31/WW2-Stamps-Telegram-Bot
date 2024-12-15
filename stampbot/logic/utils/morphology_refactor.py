import pymorphy3

morph = pymorphy3.MorphAnalyzer()

async def determine_gender(word):

    parsed_word = morph.parse(word)

    if parsed_word:

        first_form = parsed_word[0]

        if 'masc' in first_form.tag:
            return 'мужской'
        elif 'femn' in first_form.tag:
            return 'женский'
        elif 'neut' in first_form.tag:
            return 'средний'
        else:
            return 'неопределенный'
    else:
        return 'неизвестно'

async def to_genitive_case(text, gender):
    words = text.split()
    transformed_words = []

    for word in words:

        parsed_word = morph.parse(word)[0]
        word_genitive = None

        if gender:

            if gender == 'мужской':
                word_genitive = parsed_word.inflect({'gent', 'masc'})
            elif gender == 'женский':
                word_genitive = parsed_word.inflect({'gent', 'femn'})
            elif gender == 'средний':
                word_genitive = parsed_word.inflect({'gent', 'neut'})
        else:
            word_genitive = parsed_word.inflect({'gent'})

        if word_genitive:
            transformed_words.append(word_genitive.word)
        else:
            transformed_words.append(word)

    return ' '.join(transformed_words)

