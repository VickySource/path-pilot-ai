from datetime import datetime
from pydantic import BaseModel

from app.models.skill import Skill


class Resource(BaseModel):
    title: str
    url: str


class RoadmapStep(BaseModel):
    id: str
    title: str
    description: str
    estimatedHours: int
    resources: list[Resource] = []
    skills: list[Skill] = []


class Roadmap(BaseModel):
    id: str
    userId: str
    goal: str
    steps: list[RoadmapStep]
    createdAt: datetime
