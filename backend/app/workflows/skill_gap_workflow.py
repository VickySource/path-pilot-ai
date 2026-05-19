"""
LangGraph Skill Gap Analysis Workflow
--------------------------------------
A dedicated graph for analysing the gap between a user's current skills
and the skills required for a target role.

Nodes:
  skill_extraction → gap_analysis → recommendation_generation → roadmap_generation

The LLM is used to:
  1. Identify required skills for the target role
  2. Analyse which skills are missing
  3. Recommend courses and projects
  4. Build a step-by-step learning roadmap
"""

import json
import logging
import re
from typing import TypedDict, List, Optional

from langgraph.graph import StateGraph, END

from app.services.ollama_service import get_ollama_service

logger = logging.getLogger(__name__)


# ── Shared state ──────────────────────────────────────────────────────────────

class SkillGapState(TypedDict):
    """State that flows through the skill gap analysis workflow."""
    # Input
    current_skills: List[str]
    target_role: str

    # Set by skill_extraction node
    required_skills: List[str]

    # Set by gap_analysis node
    missing_skills: List[str]
    matching_skills: List[str]
    gap_percentage: float

    # Set by recommendation_generation node
    courses: List[dict]
    projects: List[dict]

    # Set by roadmap_generation node
    roadmap: List[dict]
    summary: str

    # Error tracking
    error: Optional[str]


# ── Helper: safe JSON extraction ──────────────────────────────────────────────

def _extract_json(text: str) -> any:
    """
    Extract the first JSON object or array from a string.
    The LLM sometimes wraps JSON in markdown code fences — this strips them.
    """
    # Remove markdown code fences
    text = re.sub(r"```(?:json)?", "", text).strip()
    # Find the first { or [ and the matching closing bracket
    for start_char, end_char in [("{", "}"), ("[", "]")]:
        start = text.find(start_char)
        if start != -1:
            # Find the last occurrence of the closing bracket
            end = text.rfind(end_char)
            if end != -1:
                try:
                    return json.loads(text[start : end + 1])
                except json.JSONDecodeError:
                    pass
    return None


# ── Node implementations ──────────────────────────────────────────────────────

async def skill_extraction_node(state: SkillGapState) -> SkillGapState:
    """
    Node 1 — Skill Extraction
    Ask the LLM to list the skills typically required for the target role.
    """
    logger.info(f"[SkillGap: skill_extraction] Role: '{state['target_role']}'")
    ollama = get_ollama_service()

    prompt = f"""List the top 15 technical and soft skills required for a "{state['target_role']}" role.
Return ONLY a JSON array of skill strings. Example: ["Python", "SQL", "Communication"]
Do not include any explanation, just the JSON array."""

    try:
        response = await ollama.generate(prompt=prompt, temperature=0.3)
        skills = _extract_json(response)
        if not isinstance(skills, list):
            skills = []
        # Normalise to strings
        required_skills = [str(s).strip() for s in skills if s]
    except Exception as exc:
        logger.error(f"[SkillGap: skill_extraction] Error: {exc}")
        required_skills = []

    return {**state, "required_skills": required_skills}


async def gap_analysis_node(state: SkillGapState) -> SkillGapState:
    """
    Node 2 — Gap Analysis
    Compare current skills against required skills to find missing ones.
    Uses fuzzy matching via the LLM to handle synonyms (e.g. "JS" vs "JavaScript").
    """
    logger.info("[SkillGap: gap_analysis] Comparing skills")
    ollama = get_ollama_service()

    current = state["current_skills"]
    required = state["required_skills"]

    if not required:
        return {
            **state,
            "missing_skills": [],
            "matching_skills": current,
            "gap_percentage": 0.0,
        }

    prompt = f"""Given:
Current skills: {json.dumps(current)}
Required skills for "{state['target_role']}": {json.dumps(required)}

Identify which required skills the person is MISSING (considering synonyms and related technologies).
Return ONLY a JSON object with two keys:
  "missing": list of missing required skills
  "matching": list of required skills the person already has

Example: {{"missing": ["Docker", "Kubernetes"], "matching": ["Python", "SQL"]}}"""

    try:
        response = await ollama.generate(prompt=prompt, temperature=0.2)
        data = _extract_json(response)
        if isinstance(data, dict):
            missing = [str(s) for s in data.get("missing", [])]
            matching = [str(s) for s in data.get("matching", [])]
        else:
            # Fallback: simple string comparison
            current_lower = {s.lower() for s in current}
            missing = [s for s in required if s.lower() not in current_lower]
            matching = [s for s in required if s.lower() in current_lower]
    except Exception as exc:
        logger.error(f"[SkillGap: gap_analysis] Error: {exc}")
        current_lower = {s.lower() for s in current}
        missing = [s for s in required if s.lower() not in current_lower]
        matching = [s for s in required if s.lower() in current_lower]

    gap_pct = round((len(missing) / len(required)) * 100, 1) if required else 0.0

    return {
        **state,
        "missing_skills": missing,
        "matching_skills": matching,
        "gap_percentage": gap_pct,
    }


async def recommendation_generation_node(state: SkillGapState) -> SkillGapState:
    """
    Node 3 — Recommendation Generation
    Suggest specific courses and projects to fill the identified skill gaps.
    """
    logger.info("[SkillGap: recommendation_generation] Generating recommendations")
    ollama = get_ollama_service()

    missing = state["missing_skills"]
    role = state["target_role"]

    if not missing:
        return {**state, "courses": [], "projects": []}

    prompt = f"""A person wants to become a "{role}" and is missing these skills: {json.dumps(missing[:8])}.

Recommend:
1. 5 online courses (with platform, skill covered, duration, difficulty)
2. 3 hands-on projects (with description, skills practiced, difficulty)

Return ONLY a JSON object with this exact structure:
{{
  "courses": [
    {{
      "title": "Course Name",
      "platform": "Coursera/Udemy/YouTube/etc",
      "skill_covered": "Skill Name",
      "estimated_duration": "X weeks",
      "difficulty": "Beginner/Intermediate/Advanced"
    }}
  ],
  "projects": [
    {{
      "title": "Project Name",
      "description": "Brief description",
      "skills_practiced": ["skill1", "skill2"],
      "difficulty": "Beginner/Intermediate/Advanced"
    }}
  ]
}}"""

    try:
        response = await ollama.generate(prompt=prompt, temperature=0.5)
        data = _extract_json(response)
        if isinstance(data, dict):
            courses = data.get("courses", [])
            projects = data.get("projects", [])
        else:
            courses, projects = [], []
    except Exception as exc:
        logger.error(f"[SkillGap: recommendation_generation] Error: {exc}")
        courses, projects = [], []

    return {**state, "courses": courses, "projects": projects}


async def roadmap_generation_node(state: SkillGapState) -> SkillGapState:
    """
    Node 4 — Roadmap Generation
    Create a phased, week-by-week learning roadmap to reach the target role.
    """
    logger.info("[SkillGap: roadmap_generation] Building roadmap")
    ollama = get_ollama_service()

    role = state["target_role"]
    missing = state["missing_skills"]
    gap_pct = state["gap_percentage"]

    prompt = f"""Create a learning roadmap for someone who wants to become a "{role}".
They need to learn: {json.dumps(missing[:10])}
Current skill gap: {gap_pct}%

Build a 4-6 step roadmap. Return ONLY a JSON array:
[
  {{
    "step": 1,
    "title": "Phase Title",
    "description": "What to focus on",
    "duration": "X weeks",
    "skills": ["skill1", "skill2"]
  }}
]"""

    summary_prompt = f"""In 2-3 sentences, summarise the career transition plan for someone 
moving into a "{role}" role with a {gap_pct}% skill gap. 
Be encouraging and specific about the timeline."""

    try:
        roadmap_response = await ollama.generate(prompt=prompt, temperature=0.4)
        roadmap = _extract_json(roadmap_response)
        if not isinstance(roadmap, list):
            roadmap = []

        summary = await ollama.generate(prompt=summary_prompt, temperature=0.6)
    except Exception as exc:
        logger.error(f"[SkillGap: roadmap_generation] Error: {exc}")
        roadmap = []
        summary = f"Focus on acquiring the missing skills for the {role} role."

    return {**state, "roadmap": roadmap, "summary": summary.strip()}


# ── Graph assembly ────────────────────────────────────────────────────────────

def build_skill_gap_graph() -> StateGraph:
    """
    Assemble and compile the skill gap analysis LangGraph workflow.
    """
    graph = StateGraph(SkillGapState)

    graph.add_node("skill_extraction", skill_extraction_node)
    graph.add_node("gap_analysis", gap_analysis_node)
    graph.add_node("recommendation_generation", recommendation_generation_node)
    graph.add_node("roadmap_generation", roadmap_generation_node)

    graph.set_entry_point("skill_extraction")
    graph.add_edge("skill_extraction", "gap_analysis")
    graph.add_edge("gap_analysis", "recommendation_generation")
    graph.add_edge("recommendation_generation", "roadmap_generation")
    graph.add_edge("roadmap_generation", END)

    return graph.compile()


# ── Singleton ─────────────────────────────────────────────────────────────────

_skill_gap_graph = None


def get_skill_gap_graph():
    """Return the compiled skill gap LangGraph workflow (built once)."""
    global _skill_gap_graph
    if _skill_gap_graph is None:
        _skill_gap_graph = build_skill_gap_graph()
        logger.info("LangGraph Skill Gap workflow compiled successfully.")
    return _skill_gap_graph
