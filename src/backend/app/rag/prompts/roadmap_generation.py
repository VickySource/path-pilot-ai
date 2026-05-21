ROADMAP_GENERATION_PROMPT = """Given the candidate's goal and the identified skill gaps,
generate a step-by-step personalized learning roadmap as JSON. Each step must include
title, description, estimated_hours, and recommended resources.

GOAL:
{goal}

GAPS:
{gaps}

CONTEXT:
{context}
"""
