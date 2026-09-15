import streamlit as st
import tempfile
import json
from sqlite3_database.db_tables import DBTables
from sqlite3_database.db_columns import DBColumns
from sqlite3_database.db_constants import DBConstants
from parsers.schema.resume_schema import ResumeSchema
from sqlite3_database.db_resume import SqliteDbResume
from sqlite3_database.db_resume import SqliteDbResume
from data.resume_data_model import ResumeDataModel
from embedding.vector_store import add_resume_vector_store
from loaders.document_loader import load_text_from_file
from parsers.document_parsers import parse_resume
import os

class ResumeRepository:

    file_path = []

    def __init__(self, sqliteDb: SqliteDbResume):
        self.sqliteDb = sqliteDb

    def fetchTotalCount(self) -> int:
        return self.sqliteDb.fetchTotalCount()

    def fetchJDCandidatesData(self, exp: int) -> list[int]:
        return self.sqliteDb.fetchJDCandidatesData(exp)

    def fetchNameFromId(self, id: int) -> str:
        return self.sqliteDb.fetchNameFromId(id)

    def fetchExpFromId(self, id: int) -> float:
        return self.sqliteDb.fetchExpFromId(id)

    def filter(self, dataModelList: list[ResumeDataModel], sort_by: str, status: str, status_arr: list[str], sort_arr: list[str]):
        if status != status_arr[0]:
            if status == status_arr[1]:
                dataModelList[:] = [model for model in dataModelList if model.isAnalyzed]
            elif status == status_arr[2]:
                dataModelList[:] = [model for model in dataModelList if not model.isAnalyzed]

        if sort_by == sort_arr[0]:  # Newest
            dataModelList.sort(key=lambda x: x.id, reverse=True)
        elif sort_by == sort_arr[1]:  # Oldest
            dataModelList.sort(key=lambda x: x.id)
        elif sort_by == sort_arr[2]:  # Name
            dataModelList.sort(key=lambda x: x.name.lower())

    def updateAnalyzedResumeModel(self, dataModelList: list[ResumeDataModel], analyzedResumeIds: list[int]):
        for resume_model in dataModelList:
            if resume_model.id in analyzedResumeIds:
                resume_model.isAnalyzed = True

    def fetchAllResumes(self) -> list[ResumeDataModel]:
        rows_main = self.sqliteDb.fetchAllDataFromMainWithId(resume_id=-1)
        results = []
        for row in rows_main:
            dataModel: ResumeDataModel = ResumeDataModel()
            dataModel.id = row[0]
            dataModel.name = row[1]
            dataModel.currentRole = row[4]
            dataModel.totalExperience = row[6]
            dataModel.location = row[7]
            results.append(dataModel)
        return results

    def deleteAllResumes(self):
        self.sqliteDb.deleteAllResumes()

    def dropResumeTables(self):
        self.sqliteDb.dropResumeTables()

    def fetchResumeDetailsFromId(self, resume_id: int) -> ResumeDataModel:
        row_main = self.sqliteDb.fetchAllDataFromMainWithId(resume_id=resume_id) 
        row_certifications = self.sqliteDb.fetchCertifications(resume_id=resume_id)
        row_projects = self.sqliteDb.fetchProjects(resume_id=resume_id)
        row_education = self.sqliteDb.fetchEducations(resume_id=resume_id)
        row_companies = self.sqliteDb.fetchCompanies(resume_id=resume_id)
        row_skills = self.sqliteDb.fetchSkills(resume_id=resume_id)
        
        dataModel: ResumeDataModel = ResumeDataModel()
        for row in row_main:
            dataModel.id = resume_id
            dataModel.name = row[1]
            dataModel.email = row[2]
            dataModel.phone = row[3]
            dataModel.currentRole = row[4]
            dataModel.summary = row[5]
            dataModel.totalExperience = row[6]
            dataModel.location = row[7]
            dataModel.domainExpertise = json.loads(row[8])
            
        certifications = []
        for row in row_certifications:
            certifications.append(row)
        dataModel.certifications = certifications

        projects = []
        for row in row_projects:
            print(row)
            projects.append(row)
        dataModel.projects = projects

        education = []
        for row in row_education:
            education.append(row)
        dataModel.education = education

        companies = []
        for row in row_companies:
            companies.append(row)
        dataModel.companiesWorked = companies

        skills = []
        for row in row_skills:
            skills.append(row)
        dataModel.skills = skills

        return dataModel
  
    def getFileExtension(self, name):
        suffix = ".pdf" if name.lower().endswith(".pdf") else "docx" if name.lower().endswith(".docx") else ".txt"
        return suffix

    def upload(self, upload_files):
        if upload_files:
            total = len(upload_files)
            progress_bar = st.progress(0)
            status = st.empty()
            for i, file in enumerate(upload_files):
                status.info(f"Uploading {i+1}/{total} files...")
                with tempfile.NamedTemporaryFile(delete=False, 
                                                     suffix=self.getFileExtension(file.name)) as tmp:
                    tmp.write(file.read())
                    self.file_path.append(tmp.name)
                    if not os.path.exists(tmp.name):
                        status.warning(f"File Size: {os.path.getsize(tmp.name)} bytes")
                    progress_bar.progress(10)
                    resume_text = load_text_from_file(tmp.name, size=300)
                    progress_bar.progress(25)
                    if not resume_text:
                        status.warning(f"Unable to extract text from {file.name}. Please check the file format.")
                        progress_bar.empty()
                        continue
                    structured_output_resume: ResumeSchema = parse_resume(resume_text)
                    progress_bar.progress(50)
                    self.sqliteDb.begin()
                    resume_id = self.sqliteDb.insert_resume(structured_output_resume)
                    if resume_id == DBConstants.EMAIL_ERROR:
                        status.error(f"Email - {structured_output_resume.email} already exists!!")
                        self.sqliteDb.rollback()
                    elif resume_id == DBConstants.PHONE_ERROR:
                        status.error(f"Duplicate Phone of {structured_output_resume.name} found!!")
                        self.sqliteDb.rollback()
                    elif resume_id == DBConstants.OTHER_ERROR:
                        status.error("Oops! Some error occurred while inserting.")
                        self.sqliteDb.rollback()
                    else:
                        try:
                            progress_bar.progress(60)
                            self.sqliteDb.insert_list_data(table_name= DBTables.CERTIFICATIONS, column_name= DBColumns.CERTIFICATION_NAME, resume_id= resume_id, values= structured_output_resume.certifications)
                            self.sqliteDb.insert_list_data(table_name= DBTables.SKILLS, column_name= DBColumns.SKILL, resume_id= resume_id, values= structured_output_resume.skills)
                            self.sqliteDb.insert_list_data(table_name= DBTables.COMPANIES_WORKED, column_name= DBColumns.COMPANY_NAME, resume_id= resume_id, values= structured_output_resume.companies_worked)                                
                            self.sqliteDb.insert_list_data(table_name= DBTables.PROJECTS, column_name= DBColumns.PROJECT_NAME, resume_id= resume_id, values= structured_output_resume.projects)
                            self.sqliteDb.insert_list_data(table_name= DBTables.EDUCATION, column_name= DBColumns.QUALIFICATION, resume_id= resume_id, values= structured_output_resume.education)
                            progress_bar.progress(80)
                            if add_resume_vector_store(structured_output_resume, resume_id):
                                status.success(f"Resumes uploaded successfully.")
                                self.sqliteDb.commit()
                                progress_bar.progress(100)
                            else:
                                self.sqliteDb.rollback()
                                status.warning(f"Email ({structured_output_resume.email}) of {structured_output_resume.name} already exists.")
                        except Exception as ex:
                            status.error(f"Error occurred {ex}")
                            self.sqliteDb.rollback()                
            progress_bar.empty()
            self.file_path.clear()
        else:
            st.warning("Please upload at least one resume.")

            
                                                
            

