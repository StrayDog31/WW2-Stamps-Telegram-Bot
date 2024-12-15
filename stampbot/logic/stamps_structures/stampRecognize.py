from typing import List
import re
import psycopg2
async def extract_code(text):

    combined_text = ''.join(text).lower()
    match = re.search(r'\d+', combined_text)
    index = match.start()
    return combined_text[index:]
async def waa_recognize(text: List[str], update, context):

    code = await extract_code(text)

    try:
        connection = psycopg2.connect(
            dbname='ww2_stamps',
            user='postgres',
            password='123456',
            host='localhost',
            port='8086',
            options='-c client_encoding=utf8'
        )
        cursor = connection.cursor()

        query = '''
        SELECT 
            L."id_location" AS id_location,
            L."Location" AS Location, 
            C."id_country" AS id_country, 
            C."Country" AS Country, 
            H."Manufacturer" AS Manufacturer, 
            H."Period" AS Period
        FROM 
            public."Stamp" H
        JOIN 
            public."Location" L ON H."id_location" = L."id_location"
        JOIN 
            public."Country" C ON L."id_country" = C."id_country"
        WHERE 
            H."Code" = %s;  -- Код должен быть строкой
        '''

        cursor.execute(query, (code,))

        row = cursor.fetchone()
        print(row)

        if row:
            id_location = row[0] if row[0] is not None else "Не указано"
            Location = row[1] if row[1] is not None else "Не указано"
            id_country = row[2] if row[2] is not None else "Не указано"
            Country = row[3] if row[3] is not None else "Не указано"
            Manufacturer = row[4] if row[4] is not None else "Не указано"
            Period = row[5] if row[5] is not None else "Не указан"

            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=f"Расположение: г. {Location}  ({Country}), \nПроизводитель: {Manufacturer}, \nПериод: {Period} г.")
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="Клеймо не найдено.")

    except Exception as error:
        print(f"Ошибка при работе с PostgreSQL: {error}")

    except Exception as error:
        print(f"Ошибка при работе с PostgreSQL: {error}")
