import uvicorn
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware

from app.database import init_db
from app.flask_app import app as flask_app
from app.routers import film, reviews, user

app = FastAPI(title='Film rating service')

app.include_router(film.router)
app.include_router(user.router)
app.include_router(reviews.router)
app.mount('/', WSGIMiddleware(flask_app))


if __name__ == '__main__':  # pragma: no cover
    init_db()
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
