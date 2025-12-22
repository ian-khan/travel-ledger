import sqlite3
import pandas as pd
import os.path as osp
from .statements import build_select_all_stmt

def export_to_excel(db_path: str, out_path: str = None):
    """Export all expense records to an Excel file."""
    con = sqlite3.connect(db_path)
    stmt = build_select_all_stmt()
    df = pd.read_sql_query(stmt, con)
    con.close()

    if df.empty:
        print("No records found in the database. Nothing to export.")
        return

    if out_path is None:
        base = osp.splitext(db_path)[0]
        out_path = base + ".xlsx"

    df.to_excel(out_path, index=False)
    print(f"Exported {len(df)} records to {out_path}")
