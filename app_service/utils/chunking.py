import tiktoken

def chunk_text(sections, doc_id="unknown", full_path=None, max_tokens=512, overlap=50):
    """
    Découpe les sections en chunks de max_tokens avec overlap, en gardant les métadonnées.
    """
    encoding = tiktoken.get_encoding("cl100k_base")
    chunks = []
    chunk_id = 0

    for section in sections:
        section_title = section["title"]
        text = section["text"]
        tokens = encoding.encode(text, allowed_special="all")

        start = 0
        while start < len(tokens):
            end = min(start + max_tokens, len(tokens))
            chunk_tokens = tokens[start:end]
            chunk_text = encoding.decode(chunk_tokens)

            chunks.append({
                "doc_id": doc_id,
                "chunk_num": chunk_id,
                "section": section_title,
                "full_path": full_path or "",
                "text": chunk_text.strip()
            })

            chunk_id += 1
            start += max_tokens - overlap
            if end == len(tokens):
                break

    return chunks