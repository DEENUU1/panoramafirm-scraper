import asyncio

from repository import get_companies_with_pagination, update_company_details
from scraper import scrape_company_details
import logging

logger = logging.getLogger(__name__)


async def process_company_batch(db, limit, offset):
    async with db.cursor() as cursor:
        companies = await get_companies_with_pagination(cursor, limit, offset)
        if not companies:
            return False

        tasks = []
        for company in companies:
            details = await scrape_company_details(company['details_url'], company['id'])
            if details:
                tasks.append(update_company_details(
                    cursor,
                    company_id=details._id,
                    nip=details.nip,
                    region=details.region,
                    postal_code=details.postal_code,
                    street=details.street,
                    description=details.description,
                    city=details.city
                ))
        await asyncio.gather(*tasks)
        await db.commit()
    return True


async def process_company_details(db) -> None:
    try:
        limit = 25
        offset = 0
        while True:
            logger.info(f"Offset: {offset}")
            success = await process_company_batch(db, limit, offset)
            if not success:
                break
            offset += limit

    except Exception as e:
        logger.error(e)