'''
--- HELP ---

create|list|update|remove - вибирається дія яку потрібно виконати
--model|-m <Molel's name> - визначаємо над якою моделлю потрібно виконати дію
--id <int> - id запису над яким потрібно здійснити дію
--column|-c <column name>[...] - назва колонки або колонок для операцій створення та зміни (колонки можна прописувати підряд)
--value|-v <value>[...] - одне або декілька значень які потрібно помістити у колонку (значення можна прописувати підряд для декількох колонок)


--- EXAMPLES ---

CREATE
python3 main.py -a create -m Tutor -c fullname group_id -v 'Maxym Klym' 3
python3 main.py -a create -m student -c fullname group_id -v 'Voymyr Zelenskiy' 3

LIST
python3 main.py -a list -m Grade

UPDATE
python3 main.py -a update -m Student --id 2 -c group_id -v 2
python3 main.py -a update -m grade -i 5 -c student_id grade -v 22 2

REMOVE
python3 main.py -a remove -m Tutor --id 3

'''

from src.connect_db import session
from cli_interface.command_handlers import *
from cli_interface.command_parser import parser


ACTIONS_MAPPING = {
    'create': create_handler,
    'update': update_handler,
    'remove': remove_handler,
    'list': list_handler
}
    

def main():
    args = parser.parse_args()
    handler = ACTIONS_MAPPING[args.subcommand]
    result = handler(args, session)
    try:
        print(result) if result is not None else None
    except Exception as err:
        print(err)


if __name__ == '__main__':
    main()
    
