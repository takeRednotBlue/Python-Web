import argparse
import re

from datetime import datetime
from typing import Any


DATE_FORMAT_MAPPING = {
        r'\d{2}\.\d{2}\.\d{4}': '%d.%m.%Y',
        r'\d{2}/\d{2}/\d{4}': '%d/%m/%Y',
        r'\d{2}\.\d{2}\.\d{2}': '%d.%m.%y',
        r'\d{2}/\d{2}/\d{2}': '%d/%m/%y',
        r'\d{4}-\d{2}-\d{2}': '%Y-%m-%d',
}

def is_float(string: str) -> bool:
    '''Checks wether string contains float number'''
    try:
        float(string)
        return True
    except:
        return False


def valid_date_format(date: str) -> bool:
    '''
    Available formats: '12.03.2023', '12/03/2023', '12.03.23', '12/03/23', '2023-03-12'
    '''
    for pattern in DATE_FORMAT_MAPPING:
        if re.match(pattern, date):
            return True
    else:
         return False


def get_date_format(date: str) -> str:
    '''Returns valid patter for converting to datetime object'''
    for pattern, format in DATE_FORMAT_MAPPING.items():
        if re.match(pattern, date):
            return format
    else:
        raise ValueError('Invalid date format.')


def set_type(string: str) -> Any:
    '''Converts string to an appropriate type'''
    if string.isdigit():
        return int(string)
    elif is_float(string):
        return float(string)
    elif valid_date_format(string):
        date_format = get_date_format(string)
        try:
            date = datetime.strptime(string, date_format).date()
            return date
        except:
            return str(string) 
    elif string.lower() == 'none':
        return None
    else:
        return string
    

parser = argparse.ArgumentParser(prog='University DB CLI interface', 
                                 epilog='"Any fool can know. The point is to understand." - Albert Einstein')

# parser.add_argument('-a', '--actions', action='store_true', required=True)
subparsers = parser.add_subparsers(dest='subcommand', title='CRUD operations')

create_parser = subparsers.add_parser('create', help='add new record to the table')
create_parser.add_argument('-m', '--model', help='specify table model', type=str, required=True)
create_parser.add_argument('-c', '--column', help='specify table column or columns', type=str, nargs='+', required=True)
create_parser.add_argument('-v', '--value', help='specify value or values to add', type=set_type, nargs='+', required=True)

list_parser = subparsers.add_parser('list', help='display table or record data')
list_parser.add_argument('-m', '--model', help='specify table model', type=str, required=True)
list_parser.add_argument('-c', '--column', help='specify table column or columns', type=str, nargs='+')
list_parser.add_argument('-i', '--id', help='specify record id', type=int)

update_parser = subparsers.add_parser('update', help='change record values')
update_parser.add_argument('-m', '--model', help='specify table model', type=str, required=True)
update_parser.add_argument('-i', '--id', help='specify record id', type=int, required=True)
update_parser.add_argument('-c', '--column', help='specify table column or columns', type=str, nargs='+', required=True)
update_parser.add_argument('-v', '--value', help='specify updated value or values', type=set_type, nargs='+', required=True)

remove_parser = subparsers.add_parser('remove', help='remove record from table')
remove_parser.add_argument('-m', '--model', help='specify table model', type=str, required=True)
remove_parser.add_argument('-i', '--id', help='specify record id', type=int, required=True)




if __name__ == '__main__':
    while True:
        value = input('Enter your value: ')
        if value == 'exit':
            break
        print(f'Value {set_type(value)} type is {type(set_type(value))}')




