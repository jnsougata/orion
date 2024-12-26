import os
import sqlite3

class Database:
    def __init__(self, __dir: str):
        if not os.path.exists(__dir):
            os.makedirs(__dir)
        self.__dir = __dir

    def create(self, name: str) -> sqlite3.Connection:
        return sqlite3.connect(f"{self.__dir}/{name}")

    def connect(self, name: str) -> sqlite3.Connection:
        return sqlite3.connect(f"{self.__dir}/{name}")