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
import asyncio
import argparse
import logging
from datetime import datetime, timedelta

import aiohttp


AVAILABLE_CURRENCIES = ["USD", "EUR", "CHF", "GBP", "PLZ", "SEK", "XAU", "CAD",]
DEFAULT_CURRENCIES = ["USD", "EUR"]
DAYS_LIMIT = list(range(1, 11))  # 10 days

parser = argparse.ArgumentParser(description="PB currency archive")

parser.add_argument('-d', '--days', type=int, default=1, required=False, choices=DAYS_LIMIT)
parser.add_argument('-c', '--currency', default=None, required=False, type=str, choices=AVAILABLE_CURRENCIES)


def privat_ccy_api_by_date(date): 
    return f'https://api.privatbank.ua/p24api/exchange_rates?date={date}'


async def get_exchange_by_date(session, date):
    async with session.get(privat_ccy_api_by_date(date)) as response:
        print(f'Start waiting for date: {date}')
        try:
            if response.status == 200:
                response_result = await response.json()
                print(f'Finished waiting for date: {date}')
                return response_result
            logging.error(f"Error status: {response.status} for {response.url}")
            return None
        except aiohttp.ClientConnectorError as err:
            logging.error(f"Connection error: {str(err)}")


async def get_exchange(days):
    start_date = datetime.now()
    list_of_dates = [(start_date - timedelta(num)) for num in range(1, days+1)]
    list_of_date_strings = list(map(lambda x: x.strftime('%d.%m.%Y'), list_of_dates))
    async with aiohttp.ClientSession() as session:
        coroutines = []
        for date in list_of_date_strings:
            task = asyncio.create_task(get_exchange_by_date(session, date))
            coroutines.append(task)
        exchange_rates_by_dates = await asyncio.gather(*coroutines)
    return exchange_rates_by_dates


def main():
    args = parser.parse_args()
    exchange_archive = asyncio.run(get_exchange(args.days))
    currency = args.currency
    for day in exchange_archive:
        rates = day.get('exchangeRate')
        if currency:
            exchange = list(filter(lambda x: x['currency'] == currency, rates))
        else:
            exchange = list(filter(lambda x: x['currency'] in DEFAULT_CURRENCIES, rates))

        for rate_obj in exchange:
            print(f"""
            \rDate: {day['date']}
            \rcurrency: {rate_obj['currency']}:
            \rbuy: {rate_obj['purchaseRateNB']}, 
            \rsale: {rate_obj['saleRateNB']}.""")


if __name__ == '__main__':
    start_time = datetime.now()
    main()
    end_time = datetime.now() - start_time
    print(f'Finished in {end_time.seconds} seconds.')

