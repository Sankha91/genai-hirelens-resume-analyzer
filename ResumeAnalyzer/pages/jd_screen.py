import streamlit as st
import tempfile
from embedding.vector_store import query
from parsers.schema.result_schema import ResultListSchema
from sqlite3_database.db_resume import SqliteDbResume
from sqlite3_database.db_jd import SqliteDbJD
from sqlite3_database.db_result import SqliteDbResult
from sqlite3_database.db_constants import DBConstants
from sqlite3_database.db_tables import DBTables
from sqlite3_database.db_columns import DBColumns
from loaders.document_loader import load_text_from_file
from parsers.document_parsers import parse_jd, jd_evaluation_format, jd_raw_text, parse_result

jd_input = st.text_area(
    "Paste Job Description",
     height=300
)
st.text = "OR"
uploaded_file = st.file_uploader(label="Upload JD in .pdf or .txt or .docx files", type=["pdf", "txt"], 
                                      accept_multiple_files=False)
file_path = ""

sqliteDbResume = SqliteDbResume(st.session_state.db)
sqliteDbJd = SqliteDbJD(st.session_state.db)
sqliteDbResult = SqliteDbResult(st.session_state.db)

def getFileExtension(name):
    suffix = ".pdf" if name.lower().endswith(".pdf") else "docx" if name.lower().endswith(".docx") else ".txt"
    return suffix

if st.button("Upload Job Description"):
    sqliteDbJd.createAllTables()
    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=getFileExtension(uploaded_file.name)) as temp:
            temp.write(uploaded_file.read())
            file_path = temp.name
            jd_text = load_text_from_file(file_path, chunk_size=100)
            st.session_state.jd_schema = parse_jd(jd_text)
            st.session_state.jd_embedding_text = jd_raw_text(st.session_state.jd_schema)
    elif jd_input:
        st.session_state.jd_schema = parse_jd(jd_input)
        st.session_state.jd_embedding_text = jd_raw_text(st.session_state.jd_schema)
    jd_id = sqliteDbJd.insert_jd(st.session_state.jd_schema, st.session_state.jd_embedding_text)
    if jd_id == DBConstants.OTHER_ERROR:
        st.error("Oops! Some error occurred while inserting.")
    else:
        try:
            sqliteDbJd.insert_jd_list_data(table_name= DBTables.JD_PREFERRED_SKILLS,
                                           column_name=DBColumns.SKILL, jd_id= jd_id, values=st.session_state.jd_schema.preferred_skills)
            sqliteDbJd.insert_jd_list_data(table_name= DBTables.JD_REQUIRED_SKILLS,
                                           column_name=DBColumns.SKILL, jd_id= jd_id, values=st.session_state.jd_schema.required_skills)
            sqliteDbJd.insert_jd_list_data(table_name= DBTables.JD_LOCATION,
                                           column_name=DBColumns.LOCATION, jd_id= jd_id, values=st.session_state.jd_schema.location)
            sqliteDbJd.conn.commit()
            st.write(f"JD id {jd_id} inserted successfully!")
        except Exception as ex:
            sqliteDbJd.conn.rollback()
            st.error(f"Error: {ex}")
            st.stop()

if st.button("Analyze Candidates"):
    sqliteDbResult.createAllTables()
    resume_ids = sqliteDbResume.fetchJDCandidatesData(st.session_state.jd_schema.minimum_experience_years)
    if not resume_ids:
        st.warning("No match found!")
        st.stop()
    document_with_score = query(query_text=st.session_state.jd_embedding_text, resume_ids=resume_ids)
    matched_resume_ids = []
    for doc, score in document_with_score:
        if score <= 0.6:
            matched_resume_ids.append(doc.metadata.get("resume_id"))
    st.write(f"Matched resume ids: {matched_resume_ids}")
    resume_sections = []
    for id in matched_resume_ids:
        skills = sqliteDbResume.fetchSkills(id)
        certifications = sqliteDbResume.fetchCertifications(id)
        projects = sqliteDbResume.fetchProjects(id)
        summary = sqliteDbResume.fetchSummary(id)
        exp = sqliteDbResume.fetchExperience(id)
        location = sqliteDbResume.fetchLocation(id)
        merged_resume_text = f"""
        For Resume Id {id}:
        Location: {location}
        Skills: {', '.join(skills) if skills else "None"} 
        Certifications: {', '.join(certifications) if certifications else "None"} 
        Projects: {', '.join(projects) if projects else "Not mentioned"}
        Candidate Summary: {summary}
        Years of experience: {exp} years 
        """
        resume_sections.append(merged_resume_text)

    all_resumes_text = "\n\n----------------------------\n\n".join(resume_sections)
    jd_id = sqliteDbJd.fetchLatestJdId()
    jd_text = f"""
    Job Description Id {jd_id}:
    {jd_evaluation_format(st.session_state.jd_schema)}
    """
    st.write(f"{jd_text} \n\n {all_resumes_text}")
    result_list_schema: ResultListSchema = parse_result(jd_text=jd_text, all_resumes_text=all_resumes_text)
    sqliteDbResult.insertResult(result_list_schema.result)
    sqliteDbResult.conn.commit()
    sqliteDbResult.fetchAllResults()


if st.button("DELETE all JD Datas"):
    sqliteDbJd.deleteAll()
    sqliteDbResult.deleteAll()
    st.success("Deleted all tables of JD and Result.")

if st.button("View JD"):
    try:
        sqliteDbJd.fetchAllData()
    except Exception as ex:
        st.error(ex)
