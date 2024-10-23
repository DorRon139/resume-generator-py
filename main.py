from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from .app.routers import router



app = FastAPI()

origins = ["*"]



def create_application() -> FastAPI:
    application = FastAPI()

    application.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )
    application.include_router(router)
    return application

app = create_application()




