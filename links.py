"""Loading and validation of the link catalogue (data/links.json)."""

import json
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data" / "links.json"


class LinkDataError(Exception):
    """Raised when the catalogue file is missing or malformed."""


def load_links(path=DATA_FILE):
    """Read and validate the catalogue.

    Read on every call so edits to the JSON show up on refresh, with no restart.
    """
    try:
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise LinkDataError(f"Catalogue file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise LinkDataError(f"Invalid JSON in {path}: {exc}") from exc

    if not isinstance(raw, dict):
        raise LinkDataError("Top level of the catalogue must be an object.")

    categories = raw.get("categories")
    if not isinstance(categories, list):
        raise LinkDataError("'categories' must be a list.")

    for index, category in enumerate(categories):
        if not isinstance(category, dict):
            raise LinkDataError(f"Category {index} must be an object.")
        if not category.get("name"):
            raise LinkDataError(f"Category {index} is missing 'name'.")
        links = category.get("links")
        if not isinstance(links, list):
            raise LinkDataError(f"Category '{category['name']}' needs a 'links' list.")
        for link in links:
            if not isinstance(link, dict) or not link.get("title") or not link.get("url"):
                raise LinkDataError(
                    f"Every link in '{category['name']}' needs a 'title' and a 'url'."
                )
            link.setdefault("description", "")
            link.setdefault("tags", [])

    raw.setdefault("title", "Internal Resource Hub")
    raw.setdefault("subtitle", "")
    return raw


def count_links(catalogue):
    return sum(len(category["links"]) for category in catalogue["categories"])
