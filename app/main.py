
from fastapi import FastAPI
from routes import sheet
from core import env

app = FastAPI()

from core import handlers, middlewares

app.include_router(sheet.router)

@app.get('/')
async def who_i_am():
    return {
        "who i am": "My Finances API"
    }
