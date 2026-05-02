from fastapi import FastAPI
from api.webhook import router

app = FastAPI()
app.include_router(router, prefix="/webhook")