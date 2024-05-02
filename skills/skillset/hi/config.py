from dataclasses import dataclass

@dataclass
class SkillConfig:
    registered: bool = True
    pypath: str = "skills.skillset.hi"
    version: str = "0.0.1"