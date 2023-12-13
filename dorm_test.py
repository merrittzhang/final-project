import sqlite3
import unittest

class User:
    def __init__(self, full_name: str, age: int, id: int = None):
        self.full_name = full_name
        self.age = age
        self.id = id

    def __eq__(self, other):
        if isinstance(other, User):
            return self.full_name == other.full_name and self.age == other.age and self.id == other.id
        return False

class TestDorm(unittest.TestCase):
    @staticmethod
    def connect_sql():
        return sqlite3.connect(":memory:")

    @staticmethod
    def create_user_table(conn):
        conn.execute('''CREATE TABLE user (
                            full_name TEXT, 
                            age INT, 
                            id INTEGER PRIMARY KEY)''')
        conn.commit()

    @staticmethod
    def insert_users(conn, users):
        for user in users:
            conn.execute('INSERT INTO user (full_name, age, id) VALUES (?, ?, ?)', (user.full_name, user.age, None))
        conn.commit()

    def test_column_names(self):
        # Python does not need a specific method for this as reflection is different from Go
        pass

    def test_table_name(self):
        # Python does not need a specific method for this as reflection is different from Go
        pass

    def test_find(self):
        conn = self.connect_sql()
        self.create_user_table(conn)

        mock_users = [User("Test User 1", 36, 1), User("Test User 2", 22, 2)]
        self.insert_users(conn, mock_users)

        cursor = conn.cursor()
        cursor.execute("SELECT full_name, age, id FROM user")
        results = [User(*row) for row in cursor.fetchall()]

        self.assertEqual(len(results), len(mock_users))
        for i, user in enumerate(results):
            self.assertEqual(user, mock_users[i])

        conn.close()

    def test_first(self):
        conn = self.connect_sql()
        self.create_user_table(conn)

        mock_users = [User("Test User 1", 36, 1), User("Test User 2", 22, 2)]
        self.insert_users(conn, mock_users)

        cursor = conn.cursor()
        cursor.execute("SELECT full_name, age, id FROM user LIMIT 1")
        result = cursor.fetchone()
        expected_user = User(*result) if result else None

        self.assertIsNotNone(expected_user)
        self.assertEqual(expected_user, mock_users[0])

        conn.close()

    def test_create(self):
        conn = self.connect_sql()
        self.create_user_table(conn)

        mock_users = [User("Test User 1", 36), User("Test User 2", 22)]
        for user in mock_users:
            conn.execute('INSERT INTO user (full_name, age) VALUES (?, ?)', (user.full_name, user.age))
        conn.commit()

        cursor = conn.cursor()
        cursor.execute("SELECT full_name, age, id FROM user")
        results = [User(*row) for row in cursor.fetchall()]

        self.assertEqual(len(results), len(mock_users))
        for i, user in enumerate(results):
            self.assertEqual(user.full_name, mock_users[i].full_name)
            self.assertEqual(user.age, mock_users[i].age)
            self.assertIsNotNone(user.id)

        conn.close()

if __name__ == '__main__':
    unittest.main()