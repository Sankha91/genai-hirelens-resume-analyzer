from dataclasses import dataclass, field

@dataclass
class ResultDataModel:
    matchingSkills: list[str] = field(default_factory=list)
    missingSkills: list[str] = field(default_factory=list)
    matchPercent: int = 0
    recommendation: str = ""
    strengths: str = ""
    weakness: str = ""
    jdId: int = -1
    resumeId: int = -1
