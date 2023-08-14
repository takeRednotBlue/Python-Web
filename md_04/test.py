import requests
from pprint import pprint


r = requests.get('https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11')
exchange_rate = r.json()
pprint(exchange_rate)