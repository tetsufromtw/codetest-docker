import aiomysql
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db import init_db, close_db, get_db_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown
    await close_db()


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"hello": "from codetest-docker!"}


@app.get("/debug/users")
async def get_users():
    """Debug endpoint to get all users"""
    async with get_db_connection() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute("SELECT id, name, api_key FROM codetest.users")
            users = await cursor.fetchall()
            return {"users": users}
