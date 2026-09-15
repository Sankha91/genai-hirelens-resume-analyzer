from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model='gemini-3.1-flash-lite-preview', temperature = 0.7)
prompt = PromptTemplate(template="Write a summary of the following document: {doc}",
                        input_variables=["doc"])
outputParser = StrOutputParser()

input = input(f"Choose (type 1 or 2):\n1. .txt \n2. .pdf\n")
if input == "1":
    loader = TextLoader("Improvement_for_DM_app_Sankha.txt", encoding="utf-8")
else: #Split the pdf like: [Document(page_1), Document(page_2),...]
    loader = PyPDFLoader("dummy_bluetooth_troubleshooting_guide.pdf")
document = loader.load()

#chain = prompt | model | outputParser
#result = chain.invoke({"doc": document[0].page_content})

print(document[0].page_content)
print(document[0].metadata)

#print(f"Summary: {result}")