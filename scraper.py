from dataclasses import dataclass
from typing import Optional, List
import httpx
from bs4 import BeautifulSoup
import logging
from utils import parse_str_to_int
import re

logger = logging.getLogger(__name__)


@dataclass
class Company:
    industry: str
    category: str
    name: str
    details_url: str
    nip: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    image_url: Optional[str] = None
    rate_value: Optional[float] = None
    rate_count: Optional[int] = None


@dataclass
class CompanyDetails:
    _id: int = None
    street: Optional[str] = None
    postal_code: Optional[str] = None
    city: Optional[str] = None
    region: Optional[str] = None
    nip: Optional[str] = None
    description: Optional[str] = None


async def scrape_company_details(url: str, _id: int) -> Optional[CompanyDetails]:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            nip = None
            contact_items = soup.find_all('div', class_='row contact-item py-2')
            for item in contact_items:
                item_divs = item.find_all('div')
                if len(item_divs) == 2:
                    first_div = item_divs[0]
                    if first_div and first_div.text.strip() == "NIP":
                        nip = item_divs[1].text.strip()
                        break

            description = None
            information_div = soup.find("div", id="information")
            if information_div:
                description = information_div.get_text(separator=" ", strip=True)

            street, city, region, postal_code = None, None, None, None
            address_div = soup.find("div", class_="address")
            if address_div:
                address_strong = address_div.get_text(separator=" ", strip=True)
                if address_strong:
                    postal_code_pattern = r'\d{2}-\d{3}'
                    city_pattern = r'\d{2}-\d{3} ([\w\s]+?),'
                    province_pattern = r'woj\. ([\w\s]+)'
                    street_pattern = r'ul\. ([\w\s]+?),'

                    postal_code_match = re.search(postal_code_pattern, address_strong)
                    city_match = re.search(city_pattern, address_strong)
                    province_match = re.search(province_pattern, address_strong)
                    street_match = re.search(street_pattern, address_strong)

                    postal_code = postal_code_match.group(0) if postal_code_match else None
                    city = city_match.group(1) if city_match else None
                    region = province_match.group(1) if province_match else None
                    street = street_match.group(1) if street_match else None

            return CompanyDetails(
                _id=_id,
                nip=nip,
                description=description,
                city=city,
                region=region,
                street=street,
                postal_code=postal_code
            )

    except Exception as e:
        logger.error(f"Error scraping company details from {url}: {e}")
        return None


async def scrape_company_list(start_url: str, industry: str, category: str) -> List[Company]:
    url = start_url
    next_page = True
    result = []

    async with httpx.AsyncClient() as client:
        while next_page:
            try:
                logger.info(f"Scraping {url}")
                response = await client.get(url)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, 'html.parser')

                companies = soup.find_all('li', class_='company-item')
                logger.info(f"Found {len(companies)} companies")

                for company in companies:
                    name = company.find("a", class_="company-name")
                    phone = company.find("a", class_="icon-telephone")
                    email = company.find("a", class_="icon-envelope")
                    website = company.find("a", class_="icon-website")
                    image_url = company.find("img", class_="logo")
                    rate_value = company.find("div", class_="rating-average")
                    rate_count = company.find("div", class_="rating-count")

                    if not name:
                        continue

                    company_obj = Company(
                        industry=industry,
                        category=category,
                        name=name.text,
                        details_url=name["href"],
                        phone=phone.get("title") if phone else None,
                        email=email.get("data-company-email") if email else None,
                        website=website.get("href") if website else None,
                        image_url=image_url.get("src") if image_url else None,
                        rate_value=float(rate_value.text) if rate_value else None,
                        rate_count=parse_str_to_int(rate_count.text) if rate_count else None,
                    )
                    result.append(company_obj)

                next_page_element = soup.find("a", {"title": "Przejdź do następnej strony"})
                if next_page_element is None:
                    next_page = False
                else:
                    url = next_page_element['href']

            except Exception as e:
                logger.error(e)
                break

    return result
