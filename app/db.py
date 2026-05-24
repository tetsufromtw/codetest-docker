import aiomysql
import asyncio
from contextlib import asynccontextmanager

# Database connection pool
pool = None


async def init_db():
    """Initialize database connection pool with retry logic"""
    global pool
    max_retries = 10
    retry_delay = 2

    for attempt in range(max_retries):
        try:
            pool = await aiomysql.create_pool(
                host='db',
                port=3306,
                user='root',
                password='',
                db='codetest',
                autocommit=False,
                minsize=1,
                maxsize=10
            )
            return
        except Exception:
            if attempt < max_retries - 1:
                await asyncio.sleep(retry_delay)
            else:
                raise


async def close_db():
    """Close database connection pool"""
    global pool
    if pool:
        pool.close()
        await pool.wait_closed()


@asynccontextmanager
async def get_db_connection():
    """Get a database connection from the pool"""
    async with pool.acquire() as conn:
        yield conn
