import sqlite3
from travel_ledger.utils import (get_create_table_cmd, get_insert_cmd_params,
                                 get_update_cmd_params, get_select_one_cmd)


def init_db(db_name: str):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute(get_create_table_cmd())
    con.commit()
    con.close()

def insert_expense(db_path: str, **kwargs):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cmd, params = get_insert_cmd_params(**kwargs)
    cur.execute(cmd, params)
    con.commit()
    con.close()

def fetch_expense_with_id(db_path: str, id_:int):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute(get_select_one_cmd(), (id_,))
    row = cur.fetchone()
    con.close()
    return row


def update_expense(db_path: str, id_:int, **kwargs):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cmd, params = get_update_cmd_params(**kwargs)
    params.append(id_)
    cur.execute(cmd, params)
    con.commit()
    con.close()