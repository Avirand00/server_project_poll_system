from fastapi import FastAPI
from controller.question_controller import router as question_router
from repository.database import database

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(question_router)
