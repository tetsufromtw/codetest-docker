from app.db import get_db_connection

AMOUNT_LIMIT = 1000


async def register_transaction(user_id: int, amount: int, description: str) -> bool:
    """
    Register a transaction for a user.

    Returns True if transaction was registered successfully.
    Returns False if registering would exceed the user's limit.

    Uses SELECT FOR UPDATE to prevent race conditions in concurrent requests.
    """
    async with get_db_connection() as conn:
        async with conn.cursor() as cursor:
            # Start a transaction
            await conn.begin()

            try:
                # Lock the user's transaction rows and get current total
                # SELECT FOR UPDATE prevents other transactions from reading/writing until we commit
                await cursor.execute(
                    "SELECT COALESCE(SUM(amount), 0) FROM codetest.transactions WHERE user_id = %s FOR UPDATE",
                    (user_id,)
                )
                result = await cursor.fetchone()
                current_total = result[0] if result else 0

                # Check if adding this amount would exceed the limit
                if current_total + amount > AMOUNT_LIMIT:
                    await conn.rollback()
                    return False

                # Insert the transaction
                await cursor.execute(
                    "INSERT INTO codetest.transactions (user_id, amount, description) VALUES (%s, %s, %s)",
                    (user_id, amount, description)
                )

                # Commit the transaction
                await conn.commit()
                return True

            except Exception:
                await conn.rollback()
                raise
