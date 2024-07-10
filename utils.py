import json
import os
from typing import Dict, Any, List

from categories import category_scraper


def get_categories() -> List[Dict[str, Any]]:
    if not os.path.exists("categories.json"):
        category_scraper()

        with open("categories.json", "r") as f:
            return json.load(f)

    with open("categories.json", "r") as f:
        return json.load(f)
