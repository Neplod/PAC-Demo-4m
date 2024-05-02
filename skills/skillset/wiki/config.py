from dataclasses import dataclass

@dataclass
class SkillConfig:
    registered: bool = False
    pypath: str = "skills.skillset.wiki"
    version: str = "0.0.1"