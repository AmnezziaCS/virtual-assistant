import mwparserfromhell
import re
import unicodedata

def clean_wiki_markup(text):
    """
    Nettoie les balises wiki, templates, caractères spéciaux, et normalise les encodages.
    """
    # Supprimer les templates {{...}} et {Template:...}
    text = re.sub(r'\{\{[^}]+\}\}', '', text)
    text = re.sub(r'\{Template:[^}]+\}', '', text)

    # Supprimer les fichiers [[File:...]]
    text = re.sub(r'\[\[File:[^\]]+\]\]', '', text)

    # Transformer les liens internes [[...]] en texte brut
    text = re.sub(r'\[\[([^|\]]*\|)?([^\]]+)\]\]', r'\2', text)

    # Supprimer les balises de mise en forme (gras, italique)
    text = re.sub(r"''+", '', text)

    # Supprimer les balises HTML
    text = re.sub(r'<[^>]+>', '', text)

    # Supprimer les titres vides ou délimiteurs
    text = re.sub(r'^=+\s*=+$', '', text, flags=re.MULTILINE)

    # Supprimer les espaces avant la ponctuation
    text = re.sub(r'\s+([.,:;!?])', r'\1', text)

    # Normaliser les encodages (é → e, etc.)
    text = unicodedata.normalize('NFKC', text)

    # Remplacer les sauts de ligne et espaces multiples
    text = re.sub(r'\s*\n\s*', ' ', text).strip()
    text = re.sub(r'\s+', ' ', text)

    return text.strip()

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