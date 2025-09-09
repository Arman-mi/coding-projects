# grader.py - evaluates a run using action_log and rubric in the DB
from typing import Dict, Any, List
import json
from db import DB

def _normalize_text(s: str) -> str:
    return (s or "").lower().strip()

def _first_three_actions(actions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return actions[:3]

def _load_actions(db: DB, run_id: str) -> List[Dict[str, Any]]:
    out = []
    for row in db.list_actions(run_id):
        a = json.loads(row["action"])
        out.append(a)
    return out

def _disease_name(db: DB, run_id: str) -> str:
    d = db.get_disease_for_run(run_id)
    return d["name"] if d else ""

def _load_vitals(db: DB, run_id: str):
    row = db.get_run(run_id)
    return json.loads(row["vitals"] or "{}") if row else {}

def grade_run(db: DB, run_id: str) -> Dict[str, Any]:
    # Fetch rubric items
    rubrics = {}
    for row in db._all("SELECT code, description, weight FROM rubric_item"):
        rubrics[row["code"]] = dict(description=row["description"], weight=row["weight"])

    actions = _load_actions(db, run_id)
    disease = _disease_name(db, run_id)

    def any_vitals_request() -> bool:
        return any(a.get("action_type") == "vitals_request" for a in actions)

    def asked_onset() -> bool:
        for a in actions:
            if a.get("action_type") == "history":
                if _normalize_text(a.get("symptom","")) == "onset time":
                    return True
                ft = _normalize_text(a.get("free_text",""))
                if any(k in ft for k in ["onset", "last known well", "lkw"]):
                    return True
        return False

    def gave_aspirin() -> bool:
        if "stemi" not in _normalize_text(disease):
            return False
        for a in actions:
            if a.get("action_type") == "intervention":
                ft = _normalize_text(a.get("free_text","")) + " " + _normalize_text(a.get("intervention",""))
                if "aspirin" in ft:
                    return True
        return False

    def gave_epinephrine() -> bool:
        if "anaphylaxis" not in _normalize_text(disease):
            return False
        for a in actions:
            if a.get("action_type") == "intervention":
                ft = _normalize_text(a.get("free_text","")) + " " + _normalize_text(a.get("intervention",""))
                if "epinephrine" in ft or " epi " in (" " + ft + " "):
                    return True
        return False

    def activated_stroke_alert() -> bool:
        if "stroke" not in _normalize_text(disease):
            return False
        for a in actions:
            ft = _normalize_text(a.get("free_text",""))
            if a.get("action_type") == "management" and any(k in ft for k in ["stroke alert","code stroke","activate stroke"]):
                return True
            if any(k in ft for k in ["stroke alert","code stroke","activate stroke"]):
                return True
        return False

    def abcs_first() -> bool:
        first_three = _first_three_actions(actions)
        if not first_three:
            return False
        for a in first_three:
            if a.get("action_type") == "vitals_request":
                return True
            ft = _normalize_text(a.get("free_text",""))
            if any(k in ft for k in ["airway","breathing","circulation","abcs","abc","check airway","check breathing","check circulation"]):
                return True
        return False

    # NEW checks
    def oxygen_for_hypoxia() -> bool:
        v = _load_vitals(db, run_id)
        spo2 = v.get("spo2")
        if spo2 is None or spo2 >= 94:
            return False
        for a in actions:
            if a.get("action_type") == "intervention":
                ft = _normalize_text(a.get("free_text","")) + " " + _normalize_text(a.get("intervention",""))
                if any(k in ft for k in ["oxygen","nasal cannula","non-rebreather","nrb","bvm","bag valve","bag-valve"]):
                    return True
        return False

    def bronchodilator_for_asthma() -> bool:
        if "asthma exacerbation" not in _normalize_text(disease):
            return False
        for a in actions:
            if a.get("action_type") == "intervention":
                ft = _normalize_text(a.get("free_text","")) + " " + _normalize_text(a.get("intervention",""))
                if any(k in ft for k in ["albuterol","salbutamol","duoneb","neb","nebulizer"]):
                    return True
        return False

    def glucose_check_for_neuro() -> bool:
        if "stroke" not in _normalize_text(disease):
            return False
        for a in actions:
            if a.get("action_type") == "diagnostic":
                ft = _normalize_text(a.get("test_name","")) + " " + _normalize_text(a.get("free_text",""))
                if "glucose" in ft or "dexi" in ft:
                    return True
        return False

    checks = {
        "ABCs_first": (abcs_first, "Prioritized ABCs early."),
        "request_vitals": (any_vitals_request, "Requested a full set of vitals."),
        "ask_onset": (asked_onset, "Established time of onset/LKW."),
        "aspirin_for_stemi": (gave_aspirin, "Gave aspirin for suspected STEMI."),
        "epi_for_anaphylaxis": (gave_epinephrine, "Administered IM epinephrine for anaphylaxis."),
        "stroke_alert": (activated_stroke_alert, "Activated stroke alert for suspected stroke."),
        # new items:
        "oxygen_for_hypoxia": (oxygen_for_hypoxia, "Applied oxygen for hypoxia."),
        "bronchodilator_for_asthma": (bronchodilator_for_asthma, "Gave bronchodilator for asthma exacerbation."),
        "glucose_check_for_neuro": (glucose_check_for_neuro, "Checked glucose in neuro deficits.")
    }

    # ---------- Applicability gate ----------
    def _applicable(code: str, disease_name: str, db: DB, run_id: str) -> bool:
        d = _normalize_text(disease_name)
        # disease-specific
        if code == "aspirin_for_stemi":
            return "stemi" in d
        if code == "epi_for_anaphylaxis":
            return "anaphylaxis" in d
        if code == "stroke_alert":
            return "stroke" in d
        if code == "bronchodilator_for_asthma":
            return "asthma" in d  # covers "asthma exacerbation"
        if code == "glucose_check_for_neuro":
            return "stroke" in d
        # state-specific
        if code == "oxygen_for_hypoxia":
            v = _load_vitals(db, run_id)
            spo2 = v.get("spo2")
            return (spo2 is not None) and (spo2 < 94)
        # generic items always apply
        return code in {"ABCs_first", "request_vitals", "ask_onset"}

    # ---------- Scoring ----------
    details, total, max_total = [], 0.0, 0.0
    for code, meta in rubrics.items():
        fn_desc = checks.get(code)
        if not fn_desc:
            continue

        if not _applicable(code, disease, db, run_id):
            details.append({
                "code": code,
                "met": None,                 # N/A
                "weight": meta["weight"] or 0.0,
                "awarded": 0.0,
                "rationale": "Not applicable"
            })
            continue  # do NOT add to max_total

        weight = meta["weight"] or 0.0
        max_total += weight
        fn, success_text = fn_desc
        ok = bool(fn())
        pts = weight if ok else 0.0
        total += pts
        details.append({
            "code": code,
            "met": ok,
            "weight": weight,
            "awarded": pts,
            "rationale": success_text if ok else f"Missed: {meta['description']}"
        })

    positives = [d["rationale"] for d in details if d["met"] is True]
    misses = [d["rationale"] for d in details if d["met"] is False]
    narrative = []
    if positives: narrative.append("What you did well: " + "; ".join(positives) + ".")
    if misses: narrative.append("Opportunities: " + "; ".join(misses) + ".")

    return {
        "disease": disease,
        "score": total,
        "max_score": max_total,
        "percent": round(100.0 * total / max_total, 1) if max_total > 0 else 0.0,
        "details": details,
        "narrative": " ".join(narrative)
    }
