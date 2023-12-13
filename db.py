import psycopg2

class db:
    def __init__(self, dsn):
        self.conn = psycopg2.connect(dsn)

    def get_tables(self):
        with self.conn.cursor() as cur:
            cur.execute("""SELECT table_name FROM information_schema.tables 
                           WHERE table_schema = 'public'""")
            return [row[0] for row in cur.fetchall()]

    def get_columns(self, table_name):
        with self.conn.cursor() as cur:
            cur.execute("""SELECT column_name FROM information_schema.columns 
                           WHERE table_name = %s""", (table_name,))
            return [row[0] for row in cur.fetchall()]

    def select(self, table_name):
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT * FROM {table_name}")
            columns = [desc[0] for desc in cur.description]
            return [{columns[0]: dict(zip(columns[1:], row[1:]))} for row in cur.fetchall()]

    def update(self, table_name, primary_key, primary_key_value, update_data):
        set_clause = ', '.join([f"{key} = %s" for key in update_data])
        with self.conn.cursor() as cur:
            cur.execute(f"UPDATE {table_name} SET {set_clause} WHERE {primary_key} = %s",
                        tuple(update_data.values()) + (primary_key_value,))
            self.conn.commit()

    def insert(self, table_name, data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        with self.conn.cursor() as cur:
            cur.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})", tuple(data.values()))
            self.conn.commit()

    def delete(self, table_name, primary_key, primary_key_value):
        with self.conn.cursor() as cur:
            cur.execute(f"DELETE FROM {table_name} WHERE {primary_key} = %s", (primary_key_value,))
            self.conn.commit()

    def join(self, table1, table2, join_condition):
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT * FROM {table1} JOIN {table2} ON {join_condition}")
            columns = [desc[0] for desc in cur.description]
            return [{columns[0]: dict(zip(columns[1:], row[1:]))} for row in cur.fetchall()]

    def close(self):
        self.conn.close()
