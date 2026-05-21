from typing import Literal
from pydantic import BaseModel

SkillLevel = Literal["beginner", "intermediate", "advanced", "expert"]


class Skill(BaseModel):
    id: str
    name: str
    level: SkillLevel
    category: str | None = None


class SkillGap(BaseModel):
    skill: Skill
    targetLevel: SkillLevel
    priority: Literal["low", "medium", "high"]
