from sentence_transformers import SentenceTransformer
import numpy as np

model = None

def get_embeddings():
    global model
    if model is None:
        model = SentenceTransformer('all-MiniLM-L6-v2')
    return model

def embed_text(text: str) -> np.ndarray:
    return get_embeddings().encode([text])[0]