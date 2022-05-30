from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from src.graph import create_graph

api_app = FastAPI()

api_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api_app.get("/")
def read_root():
    return {"Hello": "World"}


@api_app.get("/graph")
def graph():
    return HTMLResponse(create_graph())


app = FastAPI()
app.mount('/v1', api_app)  # this line should be placed before mounting static files
app.mount('/', StaticFiles(directory="web", html=True), name="web")
