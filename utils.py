import json
import os
from typing import Any

from categories import category_scraper


def get_categories() -> list[dict[str, Any]]:
    if not os.path.exists("categories.json"):
        category_scraper()

        with open("categories.json", "r") as f:
            return json.load(f)

    with open("categories.json", "r") as f:
        return json.load(f)


def parse_str_to_int(text: str) -> int:
    result = ""
    for char in text:
        if char.isdigit():
            result += char

    return int(result)
