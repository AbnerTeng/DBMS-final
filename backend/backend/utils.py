"""
Useful utilities for querying
"""
from typing import List, Tuple, Union

def clean_fetched_data(data: List[Tuple[str,]]) -> List[str]:
    """
    clean output
    """
    for idx, val in enumerate(data):
        data[idx] = val[0]
    return data

def tup2list(data: List[Tuple[int, str]]) -> List[List[Union[int, str]]]:
    """
    Convert tuple to list
    """
    for idx, val in enumerate(data):
        data[idx] = list(val)
    return data

def execute_sql_file(cursor, filename):
    """
    Execute a SQL script from a file
    """
    with open(filename, 'r', encoding="utf-8") as sql_file:
        sql_script = sql_file.read()
    cursor.executescript(sql_script)
