from travel_ledger.config import COLUMNS

def build_create_table_stmt():
    columns = ",\n    ".join(f"{col} {type_}" for col, (type_, desc) in COLUMNS.items())
    create_table_cmd = f"CREATE TABLE IF NOT EXISTS expenses (\n    {columns}\n)"
    return create_table_cmd

def build_insert_stmt_params(record):
    """
    Build the INSERT statement and its parameters. Example:
    INSERT INTO table_name (column1, column2, column3, ...)
    VALUES (value1, value2, value3, ...);
    :param record:
    :return:
    """
    cols = []
    vals = []
    for col, val in record.items():
        if col in COLUMNS:
            cols.append(col)
            vals.append(val)

    col_names = ", ".join(cols)
    placeholders = ", ".join("?" for _ in cols)

    stmt = f"INSERT INTO expenses ({col_names}) VALUES ({placeholders})"
    return stmt, vals

def build_update_stmt_params(id_: int, record_patch: dict):
    cols = []
    vals = []
    for col, val in record_patch.items():
        if col in COLUMNS:
            cols.append(col)
            vals.append(val)

    set_clause = ", ".join(f"{col}=?" for col in cols)
    update_stmt = f"UPDATE expenses SET {set_clause} WHERE id=?"

    vals.append(id_)
    return update_stmt, vals

def build_select_one_stmt():
    stmt = f"SELECT * FROM expenses WHERE id=?"
    return stmt
