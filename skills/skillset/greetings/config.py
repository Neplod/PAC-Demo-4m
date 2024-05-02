from dataclasses import dataclass

@dataclass
class SkillConfig:
    registered: bool = True
    pypath: str = "skills.skillset.greetings"
    version: str = "0.0.1"