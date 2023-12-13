import sqlite3
from typing import List, Type, Any

class DB:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def close(self):
        self.conn.close()

    def camel_to_snake(self, name: str) -> str:
        import re
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def column_names(self, cls: Type) -> List[str]:
        return [self.camel_to_snake(attr) for attr in cls.__dict__ if not attr.startswith('_')]

    def table_name(self, cls: Type) -> str:
        return self.camel_to_snake(cls.__name__)

    def find(self, cls: Type) -> List[Any]:
        cursor = self.conn.cursor()
        table_name = self.table_name(cls)
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        columns = self.column_names(cls)
        result = [cls(**dict(zip(columns, row))) for row in rows]
        return result

    def first(self, cls: Type) -> Any:
        cursor = self.conn.cursor()
        table_name = self.table_name(cls)
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 1")
        row = cursor.fetchone()
        if not row:
            return None
        columns = self.column_names(cls)
        return cls(**dict(zip(columns, row)))

    def create(self, instance: Any) -> None:
        cursor = self.conn.cursor()
        table_name = self.table_name(type(instance))
        columns = self.column_names(type(instance))
        values = [getattr(instance, col) for col in columns]
        placeholders = ', '.join('?' * len(columns))
        cursor.execute(f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})", values)
        self.conn.commit()
        setattr(instance, 'id', cursor.lastrowid)
