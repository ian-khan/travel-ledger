from travel_ledger.core.schema import COLUMNS

def build_create_table_stmt():
    columns = ",\n    ".join(f"{col.name} {col.sql_type}" for col in COLUMNS)
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
    col_names = [col.name for col in COLUMNS]
    insert_cols = []
    insert_vals = []
    for col, val in record.items():
        if col in col_names:
            insert_cols.append(col)
            insert_vals.append(val)

    cols = ", ".join(insert_cols)
    placeholders = ", ".join("?" for _ in insert_cols)

    stmt = f"INSERT INTO expenses ({cols}) VALUES ({placeholders})"
    return stmt, insert_vals

def build_update_stmt_params(id_: int, record_patch: dict):
    col_names = [col.name for col in COLUMNS]
    update_cols = []
    update_vals = []
    for col, val in record_patch.items():
        if col in col_names:
            update_cols.append(col)
            update_vals.append(val)

    set_clause = ", ".join(f"{col}=?" for col in update_cols)
    update_stmt = f"UPDATE expenses SET {set_clause} WHERE id=?"

    update_vals.append(id_)
    return update_stmt, update_vals

def build_delete_stmt_params(id_: int):
    delete_stmt = "DELETE FROM expenses WHERE id=?"
    params = (id_,)
    return delete_stmt, params

def build_select_one_stmt():
    stmt = f"SELECT * FROM expenses WHERE id=?"
    return stmt
