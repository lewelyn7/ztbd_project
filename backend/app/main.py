from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.databases import sql
from app.routers.authors import router as authors_router
from app.routers.games import router as games_router
from app.routers.reviews import router as reviews_router
def get_application():
    
    sql.Base.metadata.create_all(bind=sql.engine)

    _app = FastAPI(title=settings.PROJECT_NAME)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    _app.include_router(authors_router)
    _app.include_router(reviews_router)
    _app.include_router(games_router)

    return _app


app = get_application()
