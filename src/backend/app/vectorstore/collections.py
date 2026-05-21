from app.vectorstore.chroma_client import get_chroma_client

COLLECTION_NAMES = ("resumes", "jobs", "learning")


def get_collection(name: str):
    if name not in COLLECTION_NAMES:
        raise ValueError(f"Unknown collection: {name}")
    return get_chroma_client().get_or_create_collection(name=name)
