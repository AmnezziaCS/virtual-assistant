from fastapi import FastAPI
from utils.embeddings import get_embeddings
from utils.search import SearchEngine
from utils.chunking import DocumentProcessor

app = FastAPI()
search_engine = SearchEngine()
doc_processor = DocumentProcessor()

@app.post("/ingest")
async def ingest_document(text: str, doc_id: str):
    chunks = doc_processor.process(text, doc_id)
    search_engine.index_chunks(chunks)
    return {"status": "success", "chunks": len(chunks)}

@app.get("/search")
async def search(query: str, doc_id: str = None):
    if doc_id:
        return search_engine.search_within_document(query, doc_id)
    return search_engine.search_across_documents(query)

@app.post("/ask")
async def ask_question(query: str):
    results = search_engine.search_across_documents(query)
    # Call LLM service with results
    return {"answer": "Generated answer", "sources": results[:3]}