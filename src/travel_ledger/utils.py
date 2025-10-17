from travel_ledger.config import COLUMNS

def get_create_table_cmd():
    columns = ",\n    ".join(f"{col} {type_}" for col, type_ in COLUMNS.items())
    create_table_cmd = f"CREATE TABLE IF NOT EXISTS expenses (\n    {columns}\n)"
    return create_table_cmd

def get_insert_cmd_params(**kwargs):
    cols = []
    vals = []
    kwargs.pop('id', None)
    for col, val in kwargs.items():
        if col in COLUMNS:
            cols.append(col)
            vals.append(val)

    col_names = ", ".join(cols)
    placeholders = ", ".join("?" for _ in cols)

    insert_cmd = f"INSERT INTO expenses ({col_names}) VALUES ({placeholders})"
    return insert_cmd, vals

