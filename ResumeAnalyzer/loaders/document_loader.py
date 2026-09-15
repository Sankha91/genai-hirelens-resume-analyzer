from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_text_from_file(file_path, size):
    document_generators = []
    documents = []
    resume_text = ""
    if file_path.lower().endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    elif file_path.lower().endswith(".docx"):
        loader = Docx2txtLoader(file_path)
    else:
        loader = TextLoader(file_path, encoding="utf-8")
    # lazy_load return Generator objects not Document object.
    document_generators.append(loader.lazy_load())
    for gen in document_generators:
        for doc in gen:
            documents.append(doc)
    splitter = RecursiveCharacterTextSplitter(chunk_size=size, chunk_overlap=0)
    document_chunks = []
    document_chunks.extend(splitter.split_documents(documents))
    for chunk in document_chunks:
        resume_text += chunk.page_content + "\n"
    return resume_text

    



    