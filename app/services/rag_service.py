"""
rag_service.py
──────────────
Retrieval-Augmented Generation service for JanashakthiCare.
Uses ChromaDB as the vector store and sentence-transformers for embeddings.

Install dependencies:
    pip install chromadb sentence-transformers

Usage:
    from app.services.rag_service import retrieve_context, build_knowledge_base
"""

import os
import json

# ── Try to import RAG dependencies (graceful fallback if not installed) ──────
try:
    import chromadb
    from sentence_transformers import SentenceTransformer
    RAG_AVAILABLE = True
except ImportError:
    RAG_AVAILABLE = False

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CHROMA_DIR  = os.path.join(BASE_DIR, "database", "chroma")
KB_FILE     = os.path.join(BASE_DIR, "knowledge_base", "janashakthi_kb.json")

# ── Singleton client + collection ────────────────────────────────────────────
_client     = None
_collection = None
_model      = None


def _get_collection():
    global _client, _collection, _model
    if not RAG_AVAILABLE:
        return None
    if _collection is None:
        os.makedirs(CHROMA_DIR, exist_ok=True)
        _client     = chromadb.PersistentClient(path=CHROMA_DIR)
        _collection = _client.get_or_create_collection(
            name="janashakthi_kb",
            metadata={"hnsw:space": "cosine"}
        )
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _collection


def build_knowledge_base():
    """
    Load janashakthi_kb.json and index all entries into ChromaDB.
    Call once at startup or when knowledge base is updated.
    """
    collection = _get_collection()
    if collection is None:
        print("RAG not available — skipping knowledge base build.")
        return

    if not os.path.exists(KB_FILE):
        print(f"Knowledge base file not found: {KB_FILE}")
        return

    with open(KB_FILE, "r", encoding="utf-8") as f:
        kb = json.load(f)

    # Clear existing entries and re-index
    existing = collection.get()
    if existing["ids"]:
        collection.delete(ids=existing["ids"])

    ids, embeddings, documents, metadatas = [], [], [], []

    for entry in kb:
        doc_id   = entry["id"]
        text     = entry["content"]
        meta     = entry.get("metadata", {})
        embedding = _model.encode(text).tolist()

        ids.append(doc_id)
        embeddings.append(embedding)
        documents.append(text)
        metadatas.append(meta)

    collection.add(ids=ids, embeddings=embeddings, documents=documents, metadatas=metadatas)
    print(f"Knowledge base built: {len(ids)} entries indexed.")


def retrieve_context(query: str, n_results: int = 3) -> str:
    """
    Retrieve the top-n most relevant knowledge base entries for a query.
    Returns a formatted string to inject into the LLM system prompt.
    Returns empty string if RAG is not available or no results found.
    """
    collection = _get_collection()
    if collection is None or collection.count() == 0:
        return ""

    try:
        embedding = _model.encode(query).tolist()
        results   = collection.query(
            query_embeddings=[embedding],
            n_results=min(n_results, collection.count())
        )
        docs = results.get("documents", [[]])[0]
        if not docs:
            return ""
        return "\n\n".join(docs)
    except Exception as e:
        print(f"RAG retrieval error: {e}")
        return ""
