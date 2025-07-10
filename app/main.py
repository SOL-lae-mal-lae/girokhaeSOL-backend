from fastapi import FastAPI
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.config import settings
from app.database.core import SessionLocal
from app.src.account.routes import router as account_router

app = FastAPI(title=settings.PROJECT_NAME)

# Include routers
app.include_router(account_router, prefix="/api/v1", tags=["accounts"])


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
