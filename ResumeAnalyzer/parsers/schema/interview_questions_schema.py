from pydantic import BaseModel, Field
from typing import List

class InterviewQuestionSchema(BaseModel):
    difficulty: str = Field(description="Difficulty level of the interview question: Easy, Medium, or Hard")
    category: str = Field(description="Category of the interview question: Technical or Experience or Behavioral")
    question: str = Field(default=None, description="Interview question based on candidate's experience and skills")
    answer: str = Field(default=None, description="Expected answer or evaluation points for the given question")

class InterviewQuestionListSchema(BaseModel):
    qaList: List[InterviewQuestionSchema] = Field(default=None, description="List of interview questions and their expected answers.")