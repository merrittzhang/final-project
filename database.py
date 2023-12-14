import contextlib
import sqlite3


class DatabaseError(Exception):
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


if __name__ == "__main__":
    test()
