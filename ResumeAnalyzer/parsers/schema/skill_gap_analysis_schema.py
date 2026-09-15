from pydantic import BaseModel, Field
from typing import List

class SkillGapAnalysisSchema(BaseModel):
    skill_name: str = Field(description = "Name of the skill that is lacking or needs improvement")
    required_skill_level: str = Field(description = "The skill level required for the position: Advanced, Intermediate, or Beginner")
    candidate_skill_level: str = Field(description = "The skill level of the candidate: Advanced, Intermediate, or Beginner")
    gap_percent: int = Field(description = "The percentage representing the gap between required and candidate skill levels")
    status: str = Field(description = "The status of the skill gap: Missing, Partial, or Matched")

class SkillGapAnalysisListSchema(BaseModel):
    skillGaps: List[SkillGapAnalysisSchema] = Field(default=None, description="List of skill gaps and their analysis.")
    recommendation: str = Field(default=None, description="Overall recommendations to bridge the skill gaps and whether to proceed with the candidate or not.")