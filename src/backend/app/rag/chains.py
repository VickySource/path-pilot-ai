from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.llm.factory import get_chat_runnable
from app.rag.prompts.gap_analysis import GAP_ANALYSIS_PROMPT
from app.rag.prompts.roadmap_generation import ROADMAP_GENERATION_PROMPT
from app.rag.prompts.skills_extraction import SKILLS_EXTRACTION_PROMPT


def skills_extraction_chain():
    prompt = ChatPromptTemplate.from_template(SKILLS_EXTRACTION_PROMPT)
    return prompt | get_chat_runnable() | StrOutputParser()


def gap_analysis_chain():
    prompt = ChatPromptTemplate.from_template(GAP_ANALYSIS_PROMPT)
    return prompt | get_chat_runnable() | StrOutputParser()


def roadmap_generation_chain():
    prompt = ChatPromptTemplate.from_template(ROADMAP_GENERATION_PROMPT)
    return prompt | get_chat_runnable() | StrOutputParser()
