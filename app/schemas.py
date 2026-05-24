from pydantic import BaseModel


class TransactionRequest(BaseModel):
    user_id: int
    amount: int
    description: str


class TransactionResponse(BaseModel):
    message: str
