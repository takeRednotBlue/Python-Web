"""
Основна обов'язкова частина

Публічне АПІ ПриватБанка дозволяє отримати інформацію про готівкові курси валют ПриватБанку та НБУ на обрану дату. Архів зберігає дані за останні 
4 роки.

Напишіть консольну утиліту, яка повертає курс EUR та USD ПриватБанку протягом останніх кількох днів. Встановіть обмеження, що в утиліті можна 
дізнатися курс валют не більше, ніж за останні 10 днів. Для запиту до АПІ використовуйте Aiohttp client. Дотримуйтесь принципів SOLID під час 
написання завдання. Обробляйте коректно помилки при мережевих запитах.


Додаткова частина

    додайте можливість вибору, через передані параметри консольної утиліти, додаткових валют у відповіді програми
    візьміть чат на веб-сокетах з лекційного матеріалу та додайте до нього можливість введення команди exchange. Вона показує користувачам 
    поточний курс валют у текстовому форматі. Формат представлення виберіть на власний розсуд
    розширте додану команду exchange, щоб була можливість переглянути курс валют в чаті за останні кілька днів. Приклад exchange 2
    за допомогою пакетів aiofile та aiopath додайте логування до файлу, коли була виконана команда exchange у чаті

    https://api.privatbank.ua/p24api/exchange_rates?date=01.12.2014 
"""


from pprint import pprint
import platform 

import aiohttp
import asyncio

def privat_ccy_api_by_date(date): 
    return f'https://api.privatbank.ua/p24api/exchange_rates?date={date}'

async def main():

    async with aiohttp.ClientSession() as session:
        async with session.get(privat_ccy_api_by_date('01.12.2022')) as response:
            print('Status: ', response.status)
            print('Content-type: ', response.headers['content-type'])
            print('Cookies: ', response.cookies)
            print(response.ok)
            result = await response.json()
            exchange = list(filter(lambda x: x['currency'] in ['USD', 'EUR'], result['exchangeRate']))
            return exchange



if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    r = asyncio.run(main())
    pprint(r)