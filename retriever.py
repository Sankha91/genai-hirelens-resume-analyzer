from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_classic.retrievers.multi_query import MultiQueryRetriever
from langchain_classic.retrievers import ContextualCompressionRetriever
from langchain_classic.retrievers.document_compressors import LLMChainExtractor
from dotenv import load_dotenv

load_dotenv()

doc1 = Document(
    page_content="Artificial Intelligence enables machines to learn from data and make decisions without explicit programming.",
    metadata={"topic": "AI Basics"}
)

doc2 = Document(
    page_content="Machine learning is a subset of AI that focuses on training algorithms using data to improve performance over time.",
    metadata={"topic": "Machine Learning"}
)

doc3 = Document( page_content="Deep learning uses neural networks with multiple layers to model complex patterns in large datasets.", metadata={"topic": "Deep Learning"} ) 

doc4 = Document( page_content="Natural Language Processing allows computers to understand, interpret, and generate human language.",    metadata={"topic": "NLP"} ) 

doc5 = Document( page_content="Computer vision enables machines to analyze and interpret visual information from images and videos.", metadata={"topic": "Computer Vision"} )

document = [doc1, doc2, doc3, doc4, doc5]
ids = ["123", "345", "567", "789","901"]

for doc, id in zip(document, ids):
    vector_store = Chroma.from_documents(
        documents=[doc],
        ids=id,
        embedding=GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview"),
        persist_directory="my_test_chroma_db",
        collection_name="sample"
    )

#for doc,id in zip(document, ids):
#    vector_store.add_documents(documents=[doc], ids=[id])

print(f"vector store: {vector_store._collection.count()}")

# General Query
retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 2, "lambda_mult": 0.5})
result = retriever.invoke("What is machine learning and AI?")
for i, doc in enumerate(result):
    print(f"\nAnswer {i+1}: {doc.page_content}")

print("\n----- Multi query retriever -----\n")
llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite-preview")
multi_query_retriever = MultiQueryRetriever.from_llm(retriever=retriever, llm=llm)
result = multi_query_retriever.invoke("What is machine learning and AI?")
for i, doc in enumerate(result):
    print(f"\nAnswer {i+1}: {doc.page_content}")

print("\n ----- Contextual Compression Retriever ----- \n")
compressor = LLMChainExtractor.from_llm(llm=llm)
compression_retriever = ContextualCompressionRetriever(base_retriever= retriever, base_compressor=compressor)
result = compression_retriever.invoke("What is machine learning and AI?")
for i, doc in enumerate(result):
    print(f"\nAnswer {i+1}: {doc.page_content}")




