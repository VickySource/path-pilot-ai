"""
Pydantic schemas for all API request/response models.
These define the shape of data flowing in and out of every endpoint.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime


# ─────────────────────────────────────────────────────────────────────────────
# Document schemas
# ─────────────────────────────────────────────────────────────────────────────

class DocumentMetadata(BaseModel):
    """Metadata stored alongside each chunk in ChromaDB."""
    document_id: str
    source_file: str
    file_type: str
    chunk_index: int
    total_chunks: int
    uploaded_at: str


class DocumentInfo(BaseModel):
    """Summary info returned when listing stored documents."""
    document_id: str
    source_file: str
    file_type: str
    total_chunks: int
    uploaded_at: str


class UploadResponse(BaseModel):
    """Response returned after a successful document upload."""
    success: bool
    document_id: str
    filename: str
    total_chunks: int
    message: str


class DeleteResponse(BaseModel):
    """Response returned after deleting a document."""
    success: bool
    document_id: str
    message: str


# ─────────────────────────────────────────────────────────────────────────────
# Chat schemas
# ─────────────────────────────────────────────────────────────────────────────

class ChatMessage(BaseModel):
    """A single message in a conversation."""
    role: str = Field(..., description="'user' or 'assistant'")
    content: str


class ChatRequest(BaseModel):
    """Request body for the /chat endpoint."""
    query: str = Field(..., min_length=1, max_length=2000, description="User question")
    conversation_history: Optional[List[ChatMessage]] = Field(
        default=[], description="Previous messages for context"
    )
    document_id: Optional[str] = Field(
        default=None, description="Restrict retrieval to a specific document"
    )


class Source(BaseModel):
    """A source chunk used to generate the answer."""
    document_id: str
    source_file: str
    chunk_index: int
    content_preview: str  # first 200 chars of the chunk
    relevance_score: float


class ChatResponse(BaseModel):
    """Response returned from the /chat endpoint."""
    answer: str
    sources: List[Source]
    query: str
    model_used: str


# ─────────────────────────────────────────────────────────────────────────────
# Search schemas
# ─────────────────────────────────────────────────────────────────────────────

class SearchRequest(BaseModel):
    """Request body for the /search endpoint."""
    query: str = Field(..., min_length=1, max_length=1000)
    top_k: Optional[int] = Field(default=5, ge=1, le=20)
    score_threshold: Optional[float] = Field(default=0.3, ge=0.0, le=1.0)
    document_id: Optional[str] = Field(default=None)


class SearchResult(BaseModel):
    """A single semantic search result."""
    document_id: str
    source_file: str
    chunk_index: int
    content: str
    score: float
    metadata: dict


class SearchResponse(BaseModel):
    """Response returned from the /search endpoint."""
    query: str
    results: List[SearchResult]
    total_found: int


# ─────────────────────────────────────────────────────────────────────────────
# Skill gap analysis schemas
# ─────────────────────────────────────────────────────────────────────────────

class SkillGapRequest(BaseModel):
    """Request body for the /skill-gap-analysis endpoint."""
    current_skills: List[str] = Field(
        ..., min_length=1, description="Skills the user already has"
    )
    target_role: str = Field(
        ..., min_length=2, max_length=200, description="Job role the user wants"
    )


class CourseRecommendation(BaseModel):
    """A recommended course to fill a skill gap."""
    title: str
    platform: str
    skill_covered: str
    estimated_duration: str
    difficulty: str


class ProjectRecommendation(BaseModel):
    """A hands-on project to practice a missing skill."""
    title: str
    description: str
    skills_practiced: List[str]
    difficulty: str


class RoadmapStep(BaseModel):
    """One step in the learning roadmap."""
    step: int
    title: str
    description: str
    duration: str
    skills: List[str]


class SkillGapResponse(BaseModel):
    """Full skill gap analysis result."""
    target_role: str
    current_skills: List[str]
    required_skills: List[str]
    missing_skills: List[str]
    matching_skills: List[str]
    gap_percentage: float
    courses: List[CourseRecommendation]
    projects: List[ProjectRecommendation]
    roadmap: List[RoadmapStep]
    summary: str


# ─────────────────────────────────────────────────────────────────────────────
# Generic error schema
# ─────────────────────────────────────────────────────────────────────────────

class ErrorResponse(BaseModel):
    """Standard error envelope returned on failures."""
    success: bool = False
    error: str
    detail: Optional[Any] = None
