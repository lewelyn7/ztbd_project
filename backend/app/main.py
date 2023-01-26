from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from app.core.config import settings
from app.databases import sql
from app.routers.authors import router as authors_router
from app.routers.games import router as games_router
from app.routers.reviews import router as reviews_router
from app.routers.tests import router as tests_router
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi import status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import logging
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
    _app.add_middleware(
        TrustedHostMiddleware
    )
    _app.include_router(authors_router)
    _app.include_router(reviews_router)
    _app.include_router(games_router)
    _app.include_router(tests_router)
    _app.mount("/static", StaticFiles(directory="static"), name="static")
    return _app



app = get_application()


# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     response.headers["X-Process-Time"] = str(process_time)
#     return response

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
	exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
	logging.error(f"{request}: {exc_str}")
	content = {'status_code': 10422, 'message': exc_str, 'data': None}
	return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

@app.get('/')
def get_app_angular():

    with open('static/index.html', 'r') as file_index:
        html_content = file_index.read()
    return HTMLResponse(html_content, status_code=200)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")