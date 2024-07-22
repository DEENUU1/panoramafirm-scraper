import logging
from typing import Any, Optional

from scraper import Company

logger = logging.getLogger(__name__)


async def create_company_table(cursor):
    try:
        await cursor.execute("""
            CREATE TABLE IF NOT EXISTS companies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                industry TEXT NOT NULL,
                category TEXT NOT NULL,
                name TEXT NOT NULL,
                details_url TEXT NOT NULL UNIQUE,
                phone TEXT,
                email TEXT,
                website TEXT,
                image_url TEXT,
                rate_value FLOAT,
                rate_count INTEGER,
                street TEXT,
                postal_code TEXT,
                region TEXT,
                nip TEXT,
                description TEXT,
                city TEXT
            )
        """)
        await cursor.execute("CREATE INDEX IF NOT EXISTS idx_companies_industry ON companies(industry);")
        await cursor.execute("CREATE INDEX IF NOT EXISTS idx_companies_category ON companies(category);")
        await cursor.execute("CREATE INDEX IF NOT EXISTS idx_companies_region ON companies(region);")

    except Exception as e:
        logger.error(f"Error occurred: {e}")


async def update_company_details(cursor, company_id, nip, region, postal_code, street, description, city):
    query = """
        UPDATE companies
        SET nip = ?,
            region = ?,
            postal_code = ?,
            street = ?,
            description = ?,
            city = ?
        WHERE id = ?;
    """
    await cursor.execute(query, (nip, region, postal_code, street, description, city, company_id))


async def company_exists_by_details_url_or_nip(cursor, details_url: str, nip: Optional[str]) -> bool:
    try:
        query = """
            SELECT 1 FROM companies WHERE details_url = ? OR nip = ?
        """
        await cursor.execute(query, (details_url, nip))
        result = await cursor.fetchone()
        return result is not None
    except Exception as e:
        logger.error(e)


async def create_company(cursor, data: Company) -> None:
    try:
        await cursor.execute("""
            INSERT INTO companies (
                industry, category, name, details_url, phone, email, website, image_url, rate_value, rate_count
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.industry, data.category, data.name, data.details_url, data.phone, data.email,
            data.website, data.image_url, data.rate_value, data.rate_count
        ))
    except Exception as e:
        logger.error(e)


async def get_companies_with_pagination(cursor, limit: int = 100, offset: int = 0) -> list[dict[str, Any]]:
    try:
        count_query = """
                    SELECT COUNT(*) FROM companies WHERE email IS NOT NULL AND email != '' 
        AND phone IS NOT NULL AND phone != ''
                """
        await cursor.execute(count_query)
        total_count = await cursor.fetchone()
        if total_count:
            total_count = total_count[0]
        else:
            total_count = 0
        logger.info(f'Total number of companies with valid email and phone: {total_count}')

        query = """
            SELECT * FROM companies WHERE email IS NOT NULL AND email != ''
AND phone IS NOT NULL AND phone != '' LIMIT ? OFFSET ?
        """
        await cursor.execute(query, (limit, offset))
        rows = await cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        logger.error(e)
        return []
