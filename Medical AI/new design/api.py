# # api.py - FastAPI wrapper for EMT simulation
# # Run: uvicorn api:app --reload --port 8000
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from typing import Optional, Dict, Any

# from db import DB
# from engine import Engine
# from llm_parser import parse as parse_text
# from grader import grade_run
# from dotenv import load_dotenv
# load_dotenv()


# DB_PATH = "emt_sim.db"  # adjust if needed

# app = FastAPI(title="EMT Simulation API", version="0.1.0")
# from fastapi.middleware.cors import CORSMiddleware

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],            # for local testing; lock down later
#     allow_credentials=False,        # keep False if using "*"
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# db = DB(DB_PATH)

# class StartRunRequest(BaseModel):
#     scenario_id: Optional[int] = None

# class StartRunResponse(BaseModel):
#     run_id: str
#     scenario: Dict[str, Any]

# class StepRequest(BaseModel):
#     run_id: str
#     text: str

# class StepResponse(BaseModel):
#     parsed: Dict[str, Any]
#     reply: Dict[str, Any]

# @app.get("/health")
# def health():
#     return {"ok": True}

# @app.get("/scenarios")
# def list_scenarios():
#     rows = db.get_scenarios()
#     return [dict(row) for row in rows]
# @app.get("/")
# def root():
#     return {"ok": True, "hint": "Use /docs for interactive API"}



# @app.post("/run/start", response_model=StartRunResponse)
# def start_run(body: StartRunRequest):
#     scenarios = db.get_scenarios()
#     if not scenarios:
#         raise HTTPException(500, "No scenarios available. Did you run setup_emt_db.py?")
#     sc = None
#     if body.scenario_id is not None:
#         sc = db.get_scenario(body.scenario_id)
#         if not sc:
#             raise HTTPException(404, f"Scenario id {body.scenario_id} not found")
#     else:
#         sc = scenarios[0]
#     run_id = db.create_run(sc["id"])
#     return StartRunResponse(run_id=run_id, scenario=dict(sc))

# @app.post("/run/step", response_model=StepResponse)
# def run_step(body: StepRequest):
#     run = db.get_run(body.run_id)
#     if not run:
#         raise HTTPException(404, "Run not found")
#     parsed = parse_text(body.text)
#     eng = Engine(db, body.run_id)
#     reply = eng.step(parsed)
#     return StepResponse(parsed=parsed, reply=reply)

# @app.get("/run/{run_id}/grade")
# def run_grade(run_id: str):
#     run = db.get_run(run_id)
#     if not run:
#         raise HTTPException(404, "Run not found")
#     return grade_run(db, run_id)



# from pydantic import BaseModel
# from typing import Optional, Dict, Any

# # 1) Start session (alias to /run/start)
# class SessionStartCompat(BaseModel):
#     # Trainer sends { "case_id": 1 }, map to our scenario_id
#     case_id: Optional[int] = None

# @app.post("/session")
# def compat_start_session(body: SessionStartCompat):
#     # Reuse your existing logic
#     scenarios = db.get_scenarios()
#     if not scenarios:
#         raise HTTPException(500, "No scenarios available. Did you run setup_emt_db.py?")
#     if body.case_id is not None:
#         sc = db.get_scenario(body.case_id)
#         if not sc:
#             raise HTTPException(404, f"Scenario id {body.case_id} not found")
#     else:
#         sc = scenarios[0]
#     run_id = db.create_run(sc["id"])
#     # Return trainer-friendly keys
#     return {"session_id": run_id, "scenario": dict(sc)}

# # 2) Send message/step (alias to /run/step)
# class SessionMessageCompat(BaseModel):
#     session_id: str
#     content: str

# @app.post("/message")
# def compat_message(body: SessionMessageCompat):
#     run = db.get_run(body.session_id)
#     if not run:
#         raise HTTPException(404, "Run not found")
#     parsed = parse_text(body.content)
#     eng = Engine(db, body.session_id)
#     reply = eng.step(parsed)
#     # Shape a friendly response (and include parsed for debugging)
#     return {"reply": reply, "parsed": parsed, "session_id": body.session_id}

# # 3) Session state (optional, simple view)
# @app.get("/session/{run_id}")
# def compat_get_session(run_id: str):
#     run = db.get_run(run_id)
#     if not run:
#         raise HTTPException(404, "Run not found")
#     # If you later add db.get_turns(run_id) or vitals, include them here.
#     return {"session_id": run_id, "run": dict(run)}

# # 4) Submit / grade (alias to /run/{run_id}/grade)
# class SessionIdCompat(BaseModel):
#     session_id: str

# @app.post("/submit")
# def compat_submit(body: SessionIdCompat):
#     run = db.get_run(body.session_id)
#     if not run:
#         raise HTTPException(404, "Run not found")
#     result = grade_run(db, body.session_id)
#     return {"session_id": body.session_id, "grade": result}
