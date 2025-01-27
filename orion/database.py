import os
import sqlite3
from typing import Dict, List


class Database:
    def __init__(self, __dir: str):
        if not os.path.exists(__dir):
            os.makedirs(__dir)
        self.__dir = __dir

    def fetch_all(self) -> Dict[str, sqlite3.Connection]:
        connections = {}
        for file in os.listdir(self.__dir):
            if file.endswith(".db"):
                connections[file] = sqlite3.connect(f"{self.__dir}/{file}")
        return connections

    def list_all(self) -> List[str]:
        return os.listdir(self.__dir)

    def list_tables(self, name: str) -> List[str]:
        con = sqlite3.connect(f"{self.__dir}/{name}")
        cursor = con.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return [table[0] for table in cursor.fetchall()]

    def table_to_dict(self, name: str, table: str) -> List[Dict[str, str]]:
        con = sqlite3.connect(f"{self.__dir}/{name}")
        cursor = con.cursor()
        cursor.execute(f"SELECT * FROM {table}")
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def connect(self, name: str) -> sqlite3.Connection:
        return sqlite3.connect(f"{self.__dir}/{name}")

    def remove(self, name: str):
        os.remove(f"{self.__dir}/{name}")
