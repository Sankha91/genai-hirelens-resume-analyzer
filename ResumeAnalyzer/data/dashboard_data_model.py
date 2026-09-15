from dataclasses import dataclass, field

@dataclass
class DashboardDataModel:
    resume_id: int
    jd_id: int
    rank: str
    name: str
    experience: str
    matchPercent: str
    skills_matched: str