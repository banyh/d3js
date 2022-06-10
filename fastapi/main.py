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


test_data = [
    {
        "error": "WP-2C1D",
        "problem_id": 42131,
        "subcode": "8C010005",
        "symptom_description": "SYSTEM ERROR WP-2C1D",
        "symptom_id": 4551057,
        "symptom_title": "WS* COOLING WATER TEMP CONTROL MMDC: WAFER FLOW CONTROL: LCW PUMP ENABLED DRY OR NO FLOW ERROR",
        "causes": [
            {
                "cause_id": 4,
                "cause_title": "wafer stage PPL leak",
                "procedures": [
                    {
                        "destination": "Service",
                        "name": "cws754.rep",
                        "status": "Final",
                        "subsystem": "WaferStage",
                        "title": "REMOVE AND INSTALL LCW RETURN TEMP SENSOR IN MK4i PPL",
                        "type": "Replace",
                        "parts": [
                            {
                                "id": "SERV.646.47404",
                                "desc": "NXT WS MK4I PPL TEMP SENS ASSY",
                            },
                            {
                                "id": "SERV.502.31876",
                                "desc": "NXT WS MK4I PCA CONN SEAL SET",
                            }
                        ],
                        "tools": [
                            {
                                "id": "SERV.502.17463",
                                "desc": "CS SR GR4 TOOL TROLLEY",
                            },
                            {
                                "id": "4022.502.81530",
                                "desc": "NT WS BM3 SERVICE COVER KIT",
                            }
                        ]
                    }
                ]
            },
            {
                "cause_id": 4551058,
                "cause_title": "MORE CAUSES POSSIBLE [NXT3 ONLY]",
                "procedures": [
                    {
                        "destination": "Service",
                        "name": "cws383.oca",
                        "status": "Final",
                        "subsystem": "WaferStage",
                        "title": "NXT3&4 WS LCSW FLOW PROBLEM OR LCW PRESSURE SENSOR WIRING DEFECT",
                        "type": "Ocap",
                        "tools": [
                            {
                                "id": "SERV.640.55621",
                                "desc": "TDE CONNECTOR TOOLKIT",
                            },
                            {
                                "id": "4022.502.81530",
                                "desc": "NT WS BM3 SERVICE COVER KIT",
                            }
                        ]
                    }
                ]
            },
            {
                "cause_id": 25648264,
                "cause_title": "HR valve (too far) closed",
                "procedures": []
            }
        ],
        "issues": [
            {
                "factory": "F15B",
                "jira_id": "LIT1XVBEEA-197109",
                "event_cd": "WP-2C1D",
                "subcode": "8C010005",
                "actions": "",
                "is_useful": True,
                "tool_id": "YPAN03",
            },
            {
                "factory": "F15B",
                "jira_id": "LIT1XVBEEA-190894",
                "event_cd": "WP-2C1D",
                "subcode": "8C010005",
                "actions": "",
                "is_useful": True,
                "tool_id": "YPAN03",
            }
        ]
    }
];


@api_app.get("/graph/nodes")
def get_graph_nodes():
    return create_graph(test_data)


@api_app.get("/graph", response_class=HTMLResponse)
def get_graph(request: Request):
    return templates.TemplateResponse("d3js.html", {"request": request})


app = FastAPI()
app.mount('/v1', api_app, name="api")  # this line should be placed before mounting static files
app.mount('/', StaticFiles(directory="web", html=True), name="web")
