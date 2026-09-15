from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
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

vector_store = Chroma(
    embedding_function=GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview"),
    persist_directory="my_test_chroma_db",
    collection_name="sample"
)

document = [doc1, doc2, doc3, doc4, doc5]
ids = ["123", "345", "567", "789","901"]

for doc,id in zip(document, ids):
    vector_store.add_documents(documents=[doc], ids=[id])

print(f"vector store: {vector_store._collection.count()}")
print(vector_store.get(include=["documents","embeddings","metadatas"]))

# General Query
result = vector_store.similarity_search(query="What is machine learning?", k=2)
print(f"\nAnswer based on Query: {result[0].page_content}")

# meta-data filtering
result = vector_store.similarity_search_with_score(query="What is NLP?", filter={"topic": "NLP"}, k=1)
print(f"\nAnswer based on Metadata: {result}")

# update
#result = vector_store.update_document(document_id="123", document=Document(page_content="...", metadata={"topic": "AI", "version": "updated"}))


