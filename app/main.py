from fastapi import FastAPI
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.config import settings
from app.database.core import SessionLocal
from app.src.data_lab.rank.routes import router as rank_router

app = FastAPI(title=settings.PROJECT_NAME)
app.include_router(rank_router, prefix="/api/v1")


@app.get("/api/v1/")
def read_root():
    return {"message": "Hello, World!", "data": None}



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
