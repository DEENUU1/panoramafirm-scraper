from typing import List

from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass
import logging
import json

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)d %(name)s %(levelname)s %(message)s',
)
logger = logging.getLogger(__name__)

INDUSTRIES = [
    "biuro,z",
    "budownictwo,b",
    "dom_i_ogród,c",
    "dzieci,u",
    "finanse_i_ubezpieczenia,r",
    "instytucje,_urzędy,f",
    "motoryzacja_i_transport,h",
    "nauka,i",
    "odzież_i_tekstylia,g",
    "porady,w",
    "przemysł_i_energetyka,k",
    "rolnictwo_i_leśnictwo,j",
    "rozrywka_i_rekreacja,l",
    "telekomunikacja,_internet,_technologie,t",
    "turystyka,m",
    "usługi_dla_firm,n",
    "usługi_dla_każdego,p",
    "zdrowie_i_uroda,s",
    "żywność_i_używki,a"
]


@dataclass
class Category:
    industry: str
    category_name: str
    category_description: str
    category_url: str


def get_categories(industry: str) -> List[Category]:
    categories = []

    url = f"https://panoramafirm.pl/{industry}/branze.html"

    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0"
        }
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    category_cards = soup.find_all("li", class_="py-1")

    for card in category_cards:
        category_name = card.find("h3")
        category_description = card.find("p")
        category_url = card.find("a")

        if not category_url or not category_name or not category_description:
            continue

        category = Category(
            industry=industry,
            category_name=category_name.text.strip(),
            category_description=category_description.text.strip(),
            category_url=category_url["href"]
        )
        categories.append(category)

    return categories


def write_categories_to_json(categories: List[Category], filename: str):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump([category.__dict__ for category in categories], f, indent=4)


def category_scraper() -> None:
    logger.info("Starting script")

    results = []

    for industry in INDUSTRIES:
        categories = get_categories(industry)
        results.extend(categories)

        logger.info(f"Found {len(categories)} categories for {industry}")

    logger.info("Script finished")

    logger.info("Writing results to json")

    write_categories_to_json(results, "categories.json")

    logger.info("Done")


if __name__ == "__main__":
    category_scraper()
