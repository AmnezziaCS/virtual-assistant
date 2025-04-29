from utils.parser import parse_document
from utils.chunking import chunk_text
import re
import tiktoken

def count_words(text):
    """
    Compte les mots en ignorant la ponctuation et les espaces multiples.
    """
    words = re.findall(r'\b[\w\']+\b', text)
    return len(words)

def count_tokens(text):
    """
    Compte les tokens avec tiktoken pour validation.
    """
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text, allowed_special="all"))

long_paragraph = (
    "This is a very long paragraph to test chunking. It contains multiple sentences to ensure we exceed 512 tokens. "
    "We need to verify that the overlap works correctly. Let's add more text to make sure. "
    "Voici du texte avec des caractères spéciaux: éèçà. And some emojis: 😊🚀. "
) * 6  
sample_raw_text = f"""
= Main Section =
== Company Policy ==
'''All employees''' are entitled to 20 days of vacation per year.
[[File:logo.png]]
{{Template:HRPolicy}}
Employees must submit leave requests via [[Leave Portal|internal HR system]].
{long_paragraph}

== Benefits ==
Employees receive health insurance and a yearly bonus.
"""

def test_parsing_and_chunking():
    """
    Teste la pipeline de parsing et chunking avec un document MediaWiki.
    """
    print("Raw input:")
    print(sample_raw_text)

    print("\n Parsed sections:")
    sections = parse_document(sample_raw_text)
    if not sections:
        print("Aucune section trouvée ! Vérifiez parse_document.")
        return
    
    for section in sections:
        print(f"\nSection: {section['title']} ({count_tokens(section['text'])} tokens)")
        print(section['text'])

    print("\n Chunks:")
    chunks = chunk_text(sections, doc_id="HR_POLICY_2025", full_path="policies/HR")
    if not chunks:
        print("Aucun chunk généré ! Vérifiez chunk_text.")
        return
    
    for c in chunks:
        print(f"\nChunk #{c['chunk_num']} — Section: {c['section']} — {count_words(c['text'])} words — {count_tokens(c['text'])} tokens:")
        print(c['text'])

if __name__ == "__main__":
    test_parsing_and_chunking()