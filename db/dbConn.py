import sqlite3

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.initialize_connection()
        return cls._instance

    def initialize_connection(self):
        try:
            self.conn = sqlite3.connect("./db/DB.db", check_same_thread=False)
            self.cursor = self.conn.cursor()
            print("SQLite connection is successful.")
        except Exception as e:
            print(f"SQLite error during connection initialization: {e}")
            raise Exception(f"SQLite error during connection initialization: {e}")