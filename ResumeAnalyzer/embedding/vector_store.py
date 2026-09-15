from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from parsers.document_parsers import resume_embedding_format
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

vector_store_resume = Chroma(embedding_function=GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview"),
                            persist_directory="resume_vector_store",
                            collection_name="resume_analyser_langchain")

def reset_vector_store():
        vector_store_resume.reset_collection()
        
def add_resume_vector_store(structured_output, resume_id):
        try:
                alreadyExists = vector_store_resume.get(ids=[str(resume_id)])
                if alreadyExists["ids"]:
                        return False
                else:
                        doc = Document(page_content=resume_embedding_format(structured_output), 
                                metadata= {"resume_id": resume_id, "email": structured_output.email})
                        vector_store_resume.add_documents(documents=[doc], ids=[str(resume_id)])
                        return True
        except Exception as ex:
                st.error(f"Error: {ex}")

def query(query_text, resume_ids):
        count = min(5, vector_store_resume._collection.count())
        result_with_score = vector_store_resume.similarity_search_with_score(query=query_text, k=count, filter={
                "resume_id": {"$in": resume_ids}
        })
        return result_with_score

def fetchAllData():
        ids = vector_store_resume.get()["ids"]
        st.write(f"Vector Store ids: {ids}")