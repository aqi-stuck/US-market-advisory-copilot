from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routes_health import router as health_router
from app.api.routes_query import router as query_router
from app.core.config import settings
from app.db.session import Base, engine
from app.db import models


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    lifespan=lifespan,
)

app.include_router(health_router, tags=["health"])
app.include_router(query_router, prefix=settings.API_V1_STR, tags=["query"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
