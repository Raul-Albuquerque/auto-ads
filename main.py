from fastapi import FastAPI

from routes import hotmart_router

app = FastAPI()

app.include_router(hotmart_router)


