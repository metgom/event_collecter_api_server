import random
import json
import datetime
import uuid
import controller
from fastapi.encoders import jsonable_encoder
from pytz import utc, timezone
from model.schema import CollectedEvent

# for pytest...
# cmd : pytest tests/test.py -s


def dummy_event_generator(kst: bool = False):
    new_event = {
        "event_id": str(uuid.uuid1()),
        "user_id": "khs"+str(random.randint(0, 5)),
        "event": "purchase",
        "parameters":
            {
                "order_id": str(uuid.uuid1()),
                "currency": "krw",
                "price": random.randint(0, 99) * 100
            }
    }
    now_time = datetime.datetime.utcnow()
    if kst:
        now_time = utc.localize(now_time).astimezone(timezone('Asia/Seoul'))
    new_event["event_datetime"] = now_time
    return new_event


def test_send_to_sqs():
    event = dummy_event_generator()
    # boto3.set_stream_logger('botocore', level='DEBUG')
    resp = controller.send_to_sqs(CollectedEvent(**event))
    print(resp)


def test_search():
    search_result = controller.search_event('khs1')
    if search_result[0] is True:
        for row in search_result[1]:
            json_obj = jsonable_encoder(row)
            print(json.dumps(json_obj, indent='\t'))
            # print(f"{row.EventDB.user_id}\t{row.EventDB.event_id}\t{row.order_id}\t{row.price}")
    else:
        print("search fail.")
