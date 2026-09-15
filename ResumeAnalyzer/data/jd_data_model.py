from dataclasses import dataclass, field

@dataclass
class JDDataModel:
    title: str = ""
    minExperience: str = ""
    location: str = ""
    responsibility: list[str] = field(default_factory=list)
    summary: str = ""
    uploadedOn: str = ""
    mandatorySkills: list[str] = field(default_factory=list)
    preferredSkills: list[str] = field(default_factory=list)
    jobType: str = ""
    id: int = 0
    totalMatchingResumes: int = 0