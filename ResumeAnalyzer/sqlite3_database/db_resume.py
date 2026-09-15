import streamlit as st
from sqlite3_database.db_tables import DBTables
from sqlite3_database.db_columns import DBColumns
from sqlite3_database.db_constants import DBConstants
from sqlite3_database.db_init import SqliteDb
from parsers.schema.resume_schema import ResumeSchema
from parsers.schema.job_description_schema import JDSchema
import json
import sqlite3

class SqliteDbResume:

    def __init__(self, sqlDb: SqliteDb):
        self.sqlDb = sqlDb
        self.createAllTables()

    def close(self):
        self.sqlDb.close()

    def begin(self):
        self.sqlDb.begin()

    def rollback(self):
        self.sqlDb.rollback()

    def commit(self):
        self.sqlDb.commit()

    def createAllTables(self):
        self.createResumeMainTable()
        self.createCertificationsTable()
        self.createCompaniesWorkedTable()
        self.createEducationTable()
        self.createProjectsTable()
        self.createSkillsTable()
        self.commit()

    def createResumeMainTable(self):
        self.sqlDb.cursor.execute(f"""
                    CREATE TABLE IF NOT EXISTS {DBTables.RESUMES_MAIN}(
                    {DBColumns.ID} INTEGER PRIMARY KEY AUTOINCREMENT,
                    {DBColumns.NAME} TEXT NOT NULL,
                    {DBColumns.EMAIL} TEXT UNIQUE NOT NULL,
                    {DBColumns.PHONE} TEXT UNIQUE,
                    {DBColumns.CURRENT_ROLE} TEXT,
                    {DBColumns.SUMMARY} TEXT,
                    {DBColumns.TOTAL_EXPERIENCE} REAL,
                    {DBColumns.LOCATION} TEXT,
                    {DBColumns.DOMAIN_EXPERTISE} TEXT,
                    {DBColumns.CREATED_AT} TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                    """)
        
    def createSkillsTable(self):
        self.sqlDb.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {DBTables.SKILLS} (
        {DBColumns.ID} INTEGER PRIMARY KEY AUTOINCREMENT,

        {DBColumns.RESUME_ID} INTEGER NOT NULL,

        {DBColumns.SKILL} TEXT NOT NULL,

        FOREIGN KEY ({DBColumns.RESUME_ID})
            REFERENCES resumes_main({DBColumns.ID})
            ON DELETE CASCADE
            )
        """)
        
        
    def createCompaniesWorkedTable(self):
        self.sqlDb.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {DBTables.COMPANIES_WORKED} (
        {DBColumns.ID} INTEGER PRIMARY KEY AUTOINCREMENT,

        {DBColumns.RESUME_ID} INTEGER NOT NULL,

        {DBColumns.COMPANY_NAME} TEXT NOT NULL,

        FOREIGN KEY ({DBColumns.RESUME_ID})
            REFERENCES resumes_main({DBColumns.ID})
            ON DELETE CASCADE
        )
        """)
        

    def createCertificationsTable(self):
        self.sqlDb.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {DBTables.CERTIFICATIONS} (
        {DBColumns.ID} INTEGER PRIMARY KEY AUTOINCREMENT,

        {DBColumns.RESUME_ID} INTEGER NOT NULL,

        {DBColumns.CERTIFICATION_NAME} TEXT NOT NULL,

        FOREIGN KEY ({DBColumns.RESUME_ID})
            REFERENCES resumes_main({DBColumns.ID})
            ON DELETE CASCADE
            )
        """)

    def createEducationTable(self):
        self.sqlDb.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {DBTables.EDUCATION} (
        {DBColumns.ID} INTEGER PRIMARY KEY AUTOINCREMENT,

        {DBColumns.RESUME_ID} INTEGER NOT NULL,

        {DBColumns.QUALIFICATION} TEXT NOT NULL,

        FOREIGN KEY ({DBColumns.RESUME_ID})
            REFERENCES resumes_main({DBColumns.ID})
            ON DELETE CASCADE
            )
        """)
        

    def createProjectsTable(self):
        self.sqlDb.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {DBTables.PROJECTS} (
        {DBColumns.ID} INTEGER PRIMARY KEY AUTOINCREMENT,

        {DBColumns.RESUME_ID} INTEGER NOT NULL,

        {DBColumns.PROJECT_NAME} TEXT NOT NULL,

        FOREIGN KEY ({DBColumns.RESUME_ID})
            REFERENCES resumes_main({DBColumns.ID})
            ON DELETE CASCADE
            )
        """)

    
    def insert_resume(
        self,
        resume_schema: ResumeSchema):
        try:
            self.sqlDb.cursor.execute(f"""INSERT INTO {DBTables.RESUMES_MAIN}(
            {DBColumns.NAME}, {DBColumns.EMAIL}, {DBColumns.PHONE}, {DBColumns.CURRENT_ROLE}, 
            {DBColumns.TOTAL_EXPERIENCE}, {DBColumns.LOCATION}, {DBColumns.SUMMARY}, {DBColumns.DOMAIN_EXPERTISE})
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
            resume_schema.name,
            resume_schema.email,
            resume_schema.phone,
            resume_schema.current_role,
            resume_schema.total_experience_years,
            resume_schema.current_location,
            resume_schema.summary,
            json.dumps(resume_schema.domain_expertise)
            ))
            return self.sqlDb.cursor.lastrowid
        except sqlite3.IntegrityError as ex:
            error_msg = str(ex)
            if "email" in error_msg:
                return DBConstants.EMAIL_ERROR
            elif "phone" in error_msg:
                return DBConstants.PHONE_ERROR
        except Exception as ex:
            print(ex)
            return DBConstants.OTHER_ERROR

    
    def insert_list_data(
        self,
        table_name: str,
        column_name: str,
        resume_id: int,
        values: list[str]
        ):
        if not values:
            return
        data = [
            (resume_id, value) for value in values
        ]
        self.sqlDb.cursor.executemany(
            f"""
            INSERT INTO {table_name}
            ({DBColumns.RESUME_ID}, {column_name})
            VALUES (?, ?)
            """,
            data
        )

    def fetchTotalCount(self) -> int:
        return self.sqlDb.cursor.execute(f"SELECT COUNT(*) FROM {DBTables.RESUMES_MAIN}").fetchone()[0]

    def fetchNameFromId(self, resume_id) -> str:
        query = f"""
        SELECT {DBColumns.NAME} FROM {DBTables.RESUMES_MAIN} WHERE {DBColumns.ID} = ? 
        """
        row = self.sqlDb.cursor.execute(query, (resume_id,)).fetchone()
        return row[0]

    def fetchExpFromId(self, resume_id) -> float:
        query = f"""
        SELECT {DBColumns.TOTAL_EXPERIENCE} FROM {DBTables.RESUMES_MAIN} WHERE {DBColumns.ID} = ? 
        """
        row = self.sqlDb.cursor.execute(query, (resume_id,)).fetchone()
        return row[0]
           
    def deleteAllResumes(self):
        self.sqlDb.cursor.execute(f"DELETE FROM {DBTables.RESUMES_MAIN}")
        self.sqlDb.cursor.execute(f"DELETE FROM sqlite_sequence WHERE name=?;", (DBTables.RESUMES_MAIN,))
        self.sqlDb.cursor.execute(f"DELETE FROM sqlite_sequence WHERE name=?;", (DBTables.PROJECTS,))
        self.sqlDb.cursor.execute(f"DELETE FROM sqlite_sequence WHERE name=?;", (DBTables.SKILLS,))
        self.sqlDb.cursor.execute(f"DELETE FROM sqlite_sequence WHERE name=?;", (DBTables.EDUCATION,))
        self.sqlDb.cursor.execute(f"DELETE FROM sqlite_sequence WHERE name=?;", (DBTables.CERTIFICATIONS,))
        self.sqlDb.cursor.execute(f"DELETE FROM sqlite_sequence WHERE name=?;", (DBTables.COMPANIES_WORKED,))
        self.sqlDb.conn.commit()
        
    def dropResumeTables(self):
        self.sqlDb.cursor.execute(f"DROP TABLE IF EXISTS {DBTables.PROJECTS}")
        self.sqlDb.cursor.execute(f"DROP TABLE IF EXISTS {DBTables.SKILLS}")
        self.sqlDb.cursor.execute(f"DROP TABLE IF EXISTS {DBTables.EDUCATION}")
        self.sqlDb.cursor.execute(f"DROP TABLE IF EXISTS {DBTables.CERTIFICATIONS}")
        self.sqlDb.cursor.execute(f"DROP TABLE IF EXISTS {DBTables.COMPANIES_WORKED}")
        self.sqlDb.cursor.execute(f"DROP TABLE IF EXISTS {DBTables.RESUMES_MAIN}")
        self.sqlDb.conn.commit()
    
    def fetchSkills(self, resume_id):
        query = f"""
        SELECT * FROM {DBTables.SKILLS} WHERE {DBColumns.RESUME_ID} = ? 
        """
        rows = self.sqlDb.conn.execute(query, (resume_id,)).fetchall()
        skills_list = [row[2] for row in rows]
        return skills_list
    
    def fetchCertifications(self, resume_id):
        query = f"""
        SELECT * FROM {DBTables.CERTIFICATIONS} WHERE {DBColumns.RESUME_ID} = ? 
        """
        rows = self.sqlDb.conn.execute(query, (resume_id,)).fetchall()
        cert_list = [row[2] for row in rows]
        return cert_list
    
    def fetchProjects(self, resume_id):
        query = f"""
        SELECT * FROM {DBTables.PROJECTS} WHERE {DBColumns.RESUME_ID} = ? 
        """
        rows = self.sqlDb.conn.execute(query, (resume_id,)).fetchall()
        proj_list = [row[2] for row in rows]
        return proj_list

    def fetchEducations(self, resume_id):
        query = f"""
        SELECT * FROM {DBTables.EDUCATION} WHERE {DBColumns.RESUME_ID} = ? 
        """
        rows = self.sqlDb.conn.execute(query, (resume_id,)).fetchall()
        edu_list = [row[2] for row in rows]
        return edu_list

    def fetchCompanies(self, resume_id):
        query = f"""
        SELECT * FROM {DBTables.COMPANIES_WORKED} WHERE {DBColumns.RESUME_ID} = ? 
        """
        rows = self.sqlDb.conn.execute(query, (resume_id,)).fetchall()
        company_list = [row[2] for row in rows]
        return company_list
    
    def fetchSummary(self, resume_id):
        query = f"""
        SELECT {DBColumns.SUMMARY} FROM {DBTables.RESUMES_MAIN} WHERE {DBColumns.ID} = ? 
        """
        row = self.sqlDb.conn.execute(query, (resume_id,)).fetchone()
        return row[0]
    
    def fetchExperience(self, resume_id):
        query = f"""
        SELECT {DBColumns.TOTAL_EXPERIENCE} FROM {DBTables.RESUMES_MAIN} WHERE {DBColumns.ID} = ? 
        """
        row = self.sqlDb.conn.execute(query, (resume_id,)).fetchone()
        return row[0]
    
    def fetchLocation(self, resume_id):
        query = f"""
        SELECT {DBColumns.LOCATION} FROM {DBTables.RESUMES_MAIN} WHERE {DBColumns.ID} = ? 
        """
        row = self.sqlDb.conn.execute(query, (resume_id,)).fetchone()
        return row[0]
    
    def fetchJDCandidatesData(self, minimum_experience_years: int) -> list[int]:

        query = f"""SELECT {DBColumns.ID} FROM {DBTables.RESUMES_MAIN} 
                            WHERE {DBColumns.TOTAL_EXPERIENCE} >= ?
                            """
        param = [minimum_experience_years]
        row_ids = self.sqlDb.conn.execute(query, param).fetchall()
        resume_ids: list[int] = [row[0] for row in row_ids]
        return resume_ids

    def fetchAllDataFromMainWithId(self, resume_id: int):
        if resume_id > -1:
            return self.sqlDb.cursor.execute(f"SELECT * FROM {DBTables.RESUMES_MAIN} WHERE {DBColumns.ID} = ?", (resume_id, )).fetchall()
        else:
            return self.sqlDb.cursor.execute(f"SELECT * FROM {DBTables.RESUMES_MAIN}").fetchall()

    def fetchAllData(self):
        rows_main = self.sqlDb.cursor.execute(f"SELECT * FROM {DBTables.RESUMES_MAIN}").fetchall()
        rows_cert = self.sqlDb.cursor.execute(f"SELECT * FROM {DBTables.CERTIFICATIONS}").fetchall()
        rows_skills = self.sqlDb.cursor.execute(f"SELECT * FROM {DBTables.SKILLS}").fetchall()
        rows_edu = self.sqlDb.cursor.execute(f"SELECT * FROM {DBTables.EDUCATION}").fetchall()
        rows_companies = self.sqlDb.cursor.execute(f"SELECT * FROM {DBTables.COMPANIES_WORKED}").fetchall()
        st.write("\nResumes\n")
        for row in rows_main:
            st.write(row)
        st.write("\nCertifications\n")
        for row in rows_cert:
            st.write(row)
        st.write("\nSkills\n")
        for row in rows_skills:
            st.write(row)
        st.write("\nEducation\n")
        for row in rows_edu:
            st.write(row)
        st.write("\nCompanies Worked\n")
        for row in rows_companies:
            st.write(row)
        
    