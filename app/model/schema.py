from typing import Union
from datetime import datetime
from pydantic import BaseModel


class EventSearchBody(BaseModel):
    user_id: str


class BaseResponse(BaseModel):
    is_success: str


class SearchResponse(BaseResponse):
    results: list


class Order(BaseModel):
    order_id: str
    currency: str
    price: float

    class Config:
        orm_mode = True


class EventBase(BaseModel):
    event_id: str
    event: str
    event_datetime: Union[datetime, None] = None

    class Config:
        json_encoders = {datetime: lambda t: t.isoformat(timespec='milliseconds')+"Z"}


class SearchedEvent(EventBase):
    parameters: Union[Order, None] = None


class CollectedEvent(EventBase):
    user_id: str
    parameters: Union[Order, None] = None


class EventORM(EventBase):
    user_id: str
    order_id: Union[str, None] = None

    class Config:
        orm_mode = True
