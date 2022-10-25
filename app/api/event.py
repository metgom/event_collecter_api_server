from fastapi import APIRouter
from model.schema import CollectedEvent, BaseResponse, SearchResponse, EventSearchBody
from controller import send_to_sqs, search_event_to_schema


api_main_router = APIRouter(prefix='/api',
                            responses={403: {"description": "Operation forbidden"}})


@api_main_router.post("/collect", response_model=BaseResponse, tags=['Collect Event'])
@api_main_router.post("/event", response_model=BaseResponse, tags=['Collect Event'])
async def collect_event(event: CollectedEvent):
    # send to sqs
    response = send_to_sqs(event)
    result = BaseResponse(is_success=str(response).lower())
    return result


@api_main_router.get("/event", response_model=SearchResponse, tags=['Search Event'])
@api_main_router.get("/event/{user_id}", response_model=SearchResponse, tags=['Search Event'])
async def search_event_get(user_id: str):
    # request to rds - get
    result = search_event_to_schema(user_id)
    return result


@api_main_router.post("/search", response_model=SearchResponse, tags=['Search Event'])
async def search_event_post(user_id: EventSearchBody):
    # request to rds - post
    result = search_event_to_schema(user_id.user_id)
    return result

