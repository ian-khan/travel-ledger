import sqlite3
from travel_ledger.db.statements import (build_create_table_stmt, build_insert_stmt_params,
                                         build_update_stmt_params, build_select_one_stmt)
from contextlib import closing
from typing import Any, Optional, Sequence

def execute(db_path: str,
            stmt: str,
            params: Sequence[Any]=(),
            fetch: Optional[str]=None):
    """
    Open connection, execute a statement with optional parameters, and return the fetched result.
    :param db_path: path to database
    :param stmt: SQL statement to execute
    :param params: parameters to pass to statement
    :param fetch: None, 'one', or 'all'
    :return: fetched result
    """
    if fetch not in (None, 'one', 'all'):
        raise ValueError("fetch must be None, 'one', or 'all'")
    # Automatically close connection
    with closing(sqlite3.connect(db_path)) as con:
        # Automatically commit or roll back transaction
        with con:
            cur = con.cursor()
            cur.execute(stmt, params)
            fetched = None
            if fetch in ('one', 'all'):
                fetched = getattr(cur, f'fetch{fetch}')()
    return fetched

def create_table(db_path: str):
    stmt = build_create_table_stmt()
    execute(db_path, stmt)

def insert_record(db_path: str, record: dict):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cmd, params = build_insert_stmt_params(record)
    cur.execute(cmd, params)
    con.commit()
    con.close()

def update_record(db_path: str, id_:int, record_patch):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cmd, params = build_update_stmt_params(record_patch)
    params.append(id_)
    cur.execute(cmd, params)
    con.commit()
    con.close()

def fetch_record_with_id(db_path: str, id_:int):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute(build_select_one_stmt(), (id_,))
    record = cur.fetchone()
    con.close()
    return record