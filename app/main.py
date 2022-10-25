from fastapi import FastAPI
from api.event import api_main_router
from database import close_db
from fastapi.middleware.cors import CORSMiddleware
from api.metadata import tags_metadata


app = FastAPI(openapi_tags=tags_metadata)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_main_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.on_event("shutdown")
def shutdown_event():
    close_db()


# # for debug
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
