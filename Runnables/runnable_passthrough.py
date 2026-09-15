from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnableSequence, RunnableParallel, RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

prompt_1 = PromptTemplate(template="Write me a joke about {topic}", 
                          input_variables=["topic"])
llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite-preview")
parser = StrOutputParser()

joke_generator = RunnableSequence(prompt_1, llm, parser)

prompt_2 = PromptTemplate(template="Explain me the joke {joke} in short", input_variables=["joke"])

joke_explanation = RunnableParallel({"joke": RunnablePassthrough(), 
                                "explanation": RunnableSequence(prompt_2, llm, parser)})

final_chain = RunnableSequence(joke_generator, joke_explanation)
result = final_chain.invoke({"topic": "LLM"})
print(result)