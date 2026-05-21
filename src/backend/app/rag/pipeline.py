from app.llm.factory import get_llm
from app.rag.retriever import Retriever


class RagPipeline:
    def __init__(self) -> None:
        self.retriever = Retriever()

    async def answer(self, question: str) -> str:
        context = "\n\n".join(self.retriever.retrieve(question))
        prompt = (
            "Answer the user's question using only the provided context. "
            "If the answer is not present, say you don't know.\n\n"
            f"CONTEXT:\n{context}\n\nQUESTION: {question}"
        )
        return await get_llm().chat(prompt)


rag_pipeline = RagPipeline()
