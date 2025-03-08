from fastapi import FastAPI

from routes import hotmart_router, meta_router

app = FastAPI()

app.include_router(hotmart_router)
app.include_router(meta_router)


