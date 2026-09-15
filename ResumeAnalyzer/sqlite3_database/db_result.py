import sqlite3 as sqlDb
import streamlit as st
from sqlite3_database.db_tables import DBTables
from sqlite3_database.db_columns import DBColumns
from sqlite3_database.db_init import SqliteDb
from sqlite3_database.db_constants import DBConstants
from parsers.schema.job_description_schema import JDSchema
from parsers.schema.result_schema import ResultListSchema
import json

class SqliteDbResult:

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
        self.createAnalysisResultTable()

    def dropResultTables(self):
        self.sqliteDb.cursor.execute(f"DROP TABLE IF EXISTS {DBTables.ANALYSIS_RESULT}")
        self.commit()

    def deleteAllResults(self):
        self.sqliteDb.cursor.execute(f"DELETE FROM {DBTables.ANALYSIS_RESULT}")
        self.commit()
        
    def fetchAnalyzedResumeIds(self) -> list[int]:
        rows = self.sqliteDb.cursor.execute(f"""
        SELECT DISTINCT {DBColumns.RESUME_ID}
        FROM {DBTables.ANALYSIS_RESULT}
        """
        ).fetchall()
        return [row[0] for row in rows]
    
    def createAnalysisResultTable(self):
        self.sqliteDb.cursor.execute(f"""
                    CREATE TABLE IF NOT EXISTS {DBTables.ANALYSIS_RESULT}(
                    {DBColumns.ID} INTEGER PRIMARY KEY AUTOINCREMENT,
                    {DBColumns.JD_ID} INTEGER NOT NULL,
                    {DBColumns.RESUME_ID} INTEGER NOT NULL,
                    {DBColumns.SKILLS_MATCH} TEXT,
                    {DBColumns.MATCH_PERCENT} REAL,
                    {DBColumns.MISSING_SKILLS} TEXT,
                    {DBColumns.RECOMMENDATION} TEXT,
                    {DBColumns.STRENGTHS} TEXT,
                    {DBColumns.WEAKNESS} TEXT,
                    {DBColumns.CREATED_AT} TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE({DBColumns.JD_ID}, {DBColumns.RESUME_ID}),
                    FOREIGN KEY ({DBColumns.RESUME_ID})
                    REFERENCES resumes_main({DBColumns.ID})
                    ON DELETE CASCADE,
                    FOREIGN KEY ({DBColumns.JD_ID})
                    REFERENCES jd_main({DBColumns.ID})
                    ON DELETE CASCADE
                    )
                    """)
    
    def insertResult(self, list):
        if not list:
            return
        for result in list:
            try:
                self.sqliteDb.cursor.execute(f"""
                INSERT INTO {DBTables.ANALYSIS_RESULT}(
                {DBColumns.JD_ID}, 
                {DBColumns.RESUME_ID},
                {DBColumns.SKILLS_MATCH}, 
                {DBColumns.MATCH_PERCENT}, 
                {DBColumns.MISSING_SKILLS},
                {DBColumns.RECOMMENDATION}, 
                {DBColumns.STRENGTHS}, 
                {DBColumns.WEAKNESS})
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                result.job_des_id,
                result.resume_id,
                json.dumps(result.matched_skills),
                result.match_score,
                json.dumps(result.missing_skills),
                result.recommendation, 
                result.strengths, 
                result.weakness,
                ))
            except Exception as ex:
                print(f"Exception: {ex}")
                raise Exception(ex)
    
    def fetchAllResults(self):
        st.write("\nResults Main\n")
        rows_main = self.sqliteDb.cursor.execute(f"SELECT * FROM {DBTables.ANALYSIS_RESULT}").fetchall()
        for row in rows_main:
            st.write(row)
            st.write("\n")

    def fetchDetailsFromIds(self, resume_id: int, jd_id: int):
        return self.sqliteDb.cursor.execute(f"SELECT * FROM {DBTables.ANALYSIS_RESULT} WHERE {DBColumns.RESUME_ID} = ? AND {DBColumns.JD_ID} = ?", 
                                            (resume_id, jd_id, )).fetchall()

    def totalCount(self) -> int:
        return self.sqliteDb.cursor.execute(f"SELECT COUNT(*) FROM {DBTables.ANALYSIS_RESULT}").fetchone()[0]

    def totalMatchingResumesCount(self, jd_id) -> int:
        return self.sqliteDb.cursor.execute(f"SELECT COUNT(*) FROM {DBTables.ANALYSIS_RESULT} WHERE {DBColumns.JD_ID} = ?", (jd_id, )).fetchone()[0]

    def fetchMatchedResumeIds(self, jd_id: int) -> list[int]:
        rows = self.sqliteDb.cursor.execute(f"SELECT {DBColumns.RESUME_ID} FROM {DBTables.ANALYSIS_RESULT} WHERE {DBColumns.JD_ID} = ?", (jd_id, )).fetchall()
        return [row[0] for row in rows]

    def fetchTopNResults(self, n: int):
        return self.sqliteDb.cursor.execute(f"""
        SELECT * FROM {DBTables.ANALYSIS_RESULT} ORDER BY {DBColumns.MATCH_PERCENT} DESC LIMIT ?""", 
        (n,)).fetchall()

    def fetchTopNResultsForJdId(self, n: int, jdId: int):
            query = f"""
            SELECT * FROM {DBTables.ANALYSIS_RESULT} WHERE {DBColumns.JD_ID} = ? ORDER BY {DBColumns.MATCH_PERCENT} DESC LIMIT ?"""
            return self.sqliteDb.cursor.execute(query, 
            (jdId, n)).fetchall()

