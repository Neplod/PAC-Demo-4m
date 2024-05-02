from dataclasses import dataclass

@dataclass
class SkillConfig:
    registered: bool = True
    pypath: str = "skills.skillset.bread"
    version: str = "0.0.1"