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
Returns the data types of each column in the specified table.

:param db_file: The database file.
:param table: The table name.
:return: A dictionary where keys are column names and values are data types.
"""
def get_column_data_types(db_file, table):
    check_table(db_file, table)

    with get_connection(db_file) as conn:
        with contextlib.closing(conn.cursor()) as cursor:
            cursor.execute(f"PRAGMA table_info({table})")
            columns_info = cursor.fetchall()
            data_types = {column_info[1]: column_info[2] for column_info in columns_info}
            return data_types



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
Performs an inner join on two tables based on a common column.
:param db_file: The database file.
:param table1: The first table to join.
:param table2: The second table to join.
:param join_column: The common column used for the join.
:return: A list of dictionaries representing the joined table.
"""
def inner_join(db_file, table1, table2, join_column):
    check_table(db_file, table1)
    check_table(db_file, table2)

    with get_connection(db_file) as conn:
        with contextlib.closing(conn.cursor()) as cursor:
            sql_query = f"SELECT * FROM {table1} INNER JOIN {table2} ON {table1}.{join_column} = {table2}.{join_column}"
            cursor.execute(sql_query)
            columns = [col[0] for col in cursor.description]
            data = []

            for row in cursor.fetchall():
                entry = {}
                for i, column in enumerate(columns):
                    entry[column] = row[i]
                data.append(entry)
            return data
        
"""
Performs an inner join on multiple tables based on a common column.

:param db_file: The database file.
:param tables: A list of tables to join.
:param join_column: The common column used for the join.
:return: A list of dictionaries representing the joined table.
"""
def inner_join_multiple_tables(db_file, tables, join_column):
    if len(tables) < 2:
        raise ValueError("At least two tables are required for a join.")

    for table in tables:
        check_table(db_file, table)

    with get_connection(db_file) as conn:
        with contextlib.closing(conn.cursor()) as cursor:
            # Constructing the SQL query for multiple tables
            join_clause = f" INNER JOIN ".join(
                [f"{tables[i]} ON {tables[i]}.{join_column} = {tables[0]}.{join_column}" for i in range(1, len(tables))]
            )
            sql_query = f"SELECT * FROM {tables[0]} INNER JOIN {join_clause}"

            cursor.execute(sql_query)
            columns = [col[0] for col in cursor.description]
            data = []

            for row in cursor.fetchall():
                entry = {}
                for i, column in enumerate(columns):
                    entry[column] = row[i]
                data.append(entry)
            return data

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
    pass
