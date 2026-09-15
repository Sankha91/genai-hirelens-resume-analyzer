from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnableSequence, RunnableParallel
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

prompt_1 = PromptTemplate(template="Write me a short linkedin post about {topic} in short", 
                          input_variables=["topic"])
prompt_2 = PromptTemplate(template="Write me a twitter post on {topic} in short", 
                          input_variables=["topic"])
llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite-preview")
parser = StrOutputParser()

chain = RunnableParallel({"tweet":RunnableSequence(prompt_1, llm, parser),
                          "linkedin": RunnableSequence(prompt_2, llm, parser)})
result_dictionary = chain.invoke({"topic": "Langchain"})

print("***** Tweet *****\n")
print(result_dictionary["tweet"])
print("\n***** Linkedin post *****\n")
print(result_dictionary["linkedin"])
