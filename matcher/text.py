"""Text helpers: reading files and normalizing words."""
import re
from pathlib import Path

STOPWORDS = {
    "a", "about", "above", "after", "all", "also", "an", "and", "any", "are", "as", "at",
    "be", "been", "being", "by", "can", "will", "would", "should", "could", "must", "may",
    "for", "from", "has", "have", "had", "how", "in", "into", "is", "it", "its", "of", "on",
    "or", "our", "such", "that", "the", "their", "them", "then", "there", "these", "they",
    "this", "to", "up", "we", "were", "what", "when", "where", "which", "who", "with",
    "you", "your", "work", "working", "ability", "strong", "good", "excellent", "knowledge",
    "experience", "experienced", "required", "requirements", "preferred", "responsibilities",
    "role", "job", "team", "teams", "years", "year", "etc", "including", "include", "using",
    "use", "new", "looking", "join", "candidate", "candidates", "company", "position",
    "intern", "internship", "skills", "skill", "understanding", "familiarity", "proficiency", "plus", "bonus",
}

WORD_RE = re.compile(r"[a-zA-Z][a-zA-Z+#.\-]*[a-zA-Z+#]|[a-zA-Z]")


def read_text(path) -> str:
    """Read .txt/.md files, or .pdf if pypdf is installed."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    if path.suffix.lower() == ".pdf":
        try:
            from pypdf import PdfReader
        except ImportError:
            raise RuntimeError("PDF support needs pypdf: pip install pypdf")
        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    return path.read_text(encoding="utf-8", errors="ignore")


def tokenize(text: str) -> list:
    """Lowercase words, minus stopwords and 1-letter tokens."""
    words = [w.lower().strip(".-") for w in WORD_RE.findall(text)]
    return [w for w in words if len(w) > 1 and w not in STOPWORDS]
