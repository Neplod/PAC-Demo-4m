from dataclasses import dataclass

@dataclass
class SkillConfig:
    registered: bool = False
    pypath: str = "skill.skillset.{SKILLNAME}.skill"
    version: str = "0.0.1"