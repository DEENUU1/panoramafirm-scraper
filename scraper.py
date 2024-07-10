from dataclasses import dataclass
from typing import Optional, List
import asyncio
import httpx
import requests
from bs4 import BeautifulSoup
import logging
from utils import get_categories


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)d %(name)s %(levelname)s %(message)s',
)
logger = logging.getLogger(__name__)


@dataclass
class Company:
    # From list
    name: str
    details_url: str
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    image_url: Optional[str] = None
    rate_value: Optional[float] = None
    rate_count: Optional[int] = None

    # From details
    street: Optional[str] = None
    postal_code: Optional[str] = None
    region: Optional[str] = None
    nip: Optional[str] = None
    description: Optional[str] = None


def scrape_company_list(start_url: str) -> List[Company]:

    url = start_url
    next_page = True
    result = []

    while next_page:
        try:
            logger.info(f"Scraping {url}")

            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            companies = soup.find_all('li', class_='company-item')
            logging.info(f"Found {len(companies)} companies")

            next_page_element = soup.find("a", {"title": "Przejdź do następnej strony"})
            if next_page_element is None:
                next_page = False

            url = next_page_element['href']

        except Exception as e:
            logging.error(e)

    return result


def company_list_scraper() -> None:
    logger.info("Starting scraper...")

    categories = get_categories()

    for category in categories:
        logger.info(f"Industry: {category.get('industry')} | Category: {category.get('category_name')}")

        full_url = f"https://panoramafirm.pl{category.get('category_url')}"

        companies = scrape_company_list(full_url)

    logger.info("Done")


if __name__ == '__main__':
    company_list_scraper()
