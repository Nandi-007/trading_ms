from typing import Union

from pydantic import BaseModel, validator


class OrderInput(BaseModel):
    id: Union[str, None] = None
    stoks: str
    quantity: float
    status: Union[str, None] = None

    @validator('quantity')
    def validate_quantity(cls, value: float):
        if not isinstance(value, float) or value <= 0:
            raise ValueError("Quantity must be a positive float")
        return value

    @validator('stoks')
    def validate_stoks(cls, value: str):
        if value not in ["EUR", "USD", "GBP"]:
            raise ValueError("stoks must be 'EUR' or 'USD' or 'GBP'")
        return value


class OrderStatus(BaseModel):
    orderId: str
    orderStatus: str
