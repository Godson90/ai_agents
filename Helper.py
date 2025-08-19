import re

def slugify(text: str) -> str:
    # keep letters, numbers, spaces, dashes, underscores, and dots
    slug = re.sub(r"[^A-Za-z0-9 ._-]+", "", text).strip().replace(" ", "_")
    return slug or "result"
