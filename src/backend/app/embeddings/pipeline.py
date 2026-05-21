from app.embeddings.provider import embed_texts
from app.vectorstore.collections import get_collection


class EmbeddingsPipeline:
    def upsert(self, document_id: str, chunks: list[str], collection: str = "resumes") -> None:
        if not chunks:
            return
        col = get_collection(collection)
        ids = [f"{document_id}:{i}" for i in range(len(chunks))]
        embeddings = embed_texts(chunks)
        col.upsert(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=[{"document_id": document_id, "chunk": i} for i in range(len(chunks))],
        )


embeddings_pipeline = EmbeddingsPipeline()
