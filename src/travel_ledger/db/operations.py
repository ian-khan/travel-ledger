import sqlite3
from travel_ledger.db.statements import (build_create_table_stmt, build_insert_stmt_params,
                                         build_update_stmt_params, build_select_one_stmt)


def create_table(db_name: str):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute(build_create_table_stmt())
    con.commit()
    con.close()

def insert_record(db_path: str, record: dict):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cmd, params = build_insert_stmt_params(record)
    cur.execute(cmd, params)
    con.commit()
    con.close()

def update_record(db_path: str, id_:int, **kwargs):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cmd, params = build_update_stmt_params(**kwargs)
    params.append(id_)
    cur.execute(cmd, params)
    con.commit()
    con.close()

def fetch_record_with_id(db_path: str, id_:int):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute(build_select_one_stmt(), (id_,))
    row = cur.fetchone()
    con.close()
    return row