from fastapi import FastAPI # type: ignore
from database.config import Base, engine
from auth.router import auth_router

app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(auth_router, prefix="/auth")

@app.get("/")
def read_root():
    return {"Hello": "World"}
