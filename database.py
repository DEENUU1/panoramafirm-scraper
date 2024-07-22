import aiosqlite
import logging

logger = logging.getLogger(__name__)


async def connect_db():
    return await aiosqlite.connect('database.db')
