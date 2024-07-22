import logging
from repository import company_exists_by_details_url_or_nip, create_company
from scraper import scrape_company_list
from utils import get_categories

logger = logging.getLogger(__name__)


async def process_companies(db) -> None:
    try:
        categories = get_categories()

        for category in categories:

            logger.info(f"Industry: {category.get('industry')} | Category: {category.get('category_name')}")

            full_url = f"https://panoramafirm.pl{category.get('category_url')}"

            companies = await scrape_company_list(
                full_url, category.get("industry"), category.get("category_name")
            )

            async with db.cursor() as cursor:
                logger.info("Saving data to database")

                for company in companies:
                    if not await company_exists_by_details_url_or_nip(
                            cursor, company.details_url, company.nip
                    ):
                        await create_company(cursor, company)
                await db.commit()
    except Exception as e:
        logger.error(e)
