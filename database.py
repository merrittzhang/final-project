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


def test():
    db_file = "reg.sqlite"
    tables = get_table_names(db_file)
    print(tables)

    columns = get_columns(db_file, 'classes')
    print(columns)

    classes = get_all(db_file, 'classes')
    print(f"Num classes: {len(classes)}")
    print(f"First 10:")
    for clss in classes[0:10]:
        print(f"{clss['classid']} - {clss['courseid']}")

    delete(db_file, 'classes', 7838)

    classes = get_all(db_file, 'classes')
    print(f"Num classes: {len(classes)}")
    print(f"First 10:")
    for clss in classes[0:10]:
        print(f"{clss['classid']} - {clss['courseid']}")


    class_dict = {
        'classid' : 7838, 
        'courseid': 3457, 
        'days': 'M',
        'starttime': '01:30 PM',
        'endtime': '04:20 PM', 
        'bldg': 'CHANC', 
        'roomnum': 105,
    }

    insert(db_file, 'classes', class_dict)

    classes = get_all(db_file, 'classes')
    print(f"Num classes: {len(classes)}")
    print(f"First 10:")
    for clss in classes[0:len(classes)]:
        print(f"{clss['classid']} - {clss['courseid']}")

    update_dict = {
        'courseid': 3458, 
    }

    update(db_file, 'classes', update_dict, 7838)

    classes = get_all(db_file, 'classes')
    print(f"Num classes: {len(classes)}")
    print(f"First 10:")
    for clss in classes[0:len(classes)]:
        print(f"{clss['classid']} - {clss['courseid']}")


if __name__ == "__main__":
    test()
