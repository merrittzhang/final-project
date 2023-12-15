import contextlib
import sqlite3


class DatabaseError(Exception):
    def __init__(self, string):
        self.error = string
    
    def __str__(self):
        return f"DatabaseError: {self.error}"


class InvalidTable(DatabaseError):
    def __init__(self, string):
        self.error = string
    
    def __str__(self):
        return f"InvalidTable: {self.error}"
    

class BadFields(DatabaseError):
    def __init__(self, string):
        self.error = string
    
    def __str__(self):
        return f"BadFields: {self.error}"


def get_connection(db_file):
    conn = sqlite3.connect(db_file)
    return conn


"""
Checks that a table exists within db_file.
"""
def check_table(db_file, table):
    tables = get_table_names(db_file)
    if table not in tables:
        raise InvalidTable(f"Table {table} does not exist in {db_file}")


"""
Checks that a row has all of the keys matching all of the columns of a table.
"""
def check_columns(db_file, table, row):
    columns = get_columns(db_file, table)
    keys = row.keys()
    if len(keys) != len(columns):
        raise DatabaseError(f"Row {row} does not have keys matching the columns of {table}")
    for col in columns:
        if col not in keys:
            raise DatabaseError(f"Row {row} does not have keys matching the columns of {table}")


"""
Returns the names of all tables in db_file.
"""
def get_table_names(db_file):
    with get_connection(db_file) as conn:
        with contextlib.closing(conn.cursor()) as cursor:
            sql_query = "SELECT name FROM sqlite_master WHERE type='table'"
            cursor.execute(sql_query)
            rows = cursor.fetchall()
            tables = [row[0] for row in rows]
            return tables
        

"""
Returns the names of all columns in table belonging to db_file.
"""
def get_columns(db_file, table):
    check_table(db_file, table)
    
    with get_connection(db_file) as conn:
        with contextlib.closing(conn.cursor()) as cursor:
            sql_query = f"SELECT * FROM {table}" 
            cursor.execute(sql_query)
            columns = [col[0] for col in cursor.description]
            return columns
        

"""
Returns all rows and all columns of table in db_file.
"""
def get_all(db_file, table):
    check_table(db_file, table)

    columns = get_columns(db_file, table)

    data = []

    with get_connection(db_file) as conn:
        with contextlib.closing(conn.cursor()) as cursor:
            sql_query = f"SELECT * FROM {table}"
            cursor.execute(sql_query)
            for row in cursor.fetchall():
                entry = {}
                for i, column in enumerate(columns):
                    entry[column] = row[i]
                data.append(entry)
            return data


"""
Updates a row in table from db_file.
Values is a dict with keys representing columns and values 
representing values to update.
Identifiers is a dict with keys representing columns and 
values representing which rows to select.
"""
def update(db_file, table, values, identifiers):
    check_table(db_file, table)

    set_clause = ", ".join([f"{key} = ?" for key in values.keys()])
    where_clause = " AND ".join([f"{key} LIKE ?" for key in identifiers.keys()])
    parameters = list(values.values()) + list(identifiers.values())

    with get_connection(db_file) as conn:
        with contextlib.closing(conn.cursor()) as cursor:
            sql_query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
            print(sql_query)
            print(parameters)
            cursor.execute(sql_query, parameters)
            conn.commit()
    

"""
Inserts a row into table in db_file.
Values is a dict with keys representing columns and values
representing values to insert.
"""
def insert(db_file, table, values):
    check_table(db_file, table)
    check_columns(db_file, table, values)    

    columns = ', '.join(values.keys())
    placeholders = ', '.join(['?'] * len(values))
    parameters = list(values.values())

    with get_connection(db_file) as conn:
        with contextlib.closing(conn.cursor()) as cursor:
            sql_query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            cursor.execute(sql_query, parameters)
            conn.commit()

    
"""
Deletes a row or rows in table.
Identifiers is a dict with keys representing columns and
values representing which rows to delete.
"""
def delete(db_file, table, identifiers):
    check_table(db_file, table)

    where_clause = " AND ".join([f"{key} LIKE ?" for key in identifiers.keys()])
    parameters = list(identifiers.values())

    with get_connection(db_file) as conn:
        with contextlib.closing(conn.cursor()) as cursor:
            sql_query = f"DELETE FROM {table} WHERE {where_clause}"
            cursor.execute(sql_query, parameters)
            conn.commit()


"""
For local testing (see more in test_db.py).
"""
def test():
    update_vals = {
        'days': 'TEST!!!',
        'roomnum': 'TEST'
    }
    id_vals = {
        'classid': 7838,
        'courseid': 3457
    }
    ref_row = {
        'classid': 7838,
        'courseid': 3457,
        'days': 'M',
        'starttime': '01:30 PM',
        'endtime': '04:20 PM',
        'bldg': 'CHANC',
        'roomnum': '105'
    }


if __name__ == "__main__":
    test()
