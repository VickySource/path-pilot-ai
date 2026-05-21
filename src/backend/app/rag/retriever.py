from app.embeddings.provider import embed_texts
from app.vectorstore.collections import get_collection


class Retriever:
    def __init__(self, collection: str = "resumes", k: int = 5) -> None:
        self.collection_name = collection
        self.k = k

    def retrieve(self, query: str) -> list[str]:
        col = get_collection(self.collection_name)
        embedding = embed_texts([query])[0]
        result = col.query(query_embeddings=[embedding], n_results=self.k)
        docs = result.get("documents", [[]])
        return docs[0] if docs else []
