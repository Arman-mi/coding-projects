# api.py - FastAPI wrapper for EMT simulation (+ static UI at /web)
# Run: uvicorn api:app --reload --port 8000
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, Dict, Any
from pathlib import Path
from fastapi.staticfiles import StaticFiles

from db import DB
from engine import Engine
from llm_parser import parse as parse_text
from grader import grade_run
from dotenv import load_dotenv
load_dotenv()

DB_PATH = "emt_sim.db"  # adjust if needed

# app = FastAPI(title="EMT Simulation API", version="0.1.0")
# app.mount("/web", StaticFiles(directory="web", html=True), name="web")
BASE_DIR = Path(__file__).resolve().parent
WEB_DIR = BASE_DIR / "web"

app = FastAPI(title="EMT Simulation API", version="0.1.0")
app.mount("/web", StaticFiles(directory=str(WEB_DIR), html=True), name="web")


@app.get("/")
def root():
    return RedirectResponse(url="/web/")

# Single DB connection (SQLite): ensure db.py uses check_same_thread=False
db = DB(DB_PATH)

class StartRunRequest(BaseModel):
    scenario_id: Optional[int] = None

class StartRunResponse(BaseModel):
    run_id: str
    scenario: Dict[str, Any]

class StepRequest(BaseModel):
    run_id: str
    text: str

class StepResponse(BaseModel):
    parsed: Dict[str, Any]
    reply: Dict[str, Any]

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/scenarios")
def list_scenarios():
    rows = db.get_scenarios()
    return [dict(row) for row in rows]

@app.post("/run/start", response_model=StartRunResponse)
def start_run(body: StartRunRequest):
    scenarios = db.get_scenarios()
    if not scenarios:
        raise HTTPException(500, "No scenarios available. Did you run setup_emt_db.py?")
    sc = None
    if body.scenario_id is not None:
        sc = db.get_scenario(body.scenario_id)
        if not sc:
            raise HTTPException(404, f"Scenario id {body.scenario_id} not found")
    else:
        sc = scenarios[0]
    run_id = db.create_run(sc["id"])
    return StartRunResponse(run_id=run_id, scenario=dict(sc))

@app.post("/run/step", response_model=StepResponse)
def run_step(body: StepRequest):
    run = db.get_run(body.run_id)
    if not run:
        raise HTTPException(404, "Run not found")
    parsed = parse_text(body.text)
    eng = Engine(db, body.run_id)
    reply = eng.step(parsed)
    return StepResponse(parsed=parsed, reply=reply)

@app.get("/run/{run_id}/grade")
def run_grade(run_id: str):
    run = db.get_run(run_id)
    if not run:
        raise HTTPException(404, "Run not found")
    return grade_run(db, run_id)
