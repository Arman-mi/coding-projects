# engine.py - deterministic patient engine using DB + vitals drift/effects
from typing import Dict, Any
import re
from db import DB

class Engine:
    def __init__(self, db: DB, run_id: str):
        self.db = db
        self.run_id = run_id

    # ---- public entry point ----
    def step(self, parsed: Dict[str, Any]) -> Dict[str, Any]:
        # advance time & drift vitals each step
        self._progress_state()

        disease = self.db.get_disease_for_run(self.run_id)
        state = self.db.get_run_state(self.run_id)
        vitals = self.db.get_run_vitals(self.run_id)

        action_type = parsed.get("action_type")
        reply = {"reply_text": "I'm not sure what you want to assess.", "observations": {}, "state_updates": {}}

        if action_type == "vitals_request":
            if not vitals:
                vitals = self._baseline_vitals(disease["name"] if disease else None)
                self.db.update_run_vitals(self.run_id, vitals)
            reply["reply_text"] = self._format_vitals(vitals)
            reply["observations"]["vitals"] = vitals

        elif action_type in ("history","ros"):
            answer = self._history_or_ros_answer(disease, parsed)
            reply["reply_text"] = answer

        elif action_type == "physical_exam":
            ans = self._exam_answer(disease, parsed)
            reply["reply_text"] = ans

        elif action_type == "intervention":
            ans = self._apply_intervention(state, parsed, disease)
            reply["reply_text"] = ans
            self.db.update_run_state(self.run_id, state)

        elif action_type in ("diagnostic","management","meta"):
            ans = self._generic_ack(parsed)
            reply["reply_text"] = ans

        # log & return
        self.db.log_action(self.run_id, parsed, reply)
        return reply

    # ---- private helpers ----
    def _format_vitals(self, v: Dict[str, Any]) -> str:
        return f"BP {v.get('bp','?')}, HR {v.get('hr','?')}, RR {v.get('rr','?')}, SpO2 {v.get('spo2','?')}%."

    def _baseline_vitals(self, disease_name: str) -> Dict[str, Any]:
        presets = {
            "STEMI (Acute MI)": dict(bp="150/90", hr=98, rr=20, spo2=94),
            "Ischemic Stroke": dict(bp="180/100", hr=84, rr=18, spo2=96),
            "Asthma Exacerbation": dict(bp="130/80", hr=110, rr=28, spo2=91),
            "Anaphylaxis": dict(bp="88/54", hr=122, rr=26, spo2=89),
        }
        return presets.get(disease_name, dict(bp="128/78", hr=82, rr=16, spo2=97))

    def _history_or_ros_answer(self, disease_row, parsed) -> str:
        # Special case: onset time
        if (parsed.get("symptom","") or "").lower() in ("onset time","time of onset","last known well","lkw"):
            run = self.db.get_run(self.run_id)
            sc = self.db.get_scenario(run["scenario_id"]) if run else None
            mins = sc["onset_minutes"] if sc else None
            return f"Started about {mins} minutes ago." if mins is not None else "Not sure."

        sym_name = parsed.get("symptom") or parsed.get("free_text","")
        sym_row = self.db.lookup_symptom(sym_name)
        if disease_row and sym_row:
            link = self.db.disease_symptom_mapping(disease_row["id"], sym_row["id"])
            if link and link["default_answer"]:
                return link["default_answer"]
        return "No significant history related to that."

    def _exam_answer(self, disease_row, parsed) -> str:
        region = (parsed.get("body_region") or "").lower()
        candidates = []
        if disease_row:
            rows = self.db._all("""
                SELECT s.name, ds.default_answer
                FROM disease_symptom ds
                JOIN symptom s ON s.id=ds.symptom_id
                WHERE ds.disease_id=? AND s.kind='exam'
                ORDER BY ds.typicality DESC
            """, (disease_row["id"],))
            for r in rows:
                if not region or region in (r["name"].lower() + " " + region):
                    candidates.append(r)
        if candidates:
            return candidates[0]["default_answer"] or f"Exam shows: {candidates[0]['name']}."
        return "Exam is unremarkable in that area."

    def _apply_intervention(self, state: Dict[str,Any], parsed: Dict[str,Any], disease_row) -> str:
        name = (parsed.get("intervention") or parsed.get("free_text") or "").lower()
        if "aspirin" in name:
            state["aspirin_given"] = True
            state["last_intervention"] = name
            return "Aspirin given."
        if "epinephrine" in name or re.search(r'\bepi\b', name):
            state["epinephrine_given"] = True
            state["last_intervention"] = name
            return "Epinephrine administered."
        if any(k in name for k in ["oxygen","nasal cannula","non-rebreather","nrb","bvm","bag-valve","bag valve"]):
            state["oxygen_given"] = True
            state["last_intervention"] = name
            return "Oxygen applied."
        if any(k in name for k in ["albuterol","salbutamol","neb","nebulizer","duoneb"]):
            state["albuterol_given"] = True
            state["last_intervention"] = name
            return "Nebulized bronchodilator given."
        state["last_intervention"] = name
        return "Intervention noted."

    def _generic_ack(self, parsed) -> str:
        t = parsed.get("action_type")
        if t == "diagnostic":
            test = parsed.get("test_name") or "the test"
            return f"Ordered {test}."
        if t == "management":
            return "Management step acknowledged."
        if t == "meta":
            return ("I can help with: vitals; history (e.g., onset time/LKW); "
                    "physical exam (e.g., lung sounds); diagnostics (ECG, glucose); "
                    "interventions (aspirin, epinephrine, oxygen, albuterol); "
                    "or management (e.g., stroke alert). What would you like to do?")
        return "Okay."

    def _progress_state(self):
        """Advance minute counter and drift vitals by disease; apply intervention effects."""
        run = self.db.get_run(self.run_id)
        disease = self.db.get_disease_for_run(self.run_id)
        state = self.db.get_run_state(self.run_id)
        vitals = self.db.get_run_vitals(self.run_id) or self._baseline_vitals(disease["name"] if disease else None)

        # Increment minute
        minute = (run["minute"] if run else 0) or 0
        minute += 1
        self.db._exec("UPDATE run SET minute=? WHERE id=?", (minute, self.run_id))

        name = (disease["name"] if disease else "")

        # Simple drift rules by disease
        if "STEMI" in name:
            vitals["hr"] = min(140, int(vitals.get("hr", 90) + 1))
            vitals["rr"] = min(30, int(vitals.get("rr", 18) + 0.2))
        elif "Stroke" in name:
            vitals["bp"] = vitals.get("bp", "180/100")
        elif "Asthma" in name:
            vitals["rr"] = min(40, int(vitals.get("rr", 24) + 0.3))
            vitals["spo2"] = max(85, int(vitals.get("spo2", 92) - 1))
        elif "Anaphylaxis" in name:
            if not state.get("epinephrine_given"):
                try:
                    sys, dia = map(int, str(vitals.get("bp", "88/54")).split("/"))
                except Exception:
                    sys, dia = 88, 54
                sys = max(70, sys - 1)
                dia = max(40, dia - 1)
                vitals["bp"] = f"{sys}/{dia}"
                vitals["spo2"] = max(82, int(vitals.get("spo2", 90) - 1))

        # Intervention effects
        if state.get("oxygen_given"):
            vitals["spo2"] = min(100, int(vitals.get("spo2", 92) + 3))
        if state.get("epinephrine_given"):
            try:
                sys, dia = map(int, str(vitals.get("bp", "90/60")).split("/"))
            except Exception:
                sys, dia = 90, 60
            sys = min(120, sys + 5)
            dia = min(80, dia + 3)
            vitals["bp"] = f"{sys}/{dia}"
            vitals["spo2"] = min(99, int(vitals.get("spo2", 88) + 4))
            vitals["hr"] = min(140, int(vitals.get("hr", 100) + 2))
        if state.get("albuterol_given"):
            vitals["rr"] = max(16, int(vitals.get("rr", 26) - 2))
            vitals["spo2"] = min(99, int(vitals.get("spo2", 90) + 2))

        self.db.update_run_vitals(self.run_id, vitals)
