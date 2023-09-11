'''
Порядок виконання

    Створіть хмарну базу даних Atlas MongoDB
    За допомогою ODM Mongoengine створіть моделі для зберігання даних із цих файлів у колекціях authors та quotes.
    Під час зберігання цитат (quotes) поле автора в документі повинно бути не рядковим значенням, а Reference fields полем, де зберігається ObjectID з колекції authors.
    Напишіть скрипти для завантаження json файлів у хмарну базу даних.
    Реалізуйте скрипт для пошуку цитат за тегом, за ім'ям автора або набором тегів. Скрипт виконується в нескінченному циклі і за допомогою звичайного оператора input приймає команди у наступному форматі - команда: значення. Приклад:

    name: Steve Martin — знайти та повернути список всіх цитат автора Steve Martin;
        tag: life — знайти та повернути список цитат для тегу life;
        tags: life live — знайти та повернути список цитат, де є теги life або live (примітка: без пробілів між тегами life, live);
        exit — завершити виконання скрипту;

    Виведення результатів пошуку лише у форматі utf-8;

Додаткове завдання

    Подумайте та реалізуйте для команд name:Steve Martin та tag:life можливість скороченого запису значень для пошуку, як name:st та tag:li відповідно;
    Виконайте кешування результату виконання команд name: та tag: за допомогою Redis, щоб при повторному запиті результат пошуку брався не з MongoDB бази даних, а з кешу;

Підказка

Для команд name:st та tag:li використовуйте регулярні вирази в String queries
'''

from typing import Any
from bson import ObjectId
import json

import redis
from mongoengine import QuerySet
from redis_lru import RedisLRU

from connection import connect
from models.models import  Authors, Quotes

# caching with redis
client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


def parse_args(input: str) -> dict[str, str]|None:
    '''Parse the command line arguments
    :param input: input string
    :return: dictionary which contains command and arguments key:value pair
    In order to be able to cache further functions results parsed arguments don't
    have to be split into list'''
    if not input:
        print('Please enter a query command or exit to end program')        
        return None
    if input.count(':') != 1:
        print("Command string from arguments must be devided by colon ':' and there should be only one.")        
        return None
    
    parsed_input = input.split(':')
    command = parsed_input[0]
    arguments = parsed_input[1].strip()
    return {'command': command, 'arguments': arguments}


def print_quote(quotes: QuerySet|Any) -> None:
    for quote in quotes:
        author_name = quote.author.fullname
        print(f'''
            \rAuthor: {author_name}
            \rQuote: {quote.quote}
            \rTags: {', '.join(quote.tags)}\n'''
        )


@cache
def name_commad_handler(name: str) -> QuerySet|None:
    '''
    Handler for name command
    :param aguments: list of arguments
    :return: mangoengine Document class :meth objects: result
    '''
    author = Authors.objects(fullname__istartswith=name).first()
    if not author:
        return None
    author_id: ObjectId = author.id
    quotes = Quotes.objects(author=author_id).all()
    return quotes


@cache
def tag_commad_handler(tag: str) -> QuerySet:
    '''
    Handler for tag command
    :param tag: tag name
    :return: mangoengine Document class :meth objects: result
    '''
    quotes = Quotes.objects(tags__istartswith=tag).all()
    return quotes


@cache()
def tags_commad_handler(tags_str: str) -> QuerySet:
    '''
    Handler for tags command
    :param aguments: list of arguments
    :return: mangoengine Document class :meth objects: result
    '''
    tags: list[str] = tags_str.split()
    quotes = Quotes.objects(tags__in=tags)
    return quotes


def main():
    while True:
        user_input = input('Enter query command >>> ')
        if user_input.startswith('exit'):
            break
        if not user_input:
            print('Please enter a query command or exit to end program')
            continue

        args_dict = parse_args(user_input)
        if not args_dict:
            continue
        command: str = args_dict['command']
        args: str = args_dict['arguments']
        
        match command:
            case 'name':
                name = args
                quotes = name_commad_handler(name)
            case 'tag':
                tag = args
                quotes = tag_commad_handler(tag)
            case 'tags':
                tags_str = args
                quotes = tags_commad_handler(tags_str)
            case _:
                print(f'Unknown command: {command}')
                continue

        if quotes:
            print_quote(quotes)
        else:
            print(f"No quotes found for command: '{command}' with argument(s): '{args}'.")
      
            
if __name__ == '__main__':
    main()