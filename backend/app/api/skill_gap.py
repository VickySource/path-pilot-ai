"""
Skill Gap Analysis Router — POST /skill-gap-analysis
------------------------------------------------------
Accepts a user's current skills and target role, then runs the
LangGraph skill gap workflow to produce:
  - Required skills for the role
  - Missing skills
  - Course recommendations
  - Project recommendations
  - Step-by-step learning roadmap
"""

import logging

from fastapi import APIRouter, HTTPException

from app.models.schemas import (
    SkillGapRequest,
    SkillGapResponse,
    CourseRecommendation,
    ProjectRecommendation,
    RoadmapStep,
)
from app.workflows.skill_gap_workflow import get_skill_gap_graph

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/skill-gap-analysis", tags=["Skill Gap"])


@router.post("", response_model=SkillGapResponse, summary="Analyse skill gap for a target role")
async def skill_gap_analysis(request: SkillGapRequest) -> SkillGapResponse:
    """
    Analyse the gap between current skills and a target role.

    Runs a 4-node LangGraph workflow:
    1. Extract required skills for the role
    2. Compare with current skills
    3. Recommend courses and projects
    4. Generate a learning roadmap

    - **current_skills**: List of skills the user already has
    - **target_role**: The job role they want to achieve
    """
    # Sanitise inputs
    current_skills = [s.strip() for s in request.current_skills if s.strip()]
    target_role = request.target_role.strip()

    if not current_skills:
        raise HTTPException(status_code=400, detail="current_skills cannot be empty.")
    if not target_role:
        raise HTTPException(status_code=400, detail="target_role cannot be empty.")

    try:
        graph = get_skill_gap_graph()

        # Initial state for the workflow
        initial_state = {
            "current_skills": current_skills,
            "target_role": target_role,
            "required_skills": [],
            "missing_skills": [],
            "matching_skills": [],
            "gap_percentage": 0.0,
            "courses": [],
            "projects": [],
            "roadmap": [],
            "summary": "",
            "error": None,
        }

        # Run the LangGraph workflow asynchronously
        final_state = await graph.ainvoke(initial_state)

        # Map raw dicts to Pydantic models (with safe defaults)
        courses = [
            CourseRecommendation(
                title=c.get("title", ""),
                platform=c.get("platform", ""),
                skill_covered=c.get("skill_covered", ""),
                estimated_duration=c.get("estimated_duration", ""),
                difficulty=c.get("difficulty", ""),
            )
            for c in final_state.get("courses", [])
            if isinstance(c, dict)
        ]

        projects = [
            ProjectRecommendation(
                title=p.get("title", ""),
                description=p.get("description", ""),
                skills_practiced=p.get("skills_practiced", []),
                difficulty=p.get("difficulty", ""),
            )
            for p in final_state.get("projects", [])
            if isinstance(p, dict)
        ]

        roadmap = [
            RoadmapStep(
                step=r.get("step", i + 1),
                title=r.get("title", ""),
                description=r.get("description", ""),
                duration=r.get("duration", ""),
                skills=r.get("skills", []),
            )
            for i, r in enumerate(final_state.get("roadmap", []))
            if isinstance(r, dict)
        ]

        return SkillGapResponse(
            target_role=target_role,
            current_skills=current_skills,
            required_skills=final_state.get("required_skills", []),
            missing_skills=final_state.get("missing_skills", []),
            matching_skills=final_state.get("matching_skills", []),
            gap_percentage=final_state.get("gap_percentage", 0.0),
            courses=courses,
            projects=projects,
            roadmap=roadmap,
            summary=final_state.get("summary", ""),
        )

    except Exception as exc:
        logger.error(f"Skill gap analysis failed: {exc}")
        raise HTTPException(
            status_code=500,
            detail=f"Skill gap analysis failed: {str(exc)}",
        )
