import contextlib
import os
import sqlite3


"""
Database related exceptions:
"""
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
    

class InvalidDB(DatabaseError):
    def __init__(self, string):
        self.error = string
    
    def __str__(self):
        return f"InvalidDB: {self.error}"


"""
Checks that a database at db_file exists.
"""
def check_db(db_file):
    if not os.path.exists(db_file):
        raise InvalidDB(f"Database at {db_file} does not exist.")


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
def check_columns(db_file, table, row, include_all=True):
    columns = get_columns(db_file, table)
    keys = row.keys()
    if include_all and len(keys) != len(columns):
        raise BadFields(f"Row {row} does not have keys matching the columns of {table}")
    for key in keys:
        if key not in columns:
            raise BadFields(f"Row {row} does not have keys matching the columns of {table}")


"""
Returns a connection to a database in db_file.
"""
def get_connection(db_file):
    check_db(db_file)
    conn = sqlite3.connect(db_file)
    return conn


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
    check_columns(db_file, table, values, include_all=False)
    check_columns(db_file, table, identifiers, include_all=False)

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
    check_columns(db_file, table, identifiers, include_all=False)

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
:param table1: The primary table.
:param table2: A list of tables to join.
:param join_column: A list of list of tuples. Each tuple is (table1, col1, table2, col2).
:return: A list of dictionaries representing the joined table.
"""
def join(db_file, prim_table, tables, identifiers):
    check_table(db_file, prim_table)
    for table in tables:
        check_table(db_file, table)
    for join_identifiers in identifiers:
        if len(join_identifiers) < 1:
            raise DatabaseError("Must have atleast one column to join on.")
        for identifier in join_identifiers:
            table1, col1, table2, col2 = identifier
            check_table(db_file, table1)
            check_table(db_file, table2)
            check_columns(db_file, table1, {col1: ""}, include_all=False)
            check_columns(db_file, table2, {col2: ""}, include_all=False)
    if len(tables) != len(identifiers):
        raise DatabaseError("Number of tables to join must match number of identifiers.")
    
    columns = get_columns(db_file, prim_table)
    lookupTable = [prim_table] * len(columns)
    for table in tables:
        secColumns = get_columns(db_file, table)
        columns += secColumns
        lookupTable += [table] * len(secColumns)


    with get_connection(db_file) as conn:
        with contextlib.closing(conn.cursor()) as cursor:
            sql_query = f"SELECT * FROM {prim_table}"
            for table, join_identifiers in zip(tables, identifiers):
                join_query = f" JOIN {table} ON "
                select_query = " AND ".join([f"{table1}.{col1} = {table2}.{col2}" for table1, col1, table2, col2 in join_identifiers])
                sql_query += join_query + select_query
            print(sql_query)
            cursor.execute(sql_query)
            
            data = []
            for row in cursor.fetchall():
                entry = {}
                for i, col in enumerate(row):
                    if columns[i] in entry and entry[columns[i]] != col:
                        entry[f"{lookupTable[i]}.{columns[i]}"] = col
                    else:
                        entry[columns[i]] = col
                data.append(entry)
            return data
        

"""
For local testing (see more in test_db.py).
"""
def test():
    db_url = "example_dbs/reg.sqlite"
    test = join(db_url, "courses", ['crosslistings', 'coursesprofs', 'profs'], 
                [[('courses', 'courseid', 'crosslistings', 'courseid')], 
                 [('courses', 'courseid', 'coursesprofs', 'courseid')], 
                 [('coursesprofs', 'profid', 'profs', 'profid')]])
    print(f"{len(test)} results found")
    for row in test[0:10]:
        print(f"{row['dept']} {row['coursenum']} - {row['title']} - {row['profname']}")
    print(test[0])


if __name__ == "__main__":
    test()
