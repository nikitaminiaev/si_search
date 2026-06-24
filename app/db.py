import aiomysql

from .config import DB_CONFIG

POOL = None


async def get_pool():
    return await aiomysql.create_pool(
        **DB_CONFIG, minsize=1, maxsize=4, autocommit=True
    )


async def init_db():
    global POOL
    POOL = await get_pool()


async def close_db():
    global POOL
    if POOL:
        POOL.close()
        await POOL.wait_closed()
        POOL = None
