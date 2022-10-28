from typing import Union
from datetime import datetime
from pydantic import BaseModel


class BodySearchEvent(BaseModel):
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


class BodyCollectEvent(EventBase):
    user_id: str
    parameters: Union[Order, None] = None


class EventTimeBase(EventBase):
    event_datetime: Union[datetime, None] = None

    class Config:
        json_encoders = {datetime: lambda t: t.isoformat(timespec='milliseconds')+"Z"}


class SearchedEvent(EventTimeBase):
    parameters: Union[Order, None] = None


class EventORM(EventTimeBase):
    user_id: str
    order_id: Union[str, None] = None

    class Config:
        orm_mode = True
