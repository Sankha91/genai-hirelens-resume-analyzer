from dataclasses import dataclass, field

@dataclass
class ResumeDataModel:
    id: int = -1
    name: str = ""
    email: str = ""
    phone: str = ""
    location: str = ""
    currentRole: str = ""
    summary: str = ""
    totalExperience: str = ""
    isAnalyzed: bool = False
    domainExpertise: list[str] = field(default_factory=list)
    projects: list[str] = field(default_factory=list)
    education: list[str] = field(default_factory=list)
    certifications: list[str] = field(default_factory=list)
    companiesWorked: list[str] = field(default_factory=list)
    skills: list[str] = field(default_factory=list)
