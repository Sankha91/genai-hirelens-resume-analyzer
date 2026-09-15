import streamlit as st
from sqlite3_database.db_tables import DBTables
from sqlite3_database.db_columns import DBColumns
from sqlite3_database.db_constants import DBConstants
from sqlite3_database.db_resume import SqliteDbResume
from sqlite3_database.db_result import SqliteDbResult
from sqlite3_database.db_jd import SqliteDbJD
from repository.result.result_repo import ResultRepository
from repository.resumes.resumes_repo import ResumeRepository
from parsers.schema.result_schema import ResultListSchema
from loaders.document_loader import load_text_from_file
from parsers.document_parsers import parse_resume
from embedding.vector_store import query
from parsers.schema.job_description_schema import JDSchema
from data.jd_data_model import JDDataModel
import json
from parsers.document_parsers import parse_jd, jd_evaluation_format, jd_raw_text, parse_result, summarize_jd_input

class JDRepository:

    def __init__(self, resumeRepo: ResumeRepository, sqliteDbJd: SqliteDbJD, resultRepo: ResultRepository):
        self.resumeRepo = resumeRepo
        self.sqliteDbJd = sqliteDbJd
        self.resultRepo = resultRepo

    def fetchTotalCount(self) -> int:
        return self.sqliteDbJd.fetchTotalCount()

    def deleteAllJDs(self) -> None:
        self.sqliteDbJd.deleteAllJDs()

    def dropJDTables(self) -> None:
        self.sqliteDbJd.dropJDTables()

    def fetchAllJDDetailsMain(self) -> list[JDDataModel]:
        rows = self.sqliteDbJd.fetchJDDetailsMain()
        resultList = []
        for row in rows:
            locationList = self.getFormattedList(self.sqliteDbJd.fetchLocations(row[0]))
            totalMatchingResumes = str(self.resultRepo.findMatchingResumesCount(row[0]))
            preferredSkills = self.sqliteDbJd.fetchPreferredSkills(row[0])
            mandatorySkills = self.sqliteDbJd.fetchMandatorySkills(row[0])
            resultList.append(JDDataModel(id=row[0], title= row[1], minExperience= row[2], location= f"{locationList}", 
                                          responsibility=json.loads(row[3]) , summary= row[4], jobType= row[5], uploadedOn= row[6], 
                                          mandatorySkills= [item[0] for item in mandatorySkills], preferredSkills= [item[0] for item in preferredSkills], 
                                          totalMatchingResumes= totalMatchingResumes))
        return resultList

    def fetchJDDetailsFromId(self, jd_id: int) -> JDDataModel:
        row = self.sqliteDbJd.fetchJDDetailsMainFromId(jd_id)
        locationList = self.getFormattedList(self.sqliteDbJd.fetchLocations(row[0]))
        totalMatchingResumes = str(self.resultRepo.findMatchingResumesCount(row[0]))
        preferredSkills = self.sqliteDbJd.fetchPreferredSkills(row[0])
        mandatorySkills = self.sqliteDbJd.fetchMandatorySkills(row[0])
        return JDDataModel(id=row[0], title= row[1], minExperience= row[2], location= f"{locationList}", 
                                    responsibility=json.loads(row[3]) , summary= row[4], jobType= row[5], uploadedOn= row[6], 
                                    mandatorySkills= [item[0] for item in mandatorySkills], preferredSkills= [item[0] for item in preferredSkills], 
                                    totalMatchingResumes= totalMatchingResumes)

    def getFormattedList(self, items) -> str:
        if not items:
            return "Not Specified"
        return ", ".join(item[0] for item in items)

    def getSelectedJDModelFromList(self, jdId: int, modelList: list[JDDataModel]) -> JDDataModel:
        for data in modelList:
            if data.id == jdId:
                return data
            
    def sortBy(self, data_model_list: list[JDDataModel], sort_by: str, order: str, sort_array: list[str], order_array: list[str]) -> None:
        reverse_order = True if order == order_array[0] else False
        if sort_by == sort_array[0]:
            data_model_list.sort(key=lambda x: x.minExperience, reverse=reverse_order)
        elif sort_by == sort_array[1]:
            data_model_list.sort(key=lambda x: int(x.totalMatchingResumes), reverse=reverse_order)
        
    def upload(self, jd_input):
        if jd_input:
            progress_bar = st.progress(0)
            status = st.empty()
            jd_summary = summarize_jd_input(raw_text=jd_input)
            jd_schema: JDSchema = parse_jd(jd_summary)
            jd_embedding_text = jd_raw_text(jd=jd_schema)
            jd_id = self.sqliteDbJd.insert_jd(jd_schema, jd_summary)
            progress_bar.progress(10)
            if jd_id == DBConstants.OTHER_ERROR:
                status.error("Oops! Some error occurred while saving JD.")
                self.sqliteDbJd.rollback()
                return
            else:
                try:
                    self.sqliteDbJd.insert_jd_list_data(table_name= DBTables.JD_PREFERRED_SKILLS,
                                                       column_name=DBColumns.SKILL, jd_id= jd_id, values=jd_schema.preferred_skills)
                    self.sqliteDbJd.insert_jd_list_data(table_name= DBTables.JD_REQUIRED_SKILLS,
                                                       column_name=DBColumns.SKILL, jd_id= jd_id, values=jd_schema.required_skills)
                    self.sqliteDbJd.insert_jd_list_data(table_name= DBTables.JD_LOCATION,
                                                       column_name=DBColumns.LOCATION, jd_id= jd_id, values=jd_schema.location)
                    self.sqliteDbJd.commit()
                    status.success(f"Job Description saved successfully!")
                except Exception as ex:
                    self.sqliteDbJd.rollback()
                    status.error(f"Error: {ex}")
                    st.stop()
            progress_bar.progress(30)
            print(f"JD experience: {jd_schema.minimum_experience_years}!")
            resume_ids: list[int] = self.resumeRepo.fetchJDCandidatesData(jd_schema.minimum_experience_years)
            if not resume_ids:
                status.warning(f"No matching resumes found!")
                progress_bar.empty()
                return
            progress_bar.progress(50)
            # Query fetched resume ids based on experience from vector store to find the match.
            document_with_score = query(query_text=jd_embedding_text, resume_ids=resume_ids)
            matched_resume_ids = []
            for doc, score in document_with_score:
                print(f"Score: {score}")
                if score <= 0.6:
                    matched_resume_ids.append(doc.metadata.get("resume_id"))
                else:
                    status.warning("No resumes found with proper match!")
                    progress_bar.empty()
                    continue
            progress_bar.progress(70)
            resume_sections = []
            for id in matched_resume_ids:
                resume_sections.append(self.getMergedResumeText(id))
            all_resumes_text = "\n\n----------------------------\n\n".join(resume_sections)
            status.info("Saving matching resumes...")
            progress_bar.progress(90)
            jd_text = f"""
            Job Description Id {jd_id}:
            {jd_evaluation_format(jd=jd_schema)}
            """
            result_list_schema: ResultListSchema = parse_result(jd_text=jd_text, all_resumes_text=all_resumes_text)
            try:
                self.resultRepo.dbResult.insertResult(result_list_schema.result)
                self.resultRepo.dbResult.commit()
                status.success(f"Matching Resumes saved successfully!")
                progress_bar.progress(100)
            except Exception as ex:
                self.resultRepo.dbResult.rollback()
                progress_bar.empty()
                status.error(f"Some error occurred while saving matching resumes: {ex}")
        else:
            st.warning("Please enter Job Description details.")

    def getMergedResumeText(self, id) -> str:
        skills = self.resumeRepo.sqliteDb.fetchSkills(id)
        certifications = self.resumeRepo.sqliteDb.fetchCertifications(id)
        projects = self.resumeRepo.sqliteDb.fetchProjects(id)
        summary = self.resumeRepo.sqliteDb.fetchSummary(id)
        exp = self.resumeRepo.sqliteDb.fetchExperience(id)
        location = self.resumeRepo.sqliteDb.fetchLocation(id)
        merged_resume_text = f"""
        For Resume Id {id}:
        Location: {location}
        Skills: {', '.join(skills) if skills else "None"} 
        Certifications: {', '.join(certifications) if certifications else "None"} 
        Projects: {', '.join(projects) if projects else "Not mentioned"}
        Candidate Summary: {summary}
        Years of experience: {exp} years 
        """
        return merged_resume_text

    def reAnalyseResumes(self, jd_id: int):
        jd_model: JDDataModel = self.fetchJDDetailsFromId(jd_id)
        if not jd_model:
            st.warning(f"Job Description not found!")
            return
        jd_embedding_text = jd_raw_text(jd_model=jd_model)
        resume_ids: list[int] = self.resumeRepo.fetchJDCandidatesData(jd_model.minExperience)
        already_matched_resume_ids: list[int] = self.resultRepo.fetchMatchedResumeIds(jd_id)
        resume_ids = [rid for rid in resume_ids if rid not in already_matched_resume_ids]
        if not resume_ids:
            st.warning("No new resumes found to analyse!")
            return
        # Query fetched resume ids based on experience from vector store to find the match.
        document_with_score = query(query_text=jd_embedding_text, resume_ids=resume_ids)
        matched_resume_ids = []
        for doc, score in document_with_score:
            if score <= 0.6:
                matched_resume_ids.append(doc.metadata.get("resume_id"))
            else:
                st.warning("No resumes found with proper match!")
                continue
        resume_sections = []
        for id in matched_resume_ids:
            resume_sections.append(self.getMergedResumeText(id))
        all_resumes_text = "\n\n----------------------------\n\n".join(resume_sections)
        jd_text = f"""
        Job Description Id {jd_id}:
        {jd_evaluation_format(jd_model=jd_model)}
        """
        result_list_schema: ResultListSchema = parse_result(jd_text=jd_text, all_resumes_text=all_resumes_text)
        try:
            self.resultRepo.dbResult.insertResult(result_list_schema.result)
            self.resultRepo.dbResult.commit()
            print(f"Matching Resumes re-analysed and saved successfully!")
        except Exception as ex:
            self.resultRepo.dbResult.rollback()
            print(f"Some error occurred while saving matching resumes: {ex}")
        

