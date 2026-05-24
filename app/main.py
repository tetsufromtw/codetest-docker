import aiomysql
from fastapi import FastAPI, Response, status
from contextlib import asynccontextmanager
from app.db import init_db, close_db, get_db_connection
from app.schemas import TransactionRequest, TransactionResponse
from app.transaction_service import register_transaction


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


@app.post("/transactions")
async def create_transaction(transaction: TransactionRequest, response: Response) -> TransactionResponse:
    """Register a new transaction for a user"""
    success = await register_transaction(
        user_id=transaction.user_id,
        amount=transaction.amount,
        description=transaction.description
    )

    if not success:
        # Return 402 Payment Required if transaction would exceed limit
        response.status_code = status.HTTP_402_PAYMENT_REQUIRED
        return TransactionResponse(message="Transaction would exceed user limit")

    # Return 201 Created on success
    response.status_code = status.HTTP_201_CREATED
    return TransactionResponse(message="Transaction registered successfully")
