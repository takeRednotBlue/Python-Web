from pprint import pprint
import platform 

import aiohttp
import asyncio

privat_ccy_api = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'

async def main():

    async with aiohttp.ClientSession() as session:
        async with session.get(privat_ccy_api) as response:
            print('Status: ', response.status)
            print('Content-type: ', response.headers['content-type'])
            print('Cookies: ', response.cookies)
            print(response.ok)
            result = await response.json()
            return result



if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    r = asyncio.run(main())
    pprint(r)