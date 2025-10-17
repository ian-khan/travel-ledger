import sqlite3
from travel_ledger.utils import get_create_table_cmd, get_insert_cmd_params

def init_db(db_name: str):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute(get_create_table_cmd())
    con.commit()
    con.close()

def add_expense(db_path: str, **kwargs):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cmd, params = get_insert_cmd_params(**kwargs)
    cur.execute(cmd, params)
    con.commit()
    con.close()