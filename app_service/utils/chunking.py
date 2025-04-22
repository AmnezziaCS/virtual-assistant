import tiktoken
from typing import List, Dict

class DocumentProcessor:
    def __init__(self):
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
    
    def process(self, text: str, doc_id: str) -> List[Dict]:
        chunks = []
        words = text.split()
        chunk_size = 512
        overlap = 51  # ~10%
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            chunks.append({
                "text": chunk,
                "doc_id": doc_id,
                "tokens": len(self.tokenizer.encode(chunk))
            })
        return chunks