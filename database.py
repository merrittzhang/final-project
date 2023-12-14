import contextlib
import sqlite3


class DatabaseError(Exception):
    def __init__(self, string):
        self.error = string
    
    def __str__(self):
        return self.error


class InvalidTable(DatabaseError):
    def __init__(self, string):
        self.error = string
    
    def __str__(self):
        return self.error


def get_connection(db_file):
    conn = sqlite3.connect(db_file)
    return conn


def check_table(db_file, table):
    tables = get_table_names(db_file)
    if table not in tables:
        raise DatabaseError(f"Table {table} does not exist in {db_file}")

def get_table_names(db_file):
    with get_connection(db_file) as conn:
        with contextlib.closing(conn.cursor()) as cursor:
            sql_query = "SELECT name FROM sqlite_master WHERE type='table'"
            cursor.execute(sql_query)
            rows = cursor.fetchall()
            tables = [row[0] for row in rows]
            return tables
        

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
updates rows in table from db_file. In row with primary key 
classid, update the columns indicated by all the keys in 
dictionary values with all the values in dictionary values
"""
def update(db_file, table, values, classid):
    check_table(db_file, table)
    set_clause = ", ".join([f"{key} = ?" for key in values.keys()])
    parameters = list(values.values()) + [classid]

    with get_connection(db_file) as conn:
        with contextlib.closing(conn.cursor()) as cursor:
            sql_query = f"UPDATE {table} SET {set_clause} WHERE classid = ?"
            cursor.execute(sql_query, parameters)
            conn.commit()

    

"""
add a row to table from db_file. Add values from dictionary
values to columns indicated by keys in dictionary values
"""
def insert(db_file, table, values):
    check_table(db_file, table)
    columns = ', '.join(values.keys())
    placeholders = ', '.join(['?'] * len(values))
    parameters = list(values.values())

    with get_connection(db_file) as conn:
        with contextlib.closing(conn.cursor()) as cursor:
            sql_query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            cursor.execute(sql_query, parameters)
            conn.commit()

    
"""
deletes a row with primary key classid from table 
in db_file.
"""
def delete(db_file, table, classid):
    check_table(db_file, table)

    with get_connection(db_file) as conn:
        with contextlib.closing(conn.cursor()) as cursor:
            sql_query = f"DELETE FROM {table} WHERE classid = ?"
            cursor.execute(sql_query, (classid,))
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


if __name__ == "__main__":
    pass
