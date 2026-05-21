"""SQLAlchemy ORM models. Importing this module registers all tables on the
shared `Base.metadata`, which is what Alembic autogenerate inspects."""
from app.db.models.user import User  # noqa: F401
from app.db.models.profile import Profile  # noqa: F401
from app.db.models.resume import Resume  # noqa: F401
from app.db.models.roadmap import Roadmap, RoadmapStep  # noqa: F401
from app.db.models.skill import Skill, UserSkill  # noqa: F401
from app.db.models.chat import ChatSession, ChatMessage  # noqa: F401
from app.db.models.analytics import AnalyticsEvent  # noqa: F401
from app.db.models.embedding import DocumentChunk  # noqa: F401