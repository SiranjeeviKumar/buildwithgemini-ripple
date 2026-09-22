# app/rag_tools.py
"""RAG Retrieval Tool for Ripple - Foresight Angle."""

import vertexai
from vertexai.preview import rag

PROJECT_ID = "qwiklabs-gcp-03-3773bdab8c6e"
LOCATION = "us-central1"
CORPUS_NAME = "projects/50358334816/locations/us-central1/ragCorpora/8936469870749417472"


def consult_knowledge_corpus(query: str) -> str:
    """Searches the Project Gutenberg knowledge corpus (pg49513) for relevant passages and information.

    Args:
        query: What to look up or search for in the corpus.

    Returns:
        Matched text passages from the corpus or a message indicating no matches were found.
    """
    try:
        # Initialize Vertex AI in us-central1 for RAG retrieval
        vertexai.init(project=PROJECT_ID, location=LOCATION)

        resp = rag.retrieval_query(
            text=query,
            rag_resources=[rag.RagResource(rag_corpus=CORPUS_NAME)],
            rag_retrieval_config=rag.RagRetrievalConfig(top_k=5),
        )

        contexts = getattr(resp.contexts, "contexts", [])
        passages = [c.text.strip() for c in contexts if getattr(c, "text", "").strip()]

        if passages:
            return "\n\n---\n\n".join(passages)
        return "No relevant passages found in the knowledge corpus."
    except Exception as e:
        return f"Retrieval failed: {str(e)}"
