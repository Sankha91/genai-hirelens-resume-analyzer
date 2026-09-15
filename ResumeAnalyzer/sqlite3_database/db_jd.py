import sqlite3 as sqlDb
import streamlit as st
from sqlite3_database.db_init import SqliteDb
from sqlite3_database.db_tables import DBTables
from sqlite3_database.db_columns import DBColumns
from sqlite3_database.db_constants import DBConstants
from parsers.schema.job_description_schema import JDSchema
import json

class SqliteDbJD:

    def __init__(self, sqliteDb: SqliteDb):
        self.sqliteDb = sqliteDb
        self.createAllTables()
    
    def close(self):
        self.sqliteDb.close()
    
    def begin(self):
        self.sqliteDb.begin()
    
    def rollback(self):
        self.sqliteDb.rollback()
    
    def commit(self):
        self.sqliteDb.commit()
    
    def createAllTables(self):
        self.createJDMainTable()
        self.createJDPreferredSkillsTable()
        self.createJDMandatorySkillsTable()
        self.createJDLocationTable()
        self.commit()
    
    def createJDMainTable(self):
        self.sqliteDb.cursor.execute(f"""
                    CREATE TABLE IF NOT EXISTS {DBTables.JD_MAIN}(
                    {DBColumns.ID} INTEGER PRIMARY KEY AUTOINCREMENT,
                    {DBColumns.JD_TITLE} TEXT,
                    {DBColumns.JD_EXPERIENCE} REAL,
                    {DBColumns.JD_RESPONSIBILITY} TEXT,
                    {DBColumns.JD_RAW_TEXT} TEXT,
                    {DBColumns.JD_JOB_TYPE} TEXT,
                    {DBColumns.CREATED_AT} TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                    """)
    
    def createJDMandatorySkillsTable(self):
        self.sqliteDb.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {DBTables.JD_REQUIRED_SKILLS} (
        {DBColumns.ID} INTEGER PRIMARY KEY AUTOINCREMENT,

        {DBColumns.JD_ID} INTEGER NOT NULL,

        {DBColumns.SKILL} TEXT,

        FOREIGN KEY ({DBColumns.JD_ID})
            REFERENCES {DBTables.JD_MAIN}({DBColumns.ID})
            ON DELETE CASCADE
            )
        """)
    
    def createJDPreferredSkillsTable(self):
        self.sqliteDb.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {DBTables.JD_PREFERRED_SKILLS} (
        {DBColumns.ID} INTEGER PRIMARY KEY AUTOINCREMENT,

        {DBColumns.JD_ID} INTEGER NOT NULL,

        {DBColumns.SKILL} TEXT,

        FOREIGN KEY ({DBColumns.JD_ID})
            REFERENCES {DBTables.JD_MAIN}({DBColumns.ID})
            ON DELETE CASCADE
            )
        """)
    
    def createJDLocationTable(self):
        self.sqliteDb.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {DBTables.JD_LOCATION} (
        {DBColumns.ID} INTEGER PRIMARY KEY AUTOINCREMENT,

        {DBColumns.JD_ID} INTEGER NOT NULL,

        {DBColumns.LOCATION} TEXT,

        FOREIGN KEY ({DBColumns.JD_ID})
            REFERENCES {DBTables.JD_MAIN}({DBColumns.ID})
            ON DELETE CASCADE
            )
        """)
    
    def insert_jd(
        self,
        jd_schema: JDSchema,
        raw_text: str) -> int:
        try:
            self.sqliteDb.cursor.execute(f"""
            INSERT INTO {DBTables.JD_MAIN}(
            {DBColumns.JD_TITLE}, {DBColumns.JD_EXPERIENCE}, 
            {DBColumns.JD_RESPONSIBILITY}, {DBColumns.JD_RAW_TEXT}, {DBColumns.JD_JOB_TYPE})
            VALUES (?, ?, ?, ?, ?)
            """, (
            jd_schema.role,
            jd_schema.minimum_experience_years,
            json.dumps(jd_schema.responsibilities),
            raw_text,
            jd_schema.job_type
            ))
            return self.sqliteDb.cursor.lastrowid
        except Exception as ex:
            print(ex)
            return DBConstants.OTHER_ERROR
    
    def insert_jd_list_data(
        self,
        table_name: str,
        column_name: str,
        jd_id: int,
        values: list[str]
        ):
        try:
            if not values:
                return
            data = [
            (jd_id, value) for value in values
            ]
            self.sqliteDb.cursor.executemany(
                f"""
                INSERT INTO {table_name}
                ({DBColumns.JD_ID}, {column_name})
                VALUES (?, ?)
                """,
                data
            )
        except Exception as ex:
            print(ex)  

    def fetchTotalCount(self) -> int:
        return self.sqliteDb.cursor.execute(f"SELECT COUNT(*) FROM {DBTables.JD_MAIN}").fetchone()[0]

    def fetchTotalSkillsCount(self, jdId: int) -> int:
        query = f""" 
        SELECT COUNT(*) FROM {DBTables.JD_REQUIRED_SKILLS} WHERE {DBColumns.JD_ID} = ?
        """
        return self.sqliteDb.cursor.execute(query, (jdId,)).fetchone()[0]

    def fetchLatestJdId(self):
        query = f"""
        SELECT {DBColumns.ID} FROM {DBTables.JD_MAIN} ORDER BY {DBColumns.ID} DESC
        LIMIT 1
        """
        row = self.sqliteDb.cursor.execute(query).fetchone()
        return row[0]


    def deleteAllJDs(self):
        self.sqliteDb.cursor.execute(f"DELETE FROM {DBTables.JD_MAIN}")
        self.sqliteDb.cursor.execute(f"DELETE FROM sqlite_sequence WHERE name=?;", (DBTables.JD_MAIN,))
        self.sqliteDb.cursor.execute(f"DELETE FROM sqlite_sequence WHERE name=?;", (DBTables.JD_PREFERRED_SKILLS,))
        self.sqliteDb.cursor.execute(f"DELETE FROM sqlite_sequence WHERE name=?;", (DBTables.JD_REQUIRED_SKILLS,))
        self.sqliteDb.cursor.execute(f"DELETE FROM sqlite_sequence WHERE name=?;", (DBTables.JD_LOCATION,))
        self.sqliteDb.commit()

    def dropJDTables(self):
        self.sqliteDb.cursor.execute(f"DROP TABLE IF EXISTS {DBTables.JD_PREFERRED_SKILLS}")
        self.sqliteDb.cursor.execute(f"DROP TABLE IF EXISTS {DBTables.JD_REQUIRED_SKILLS}")
        self.sqliteDb.cursor.execute(f"DROP TABLE IF EXISTS {DBTables.JD_LOCATION}")
        self.sqliteDb.cursor.execute(f"DROP TABLE IF EXISTS {DBTables.JD_MAIN}")
        self.sqliteDb.commit()

    def fetchJDDetailsMain(self):
            return self.sqliteDb.cursor.execute(f"SELECT * FROM {DBTables.JD_MAIN}").fetchall()

    def fetchJDDetailsMainFromId(self, jd_id: int):
            return self.sqliteDb.cursor.execute(f"SELECT * FROM {DBTables.JD_MAIN} WHERE {DBColumns.ID} = ?", (jd_id, )).fetchone()
    
    def fetchLocations(self, jdId: int):
            return self.sqliteDb.cursor.execute(f"SELECT {DBColumns.LOCATION} FROM {DBTables.JD_LOCATION} WHERE {DBColumns.JD_ID} = ?", (jdId, )).fetchall()
    
    def fetchPreferredSkills(self, jdId: int):
            return self.sqliteDb.cursor.execute(f"SELECT {DBColumns.SKILL} FROM {DBTables.JD_PREFERRED_SKILLS} WHERE {DBColumns.JD_ID} = ?", (jdId, )).fetchall()

    def fetchMandatorySkills(self, jdId: int):
            return self.sqliteDb.cursor.execute(f"SELECT {DBColumns.SKILL} FROM {DBTables.JD_REQUIRED_SKILLS} WHERE {DBColumns.JD_ID} = ?", (jdId, )).fetchall()
            
    def fetchAllData(self):
        st.write("\nJD Main\n")
        rows_main = self.sqliteDb.cursor.execute(f"SELECT * FROM {DBTables.JD_MAIN}").fetchall()
        for row in rows_main:
            st.write(row)
            st.write("\n")
        st.write("\nPreferred Skills\n")
        rows_skills = self.sqliteDb.cursor.execute(f"SELECT * FROM {DBTables.JD_PREFERRED_SKILLS}").fetchall()
        for row in rows_skills:
            st.write(f"{row} \n")
        st.write("\nRequired Skills\n")
        rows = self.sqliteDb.cursor.execute(f"SELECT * FROM {DBTables.JD_REQUIRED_SKILLS}").fetchall()
        for row in rows:
            st.write(f"{row} \n")
        st.write("\nLocation\n")
        rows_location = self.sqliteDb.cursor.execute(f"SELECT * FROM {DBTables.JD_LOCATION}").fetchall()
        for row in rows_location:
            st.write(f"{row} \n")
        
    
    
