from fastapi import APIRouter
from model.schema import CollectedEvent, BaseResponse, SearchResponse
from controller import send_to_sqs, search


api_main_router = APIRouter(prefix='/api',
                            tags=['api'],
                            responses={403: {"description": "Operation forbidden"}})
event_router = APIRouter(prefix='/event', tags=['event'])


@api_main_router.post("/collect", response_model=BaseResponse)
@event_router.post("/", response_model=BaseResponse)
async def collect_event(event: CollectedEvent):
    # send to sqs
    response = send_to_sqs(event)
    result = BaseResponse(is_success=str(response).lower())
    return result


@api_main_router.post("/search", response_model=SearchResponse)
@event_router.get("/{user_id}", response_model=SearchResponse)
async def search_event(user_id: str):
    # request to rds
    is_success, results = search(user_id)
    result = SearchResponse(is_success=str(is_success).lower(), results=results)
    return result
