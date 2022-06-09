from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

from src.graph import create_graph

api_app = FastAPI()

api_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")


@api_app.get("/")
def read_root():
    return {"Hello": "World"}


@api_app.get("/graph/nodes")
def get_graph_nodes():
    return create_graph()


@api_app.get("/graph", response_class=HTMLResponse)
def get_graph(request: Request):
    return templates.TemplateResponse("d3js.html", {"request": request})


app = FastAPI()
app.mount('/v1', api_app, name="api")  # this line should be placed before mounting static files
app.mount('/', StaticFiles(directory="web", html=True), name="web")
