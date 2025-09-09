# llm_parser.py — LLM-first parser with heuristic rescue and _source flag
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any
import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

@dataclass
class ParsedAction:
    action_type: str
    free_text: str
    symptom: Optional[str] = None
    body_region: Optional[str] = None
    duration: Optional[str] = None
    severity: Optional[str] = None
    test_name: Optional[str] = None
    intervention: Optional[str] = None
    confidence: float = 0.6
    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        return {k: v for k, v in d.items() if v is not None}

def _emit(p: ParsedAction, source: str) -> Dict[str, Any]:
    d = p.to_dict(); d["_source"] = source; return d

def _heuristic(text: str) -> Dict[str, Any]:
    t = (text or "").strip().lower()

    # management
    if any(k in t for k in ["stroke alert","code stroke","activate stroke","start a stroke code"]):
        return _emit(ParsedAction("management", text, confidence=0.9), "heuristic")

    # vitals
    if any(k in t for k in ["vitals","bp","blood pressure","hr","pulse","rr","respiratory rate","spo2","oxygen saturation"]):
        return _emit(ParsedAction("vitals_request", text, confidence=0.9), "heuristic")
    
    if any(k in t for k in [
    "where does it hurt", "where is the pain", "point to the pain",
    "show me where it hurts", "pain location", "where hurts"]):
        return _emit(ParsedAction("history", text, symptom="pain location", confidence=0.9), "heuristic")


    # interventions
    if "aspirin" in t or " asa " in f" {t} ":
        return _emit(ParsedAction("intervention", text, intervention="aspirin 324 mg PO", confidence=0.9), "heuristic")
    if "epinephrine" in t or " epi " in f" {t} ":
        return _emit(ParsedAction("intervention", text, intervention="epinephrine IM", confidence=0.9), "heuristic")
    if any(k in t for k in ["oxygen","nasal cannula","non-rebreather","nrb","bvm","bag valve","bag-valve","15 lpm"]):
        return _emit(ParsedAction("intervention", text, intervention="oxygen", confidence=0.9), "heuristic")
    if any(k in t for k in ["albuterol","salbutamol","duoneb","neb","nebulizer"]):
        return _emit(ParsedAction("intervention", text, intervention="albuterol neb", confidence=0.9), "heuristic")

    # diagnostics
    if any(k in t for k in ["ecg","ekg","12-lead","12 lead"]):
        return _emit(ParsedAction("diagnostic", text, test_name="ECG", confidence=0.8), "heuristic")
    if "glucose" in t or "dexi" in t or "fingerstick" in t:
        return _emit(ParsedAction("diagnostic", text, test_name="glucose", confidence=0.8), "heuristic")

    # physical exam
    if any(k in t for k in ["listen to lungs","lung sounds","auscultation","breath sounds"]):
        return _emit(ParsedAction("physical_exam", text, body_region="chest", confidence=0.8), "heuristic")

    # onset/LKW
    if any(k in t for k in ["onset","when did","how long","last known well","lkw"]):
        return _emit(ParsedAction("history", text, symptom="onset time", confidence=0.8), "heuristic")

    # common symptom probes
    symptoms = {
        "chest pain": ["chest pain","pressure in chest"],
        "shortness of breath": ["short of breath","sob","dyspnea","trouble breathing"],
        "nausea": ["nausea","nauseated"],
        "wheezing": ["wheezing","wheeze"],
        "pain radiation to left arm": ["left arm pain","radiate to arm"],
        "jaw pain radiation": ["jaw pain","radiate to jaw"],
        "unilateral weakness": ["one sided weakness","right side weak","left side weak","hemiparesis"],
        "speech difficulty": ["slurred speech","aphasia","trouble speaking"],
        "facial droop": ["face droop","uneven smile"],
        "hives": ["hives","urticaria"],
        "stridor": ["stridor"]
    }
    for canon, variants in symptoms.items():
        if any(v in t for v in variants):
            return _emit(ParsedAction("history", text, symptom=canon, confidence=0.8), "heuristic")

    return _emit(ParsedAction("meta", text, confidence=0.4), "heuristic")

def _try_llm(text: str):
    if os.getenv("USE_LLM","0").lower() in ("1","true","yes"):
        try:
            from llm_backend import llm_parse_action
            parsed = llm_parse_action(text) or {}
            parsed.setdefault("free_text", text)
            parsed.setdefault("confidence", 0.6)
            parsed["_source"] = "llm"
            return parsed
        except Exception:
            pass
    return None

def parse(text: str) -> Dict[str, Any]:
    # 1) LLM first
    p = _try_llm(text)
    if p is not None:
        at = p.get("action_type", "meta")
        conf = float(p.get("confidence", 0))
        # If the LLM was unsure, try heuristics as a rescue
        if at == "meta" or conf < 0.75:
            h = _heuristic(text)
            if h.get("action_type") != "meta":
                h["_source"] = "llm+heuristic"
                return h
        return p
    # 2) Heuristic fallback
    return _heuristic(text)
