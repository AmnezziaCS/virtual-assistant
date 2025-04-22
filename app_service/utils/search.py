import chromadb
from utils.embeddings import embed_text

class SearchEngine:
    def __init__(self):
        self.client = chromadb.Client()
        self.collection = self.client.create_collection(
            name="docs",
            metadata={"hnsw:space": "cosine"}
        )
    
    def index_chunks(self, chunks: list):
        ids = [f"{chunk['doc_id']}_{i}" for i, chunk in enumerate(chunks)]
        embeddings = [embed_text(chunk["text"]) for chunk in chunks]
        documents = [chunk["text"] for chunk in chunks]
        metadatas = [{"doc_id": chunk["doc_id"]} for chunk in chunks]
        
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )
    
    def search_within_document(self, query: str, doc_id: str):
        results = self.collection.query(
            query_embeddings=[embed_text(query)],
            n_results=3,
            where={"doc_id": doc_id}
        )
        return results
    
    def search_across_documents(self, query: str):
        results = self.collection.query(
            query_embeddings=[embed_text(query)],
            n_results=3
        )
        return results