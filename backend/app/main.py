from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.scenario import build_demo_scenario
from app.schemas import Scenario

app = FastAPI(title="Satellite Resource Platform API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/scenario", response_model=Scenario)
def get_scenario() -> Scenario:
    return build_demo_scenario()

