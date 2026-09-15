from pydantic import BaseModel, Field
from typing import List

class ResultSchema(BaseModel):

    resume_id: int = Field(description="Resume id of the respective candidate")

    job_des_id: int = Field(description="Job description id")

    match_score: float = Field(description="Overall match score of resume with respect to the job description")

    weakness: str = Field(default=None, description="Describe only technical gaps or missing qualifications.")

    strengths: str = Field(default=None,
        description="""Candidate's technical strengths with respect to the JD.
        """
    )

    recommendation: str = Field(default=None,
        description="""
        Provide a recommendation whether this resume can be selected for interview or not.
        Explaining why reason in 2 or 3 lines.
        """
    )

    missing_skills: List[str] = Field(default=None,
        description="List of technical and professional skills NOT matching with the Job Description."
    )

    matched_skills: List[str] = Field(default=None,
        description="List of technical and professional skills matching with the Job Description."
    )

class ResultListSchema(BaseModel):
    result: List[ResultSchema] = Field(description="Evaluation for every resume provided.")
