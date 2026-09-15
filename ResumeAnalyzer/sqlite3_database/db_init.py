import sqlite3 as sqlDb
from sqlite3_database.db_constants import DBConstants

class SqliteDb:
    def __init__(self):
        self.conn = sqlDb.connect("resume_analyzer.db", check_same_thread=False)
        # Enable foreign key support
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.conn.cursor()

    def begin(self):
         self.conn.execute(DBConstants.BEGIN_TRANSACTION)

    def commit(self):
        self.conn.commit()

    def rollback(self):
          self.conn.rollback()

    def close(self):
         self.conn.close()