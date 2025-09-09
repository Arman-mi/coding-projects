# db.py - thin SQLite helper for EMT sim
import sqlite3, uuid, json
from typing import Optional, Dict, Any, Tuple, List

class DB:
    def __init__(self, path: str = "emt_sim.db"):
        self.path = path
        self.con = sqlite3.connect(self.path, check_same_thread=False)
        self.con.row_factory = sqlite3.Row

    # ---------- generic helpers ----------
    def _one(self, q: str, args: tuple = ()) -> Optional[sqlite3.Row]:
        cur = self.con.execute(q, args)
        return cur.fetchone()

    def _all(self, q: str, args: tuple = ()) -> list:
        cur = self.con.execute(q, args)
        return cur.fetchall()

    def _exec(self, q: str, args: tuple = ()) -> None:
        self.con.execute(q, args)
        self.con.commit()

    # ---------- scenarios / runs ----------
    def get_scenarios(self) -> list:
        return self._all("SELECT * FROM scenario ORDER BY id")

    def get_scenario(self, scenario_id: int) -> Optional[sqlite3.Row]:
        return self._one("SELECT * FROM scenario WHERE id=?", (scenario_id,))

    def get_disease_for_scenario(self, scenario_id: int) -> Optional[sqlite3.Row]:
        return self._one("""
            SELECT d.* FROM disease d
            JOIN scenario s ON s.disease_id = d.id
            WHERE s.id=?
        """, (scenario_id,))

    def create_run(self, scenario_id: int, vitals: Optional[Dict[str,Any]] = None, state: Optional[Dict[str,Any]] = None) -> str:
        run_id = str(uuid.uuid4())
        vitals_json = json.dumps(vitals or {})
        state_json = json.dumps(state or {})
        self._exec("INSERT INTO run(id, scenario_id, vitals, state) VALUES (?,?,?,?)",
                   (run_id, scenario_id, vitals_json, state_json))
        return run_id

    def get_run(self, run_id: str) -> Optional[sqlite3.Row]:
        return self._one("SELECT * FROM run WHERE id=?", (run_id,))

    def get_run_state(self, run_id: str) -> Dict[str,Any]:
        row = self.get_run(run_id)
        return json.loads(row["state"] or "{}") if row else {}

    def get_run_vitals(self, run_id: str) -> Dict[str,Any]:
        row = self.get_run(run_id)
        return json.loads(row["vitals"] or "{}") if row else {}

    def update_run_state(self, run_id: str, state: Dict[str, Any]):
        self._exec("UPDATE run SET state=? WHERE id=?", (json.dumps(state), run_id))

    def update_run_vitals(self, run_id: str, vitals: Dict[str, Any]):
        self._exec("UPDATE run SET vitals=? WHERE id=?", (json.dumps(vitals), run_id))

    # ---------- symptoms & aliases ----------
    def lookup_symptom(self, name_or_alias: str) -> Optional[sqlite3.Row]:
        name = (name_or_alias or "").strip().lower()
        row = self._one("SELECT * FROM symptom WHERE lower(name)=?", (name,))
        if row: return row
        row = self._one("""
            SELECT s.* FROM symptom s
            JOIN symptom_alias a ON a.symptom_id=s.id
            WHERE lower(a.alias)=?
        """, (name,))
        return row

    def disease_symptom_mapping(self, disease_id: int, symptom_id: int) -> Optional[sqlite3.Row]:
        return self._one("""
            SELECT * FROM disease_symptom 
            WHERE disease_id=? AND symptom_id=?
        """, (disease_id, symptom_id))

    # ---------- logging & grading ----------
    def log_action(self, run_id: str, action: Dict[str,Any], response: Dict[str,Any]) -> int:
        cur = self.con.execute(
            "INSERT INTO action_log(run_id, action, response) VALUES (?,?,?)",
            (run_id, json.dumps(action), json.dumps(response))
        )
        self.con.commit()
        return cur.lastrowid

    def list_actions(self, run_id: str) -> List[sqlite3.Row]:
        return self._all("SELECT * FROM action_log WHERE run_id=? ORDER BY id ASC", (run_id,))

    # ---------- utilities ----------
    def get_disease_by_id(self, disease_id: int) -> Optional[sqlite3.Row]:
        return self._one("SELECT * FROM disease WHERE id=?", (disease_id,))

    def get_disease_for_run(self, run_id: str) -> Optional[sqlite3.Row]:
        return self._one("""
            SELECT d.* FROM disease d
            JOIN scenario s ON s.disease_id=d.id
            JOIN run r ON r.scenario_id=s.id
            WHERE r.id=?
        """, (run_id,))