from fastapi import FastAPI

from .db import init_db, close_db
from .routers import api, web

app = FastAPI(title="LibGen Search API")
app.include_router(api.router)
app.include_router(web.router)


@app.on_event("startup")
async def startup():
    await init_db()


@app.on_event("shutdown")
async def shutdown():
    await close_db()
