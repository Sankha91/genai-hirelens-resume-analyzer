from pydantic import BaseModel, Field
from typing import List


class ResumeSchema(BaseModel):

    name: str = Field(description="Candidate full name.")

    email: str = Field(description="Candidate email address.")

    phone: str = Field(description="Candidate phone number.")

    current_location: str = Field(default=None, description="Candidate current location")

    current_role: str = Field(default=None,
        description="Most recent or current job title."
    )

    total_experience_years: float = Field(default=0.0,
        description="Total years of professional experience."
    )

    skills: List[str] = Field(
        description="List of technical and professional skills."
    )

    education: List[str] = Field(default=None,
        description="List of educational qualifications."
    )

    projects: List[str] = Field(
        description="List of professional projects the candidate has worked on."
    )

    certifications: List[str] = Field(default=None,
        description="List of professional certifications."
    )

    companies_worked: List[str] = Field(
        description="List of organizations where the candidate has worked."
    )

    domain_expertise: List[str] = Field(default=None,
        description="""
        List of domains or industries where the candidate has expertise.
        """
    )

    summary: str = Field(default=None,
        description="""
        A concise professional summary of the candidate
        highlighting skills, experience, and expertise.
        """
    )