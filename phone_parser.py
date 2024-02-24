import aiohttp
import asyncio
import re

async def fetch_page(session, url):
    async with session.get(url) as response:
        return await response.text()

async def extract_phone_numbers(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_page(session, url) for url in urls]
        pages = await asyncio.gather(*tasks)

        phone_numbers = []
        for page_content in pages:
            # Looking for phone numbers using regular expression
            numbers = re.findall(r'\b(?:\+?(\b7))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})\b', page_content)
            for number_parts in numbers:
                formatted_number = '+{} ({}) {} {}'.format(number_parts[0], number_parts[1], number_parts[2], number_parts[3])
            if len(formatted_number) == 17 and phone_numbers.__contains__(formatted_number) == False:
                phone_numbers.append(formatted_number)

            # Looking for phone numbers using another regular expression
            numbers = re.findall(r'\b8\s?\(\d{3}\)\s?\d{3}-\d{2}-\d{2}\b', page_content)
            for unic_number in numbers:
                if len(unic_number)!=0 and phone_numbers.__contains__(unic_number) == False:
                    phone_numbers.append(unic_number)
        return phone_numbers


if __name__ == "__main__":
    try:
        urls = ["https://hands.ru/company/about", "https://repetitors.info"]
        phone_numbers = asyncio.run(extract_phone_numbers(urls))
        print("Extracted Phone Numbers:", phone_numbers)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
