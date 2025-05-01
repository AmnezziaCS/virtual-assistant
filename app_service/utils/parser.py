import mwparserfromhell
import re
import unicodedata

def clean_wiki_markup(text):
    #le parseur pour gérer les templates proprement
    code = mwparserfromhell.parse(text)
    text = code.strip_code()

    # Supprimer les balises HTML résiduelles
    text = re.sub(r'<[^>]+>', '', text)
    
    # Nettoyages généraux
    text = re.sub(r'\s+([.,:;!?])', r'\1', text)
    text = unicodedata.normalize('NFKC', text)
    text = re.sub(r'\s*\n\s*', ' ', text).strip()
    text = re.sub(r'\s+', ' ', text)

    return text

def parse_document(text):
    """
    Parse un document MediaWiki et retourne une liste de sections avec texte nettoyé.
    """
    wikicode = mwparserfromhell.parse(text)
    sections = []
    current_section = {"title": "Introduction", "text": []}

    for node in wikicode.nodes:
        if isinstance(node, mwparserfromhell.nodes.heading.Heading):
            if current_section["text"] and any(t.strip() for t in current_section["text"]):
                cleaned_text = clean_wiki_markup("\n".join(current_section["text"]))
                if cleaned_text.strip():
                    sections.append({
                        "title": current_section["title"],
                        "text": cleaned_text
                    })
            current_section = {"title": node.title.strip(), "text": []}
        else:
            if isinstance(node, mwparserfromhell.nodes.text.Text):
                current_section["text"].append(str(node))
            else:
                try:
                    current_section["text"].append(node.strip_code())
                except AttributeError:
                    current_section["text"].append(str(node))

    if current_section["text"] and any(t.strip() for t in current_section["text"]):
        cleaned_text = clean_wiki_markup("\n".join(current_section["text"]))
        if cleaned_text.strip():
            sections.append({
                "title": current_section["title"],
                "text": cleaned_text
            })

    return sections