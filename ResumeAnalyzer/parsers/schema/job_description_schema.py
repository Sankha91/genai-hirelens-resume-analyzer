from pydantic import BaseModel, Field
from typing import List

class JDSchema(BaseModel):

    role: str = Field(
        description="Job title or role."
    )

    job_type: str = Field(default=None,
        description="Job type like full-time/contract/part-time."
    )

    required_skills: List[str] = Field(default=None,
        description="Mandatory skills."
    )

    preferred_skills: List[str] = Field(default=None,
        description="Optional skills."
    )

    minimum_experience_years: float = Field(default=0.0,
        description="Minimum years of experience required."
    )

    responsibilities: List[str] = Field(default=None,
        description="Key responsibilities."
    )

    location: List[str] = Field(default=None,
        description="Hiring locations"
    )