import logging
import asyncio
import click

from database import connect_db
from list_processor import process_companies
from detail_processor import process_company_details
from repository import create_company_table

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)d %(name)s %(levelname)s %(message)s',
)
logger = logging.getLogger(__name__)


async def run_process(db, process_func):
    async with db.cursor() as cursor:
        await create_company_table(cursor)
        await db.commit()

    logger.info('Database connected.')

    try:
        await process_func(db)
    finally:
        await db.close()
        logger.info("Database connection closed.")


@click.command()
@click.option(
    '--process',
    type=click.Choice(['companies', 'details']),
    required=True,
    help='Choose which process to run: "companies" or "details"'
)
def main(process):
    async def async_main():
        logger.info('Connecting to database...')
        db = await connect_db()

        if process == 'companies':
            await run_process(db, process_companies)
        elif process == 'details':
            await run_process(db, process_company_details)

    asyncio.run(async_main())


if __name__ == '__main__':
    main()
