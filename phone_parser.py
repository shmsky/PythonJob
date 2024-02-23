import aiohttp
import asyncio
import re

async def fetch_page(session, url):
    async with session.get(url) as response:
        return await response.text()

async def extract_phone_numbers(url):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_page(session, url) for url in urls]
        pages = await asyncio.gather(*tasks)

        phone_numbers = []
        for page_content in pages:
            # Ищем номера телефонов с использованием регулярных выражений
            numbers = re.findall(r'\b(?:\+?(\b7))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})\b', page_content)
            for number_parts in numbers:
                formatted_number = '+{} ({}) {} {}'.format(number_parts[0], number_parts[1], number_parts[2], number_parts[3])
            if len(formatted_number) == 17 and phone_numbers.__contains__(formatted_number) == False:
                phone_numbers.append(formatted_number)

            numbers = re.findall(r'\b8\s?\(\d{3}\)\s?\d{3}-\d{2}-\d{2}\b', page_content)
            for unic_number in numbers:
                if len(unic_number)!=0 and phone_numbers.__contains__(unic_number) == False:
                    phone_numbers.append(unic_number)
        return phone_numbers

# Список URL-ов
urls = ["https://hands.ru/company/about", "https://repetitors.info"]

# Запускаем асинхронный код
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
phone_numbers = loop.run_until_complete(extract_phone_numbers(urls))

# Выводим найденные номера телефонов
print("Phone numbers found:")
for number in phone_numbers:
    print(number)
