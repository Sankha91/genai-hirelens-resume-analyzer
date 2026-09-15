from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_core.runnables import RunnableSequence

load_dotenv()

prompt_1 = PromptTemplate(template="Write me a joke about {topic}", input_variables=["topic"])
llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite-preview")
parser = StrOutputParser()
prompt_2 = PromptTemplate(template="First print me the joke then explain the following joke: {text} in short", input_variables=["text"])

chain = RunnableSequence(prompt_1, llm, parser, prompt_2, llm, parser)
result = chain.invoke({"topic": "AI"})
print(result)