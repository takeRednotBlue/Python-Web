import argparse

import uuid
import datetime
import decimal


import sqlalchemy.sql.sqltypes as types
from sqlalchemy import select, update, delete, Row, Column
from sqlalchemy.orm import Session, DeclarativeBase
from tabulate import tabulate
from typing import Sequence, Tuple, Any

from src.models import Student, Tutor, Grade, Subject, Group

# Custom typing for value that is returned by sqlalchemy.Result.all()
MySelectResult = Sequence[Row[Tuple[str, Any]]]

MODELS_LIST = [Student, Tutor, Grade, Subject, Group]

MODELS_MAPPING = {
    key:value for key, value in [(model.__name__, model) for model in MODELS_LIST]
}

SQLALCHEMY_TYPE_MAPPING = {
    bool: types.Boolean,
    bytes: types.LargeBinary,
    datetime.date: types.Date,
    datetime.datetime: types.DateTime,
    datetime.time: types.Time,
    datetime.timedelta: types.Interval,
    decimal.Decimal: types.Numeric,
    float: types.Float,
    int: types.Integer,
    str: types.String,
    uuid.UUID: types.Uuid,
}


def print_table(result: MySelectResult) -> None:
    '''Takes result from select_xx() function as argument and print it
      in table format.'''
    if not result:
        print('No data found.')
        return
    
    headers = list(result[0]._mapping.keys())
    # Pretty prints when single value is returned
    if len(result) == 1 and len(result[0]) == 1:
        print(f'{headers[0]} - {str(result[0][0])}')
        return
    else:
        data = []
        for row in result:
            data.append(list(row))
    
        table = tabulate(data, headers, tablefmt='psql')
        print(table)


def is_valid_column_type(
        model: DeclarativeBase, 
        columns: list[str], 
        values: list[Any]
) -> tuple[bool, str|None]:
    
    '''Check wether values types match columns types'''
    columns_list: list[Column] = [column for column in model.__table__.columns]
    columns_name_mapping: dict[(str, Column)] = {column.key: column for  column in columns_list}
        
    for index, value in enumerate(values):
        column_name = columns[index]
        column_type = columns_name_mapping[column_name].type
        required_type = SQLALCHEMY_TYPE_MAPPING[type(value)]
        if not isinstance(column_type, required_type):
            message = f"TypeError: '{value}' type doesn't match '{column_name}' column type - '{repr(column_type)}'."
            return False, message
    return True, None


def create_handler(
        args: argparse.Namespace,
        session: Session
) -> str:
    '''Handles addition of a new record to the existing database table.
    :param args: Namespace object that is returned when :meth parse_args: from argparse 
    library is called.'''

    # asign command line ars to variables
    model: DeclarativeBase = MODELS_MAPPING[args.model.lower().title()]
    columns: list[str] = args.column
    values: list[Any] = args.value

    if len(columns) != len(values):
        return "Columns amount doesn't match number of values."
    
    valid_column_type, error = is_valid_column_type(model, columns, values)
    if not valid_column_type:
        return error

    parameters_dict = dict(zip(columns, values))
    record = model(**parameters_dict)
    session.add(record)
    session.commit()
    return f"Record in table - '{model.__tablename__}' was successfully created."


def list_handler(
        args: argparse.Namespace,
        session: Session
) -> None:
    '''Output table data into terminal
    :param args: Namespace object that is returned when :meth parse_args: from argparse 
    library is called.'''

    # asign command line ars to variables
    model: DeclarativeBase = MODELS_MAPPING[args.model.lower().title()]

    stmt = select('*').select_from(model)
    result = session.execute(stmt).all()
    print_table(result)
    return None


def update_handler(
        args: argparse.Namespace,
        session: Session
) -> str:
    '''Update existing record with given id
    :param args: Namespace object that is returned when :meth parse_args: from argparse 
    library is called.'''

    # asign command line ars to variables
    model: DeclarativeBase = MODELS_MAPPING[args.model.lower().title()]
    id: int = args.id
    columns: list[str] = args.column
    values: list[Any] = args.value

    if len(columns) != len(values):
        return "Columns amount doesn't match number of values."
    
    valid_column_type, error = is_valid_column_type(model, columns, values)
    if not valid_column_type:
        return error

    column_value_dict = {column: value for column, value in zip(columns, values)}
    stmt = (
        update(model)
        .where(model.id == id)
        .values(**column_value_dict)
    )
    session.execute(stmt)
    session.commit()
    return f"Record with id - '{id}' from table - '{model.__tablename__}' was successfully updated."  


def remove_handler(
    args: argparse.Namespace,
    session: Session
) -> str:
    '''Remove record with given id
    :param args: Namespace object that is returned when :meth parse_args: from argparse 
    library is called.'''

    # asign command line ars to variables
    model: DeclarativeBase = MODELS_MAPPING[args.model.lower().title()]
    id: int = args.id

    stmt = (
        delete(model)
        .where(model.id == id)
    )
    session.execute(stmt)
    session.commit()
    return f"Record with id - '{id}' from table - '{model.__tablename__}' was successfully removed."

