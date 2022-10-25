"""
get request from client(bot)
send to sqs
"""
import boto3
import os
import json
import datetime
from typing import Union, Tuple, Type
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from config.config import server_config
from database import get_db_session, ORMBase
from model.schema import CollectedEvent, Order, SearchedEvent, SearchResponse
from model.orm_model import EventDB, OrderDB
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from boto3.exceptions import Boto3Error


def send_to_sqs(event: CollectedEvent) -> bool:
    # %Y-%m-%dT%H:%M:%S.%3f
    event.event_datetime = datetime.datetime.utcnow().isoformat(timespec='milliseconds')
    try:
        # 엔드포인트가 현재 서비스네임.리전.~ 형식인데 boto3에서 리전.서비스네임.~의 예전 형태로 제공되서 발생하는 문제를 해결하기 위함
        os.environ["BOTO_DISABLE_COMMONNAME"] = "True"
        sqs_client = boto3.resource('sqs',
                                    region_name=server_config["AWS_DEFAULT"]["AWS_DEFAULT_REGION"],
                                    aws_access_key_id=server_config["AWS_DEFAULT"]["AWS_ACCESS_KEY_ID"],
                                    aws_secret_access_key=server_config["AWS_DEFAULT"]["AWS_SECRET_ACCESS_KEY"],
                                    )
        queue = sqs_client.Queue(server_config["AWS_SQS"]["AWS_SQS_URL"])
        event_obj = json.dumps(jsonable_encoder(event))
        response = queue.send_message(MessageBody=event_obj)
        if response['ResponseMetadata']['HTTPStatusCode'] >= 400:
            return False
    except (Boto3Error, KeyError):
        return False
    except Exception as e:
        raise e
    return True


def search_event(user_id) -> Tuple[bool, Union[list, None]]:
    db_session = get_db_session()
    try:
        query_result = db_session.query(EventDB)\
            .options(joinedload(EventDB.order))\
            .add_columns(OrderDB.order_id.label('order_id'),
                         OrderDB.price.label('price'),
                         OrderDB.currency.label('currency')) \
            .outerjoin(OrderDB) \
            .where(user_id == EventDB.user_id)\
            .order_by(EventDB.event_datetime.desc(), EventDB.user_id.asc())\
            .all()
        result = []
        for row in query_result:
            row_event = SearchedEvent(**row.EventDB.__dict__)
            row_event.event_datetime = row_event.event_datetime.isoformat(timespec='milliseconds')+"Z"
            if row.order_id is not None:
                row_event.parameters = Order(order_id=row.order_id,
                                             price=row.price,
                                             currency=row.currency)
            result.append(row_event)
        return True, result
    except SQLAlchemyError as e:
        db_session.close()
        print(e)
        return False, None
    except Exception as e:
        db_session.close()
        raise e
    finally:
        db_session.close()


def search_event_to_schema(user_id: str) -> SearchResponse:
    is_success, results = search_event(user_id)
    result = SearchResponse(is_success=str(is_success).lower(), results=results)
    return result


def schema_to_model(schema: BaseModel, orm_class: Type[ORMBase]) -> ORMBase:
    orm_model = orm_class(**schema.dict())
    return orm_model


def collected_json_to_schema(item: dict) -> Tuple[CollectedEvent, Union[Order, None]]:
    order = None
    parameters = item.pop("parameters", None)
    event = CollectedEvent(**item)
    if parameters is not None:
        order = Order(**parameters)
        item["order_id"] = order.order_id
        event.order_id = order.order_id
    event.event_datetime = datetime.datetime.utcnow()
    return event, order

