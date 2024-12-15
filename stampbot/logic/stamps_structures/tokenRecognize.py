import copy
from typing import List
import psycopg2
import Levenshtein
from config import ORDER, BLOOD
from logic.utils.morphology_refactor import determine_gender, to_genitive_case


class Attribute:

    def __init__(self, key: str):

        self.key = key
        self.describs = []
        self.number = None
        self.name = None
class Token:

    def __init__(self, stamp: List [str]):

        self.stamp = stamp #Исходник
        self.dstamp = stamp.copy() #Резерв исходника

        self.number = None #ID солдата
        self.blood = None #группа крови (на рукаве)

        self.info = []
        self.response = ""

    def __copy__(self):

        new_instance = Token(self.stamp.copy())
        new_instance.number = self.number
        new_instance.blood = self.blood
        new_instance.info = copy.deepcopy(self.info)
        return new_instance

    async def responseGenerator(self):
        sorted_attributes = sorted(self.info, key=lambda x: ORDER.get(x.key, float('inf')))

        response = f"Жетон {self.number}-го номера" if self.number is not None else "Жетон"
        response_parts = []

        for attribute in sorted_attributes:
            if not attribute.key:
                continue

            gender = await determine_gender(attribute.key)
            describs_text = ' '.join(attribute.describs) if attribute.describs else ""

            if attribute.number is not None:
                response_text = f"{attribute.number} " + await to_genitive_case(
                    f"{describs_text} {attribute.key}".strip(), gender)
            else:
                response_text = await to_genitive_case(f"{describs_text} {attribute.key}".strip(), gender)

            if attribute.name is not None:
                response_text += f" {attribute.name}"

            response_parts.append(response_text)

        if self.blood is not None:
            response_parts.append(self.blood)
        self.response = response + " " + " ".join(response_parts).strip()

    async def extract_info(self):

        current = None
        current_number = None

        for i in range(len(self.stamp) - 1, -1, -1):

            element = self.stamp[i]

            if element.isdigit():
                if self.stamp[i-1].isdigit() or i == -1:
                    self.number = element
                else:
                    current_number = element
                continue

            row = await db_extractor(str(element), None)

            if row:

                code = row[0] if row[0] else None
                text = row[1] if row[1] else None
                type = row[2] if row[2] is not None else False

                if type:
                    if current is not None:
                        current.number = current_number
                        self.info.append(current)
                    current = Attribute(text)
                else:
                    if code is not None and text is not None:
                        if current is None:
                            continue
                        else: current.describs.append(text)
        if current is not None:
            current.number = current_number
            self.info.append(current)
        current_number = None

    async def blood_check(self):

        for i in range(0, len(self.stamp)-1):
            if self.stamp[i] in BLOOD:
                if self.stamp[i] == "O":
                    self.blood = "(1 группа крови)"
                    self.stamp.pop(i)
                    self.dstamp = self.stamp.copy()
                    break
                elif self.stamp[i] == "A":
                    self.blood = "(2 группа крови)"
                    self.stamp.pop(i)
                    self.dstamp = self.stamp.copy()
                    break
                elif self.stamp[i] == "B":
                    self.blood = "(3 группа крови)"
                    self.stamp.pop(i)
                    self.dstamp = self.stamp.copy()
                    break
                elif self.stamp[i] == "AB":
                    self.blood = "(4 группа крови)"
                    self.stamp.pop(i)
                    self.dstamp = self.stamp.copy()
                    break


    async def kompanie_check(self):

        for i in range(0, len(self.stamp)-2):
            if self.stamp[i] == "Kp" or self.stamp[i] == "Komp":
                if self.stamp[i-1].isdigit():

                    current = Attribute("рота")
                    current.number = self.stamp[i-1]

                    self.info.append(current)
                    self.stamp.pop(i)
                    self.stamp.pop(i-1)

    async def exception_check(self):

        table = "Exception"
        counter = 0

        for stamp in self.stamp:
            if stamp.isdigit():
                continue

            row = await db_extractor(str(stamp), None)

            if row:
                text = row[1] if row[1] else None
                type = row[2] if row[2] is not None else False

                if type:
                    key_object = stamp
                    current_text = ""
                    ex_text = ""
                    name = ""

                    i = self.stamp.index(key_object)

                    for j in range(i + 1, len(self.stamp)):

                        ex_text += self.stamp[j]
                        row1 = await db_extractor(str(ex_text), table)
                        if row1:
                            if row1[0] == ex_text:
                                current_text = row1[1]
                                name = row1[3]
                                self.stamp.pop(j)
                            elif row1[0] != ex_text or j-(i + 1) >= 3:
                                break
                            else:
                                break
                        else:
                            break

                    if len(current_text) < 1:
                        continue
                    else:
                        self.stamp.pop(i)
                        current = Attribute(text)
                        current.describs.append(current_text)
                        current.name = name
                        self.info.append(current)
                        counter += 1
        if counter == 0:
            self.stamp = self.dstamp


async def db_extractor(code: str, name: str):

    connection = psycopg2.connect(
        dbname='ww2_tokens',
        user='postgres',
        password='123456',
        host='localhost',
        port='8086',
        options='-c client_encoding=utf8'
    )

    cursor = connection.cursor()

    if name is None:
        name = str(code[0].upper())

    query = f'SELECT * FROM "{name}";'

    cursor.execute(query, (code,))
    try:
        cursor.execute(query)

        results = cursor.fetchall()
        if not results:
            print(f"No results found for code: {code}")
            return None

        min_distance = 1000
        closest_record = None

        for record in results:
            current_distance = Levenshtein.distance(record[0], code)
            if current_distance < min_distance:
                min_distance = current_distance
                closest_record = record
        return closest_record

    except psycopg2.Error as e:
        print(f"Database error: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    finally:
        cursor.close()
        connection.close()





