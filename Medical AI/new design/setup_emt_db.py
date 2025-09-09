# setup_emt_db.py
# Creates an EMT simulation SQLite DB with schema + seed data.
# Usage:
#   python setup_emt_db.py           # creates emt_sim.db in current folder
#   python setup_emt_db.py /path/to/emt_sim.db

import sqlite3, sys

DB_PATH = sys.argv[1] if len(sys.argv) > 1 else "emt_sim.db"

SCHEMA_SQL = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS disease(
  id INTEGER PRIMARY KEY,
  name TEXT UNIQUE NOT NULL,
  category TEXT,
  acuity TEXT,
  notes TEXT
);

CREATE TABLE IF NOT EXISTS symptom(
  id INTEGER PRIMARY KEY,
  name TEXT UNIQUE NOT NULL,
  body_region TEXT,
  kind TEXT CHECK(kind IN ('history','exam','vital','test','ros'))
);

CREATE TABLE IF NOT EXISTS symptom_alias(
  symptom_id INT REFERENCES symptom(id) ON DELETE CASCADE,
  alias TEXT NOT NULL,
  PRIMARY KEY (symptom_id, alias)
);

CREATE TABLE IF NOT EXISTS disease_symptom(
  disease_id INT REFERENCES disease(id) ON DELETE CASCADE,
  symptom_id INT REFERENCES symptom(id) ON DELETE CASCADE,
  typicality REAL,                 -- 0..1 how characteristic
  sensitivity REAL,
  specificity REAL,
  default_answer TEXT,
  PRIMARY KEY(disease_id, symptom_id)
);

CREATE TABLE IF NOT EXISTS vital_norms(
  id INTEGER PRIMARY KEY,
  age_min INT, age_max INT,
  systolic_min INT, systolic_max INT,
  diastolic_min INT, diastolic_max INT,
  hr_min INT, hr_max INT,
  rr_min INT, rr_max INT,
  spo2_min REAL, spo2_max REAL
);

CREATE TABLE IF NOT EXISTS scenario(
  id INTEGER PRIMARY KEY,
  title TEXT,
  disease_id INT REFERENCES disease(id) ON DELETE SET NULL,
  chief_complaint TEXT,
  onset_minutes INT,
  difficulty TEXT,
  seed INT
);

CREATE TABLE IF NOT EXISTS run(
  id TEXT PRIMARY KEY,
  scenario_id INT REFERENCES scenario(id) ON DELETE SET NULL,
  started_at TEXT DEFAULT (datetime('now')),
  minute INT DEFAULT 0,
  vitals TEXT,                  -- JSON
  state TEXT                    -- JSON
);

CREATE TABLE IF NOT EXISTS action_log(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  run_id TEXT REFERENCES run(id) ON DELETE CASCADE,
  t TEXT DEFAULT (datetime('now')),
  action TEXT,                  -- JSON
  response TEXT                 -- JSON
);

CREATE TABLE IF NOT EXISTS rubric_item(
  id INTEGER PRIMARY KEY,
  code TEXT UNIQUE,
  description TEXT,
  weight REAL
);

CREATE TABLE IF NOT EXISTS rubric_trigger(
  rubric_id INT REFERENCES rubric_item(id) ON DELETE CASCADE,
  when_expr TEXT,
  PRIMARY KEY (rubric_id, when_expr)
);
"""

SEED = {
    "diseases": [
        {"name":"STEMI (Acute MI)","category":"cardiac","acuity":"time-critical",
         "notes":"Treat with MONA per protocol; consider cath activation."},
        {"name":"Ischemic Stroke","category":"neuro","acuity":"time-critical",
         "notes":"Time last known well critical; stroke alert if within window."},
        {"name":"Asthma Exacerbation","category":"respiratory","acuity":"urgent",
         "notes":"Bronchodilators, steroids; assess for silent chest."},
        {"name":"Anaphylaxis","category":"allergy/immunology","acuity":"time-critical",
         "notes":"IM epinephrine first; airway readiness."}
    ],
    "symptoms": [
        # history
        {"name":"chest pain","body_region":"chest","kind":"history"},
        {"name":"pain radiation to left arm","body_region":"chest","kind":"history"},
        {"name":"jaw pain radiation","body_region":"head/neck","kind":"history"},
        {"name":"shortness of breath","body_region":"chest","kind":"history"},
        {"name":"nausea","body_region":"gi","kind":"history"},
        {"name":"onset time","body_region":"general","kind":"history"},
        {"name":"unilateral weakness","body_region":"neuro","kind":"history"},
        {"name":"facial droop","body_region":"neuro","kind":"history"},
        {"name":"speech difficulty","body_region":"neuro","kind":"history"},
        {"name":"wheezing","body_region":"chest","kind":"history"},
        {"name":"exposure to allergen","body_region":"general","kind":"history"},
        # exam
        {"name":"diaphoresis","body_region":"general","kind":"exam"},
        {"name":"wheezes on auscultation","body_region":"chest","kind":"exam"},
        {"name":"hives","body_region":"skin","kind":"exam"},
        {"name":"stridor","body_region":"airway","kind":"exam"},
        {"name":"unequal smile","body_region":"neuro","kind":"exam"},
        # vitals (labels)
        {"name":"blood pressure","body_region":"vitals","kind":"vital"},
        {"name":"heart rate","body_region":"vitals","kind":"vital"},
        {"name":"respiratory rate","body_region":"vitals","kind":"vital"},
        {"name":"spo2","body_region":"vitals","kind":"vital"},
        # tests
        {"name":"ECG ST elevation","body_region":"cardiac","kind":"test"},
        {"name":"glucose","body_region":"lab","kind":"test"}
    ],
    "aliases": {
        "shortness of breath": ["sob","dyspnea","trouble breathing"],
        "wheezes on auscultation": ["wheezes","wheezing on exam"],
        "spo2": ["oxygen saturation","pulse ox","sat"],
        "blood pressure": ["bp"],
        "heart rate": ["hr","pulse"],
        "respiratory rate": ["rr"],
        "speech difficulty": ["aphasia","slurred speech"],
        "unilateral weakness": ["one-sided weakness","hemiparesis"]
    },
    "disease_symptom": {
        "STEMI (Acute MI)": {
            "chest pain": (0.95, 0.80, 0.70, "Pressure-like, substernal."),
            "pain radiation to left arm": (0.80, 0.60, 0.75, "Radiates to left arm."),
            "jaw pain radiation": (0.40, 0.30, 0.85, "Occasional radiation to jaw."),
            "shortness of breath": (0.60, 0.50, 0.60, "Feels winded."),
            "nausea": (0.50, 0.40, 0.70, "Feels nauseated."),
            "diaphoresis": (0.70, 0.60, 0.65, "Sweaty, clammy."),
            "ECG ST elevation": (0.95, 0.80, 0.95, "ST elevation in contiguous leads.")
        },
        "Ischemic Stroke": {
            "unilateral weakness": (0.90, 0.80, 0.85, "Right arm and leg weak."),
            "facial droop": (0.80, 0.70, 0.90, "Left facial droop."),
            "speech difficulty": (0.70, 0.60, 0.80, "Words are slurred."),
            "glucose": (0.10, 0.10, 0.90, "Glucose 110 mg/dL")
        },
        "Asthma Exacerbation": {
            "shortness of breath": (0.95, 0.90, 0.50, "Tight chest, worse on exertion."),
            "wheezing": (0.90, 0.85, 0.60, "Audible wheeze."),
            "wheezes on auscultation": (0.95, 0.90, 0.60, "Diffuse expiratory wheezes.")
        },
        "Anaphylaxis": {
            "exposure to allergen": (0.85, 0.80, 0.80, "Peanut cookie just before symptoms."),
            "shortness of breath": (0.80, 0.75, 0.60, "Throat feels tight."),
            "hives": (0.80, 0.70, 0.85, "Generalized urticaria."),
            "stridor": (0.30, 0.20, 0.95, "Inspiratory stridor present.")
        }
    },
    "vital_norms": [
        {"age_min":18,"age_max":65,"systolic_min":100,"systolic_max":139,"diastolic_min":60,"diastolic_max":89,
         "hr_min":60,"hr_max":100,"rr_min":12,"rr_max":20,"spo2_min":95.0,"spo2_max":100.0}
    ],
    "scenarios": [
        {"title":"Crushing chest pain while mowing","disease":"STEMI (Acute MI)","chief_complaint":"Severe chest pain",
         "onset_minutes":45,"difficulty":"medium","seed":123},
        {"title":"Sudden right-sided weakness","disease":"Ischemic Stroke","chief_complaint":"Weakness and slurred speech",
         "onset_minutes":60,"difficulty":"hard","seed":321},
        {"title":"Tight chest after dust exposure","disease":"Asthma Exacerbation","chief_complaint":"Shortness of breath",
         "onset_minutes":30,"difficulty":"easy","seed":111},
        {"title":"Hives and throat tightness post peanut","disease":"Anaphylaxis","chief_complaint":"Difficulty breathing",
         "onset_minutes":10,"difficulty":"hard","seed":222}
    ],
    "rubric": [
        ("ABCs_first","Assess airway, breathing, circulation early", 3.0),
        ("request_vitals","Request a full set of vitals", 2.0),
        ("ask_onset","Ask time of onset / LKW", 2.0),
        ("aspirin_for_stemi","Administer aspirin when STEMI, no contraindications", 3.0),
        ("epi_for_anaphylaxis","Administer IM epinephrine promptly in anaphylaxis", 3.0),
        ("stroke_alert","Activate stroke alert for suspected stroke within window", 3.0)
    ],
    "rubric_triggers": [
        ("ABCs_first","first_three_actions_include_any_of(['airway','breathing','circulation','vitals_request'])"),
        ("request_vitals","any_action_equals('vitals_request')"),
        ("ask_onset","history_contains('onset time')"),
        ("aspirin_for_stemi","disease_is('STEMI (Acute MI)') and action_contains('intervention','aspirin')"),
        ("epi_for_anaphylaxis","disease_is('Anaphylaxis') and action_contains('intervention','epinephrine')"),
        ("stroke_alert","disease_is('Ischemic Stroke') and action_contains('management','stroke alert')")
    ]
}

def run():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.executescript(SCHEMA_SQL)

    # Diseases
    for d in SEED["diseases"]:
        cur.execute("INSERT OR IGNORE INTO disease(name, category, acuity, notes) VALUES (?,?,?,?)",
                    (d["name"], d.get("category"), d.get("acuity"), d.get("notes")))

    # Symptoms
    for s in SEED["symptoms"]:
        cur.execute("INSERT OR IGNORE INTO symptom(name, body_region, kind) VALUES (?,?,?)",
                    (s["name"], s.get("body_region"), s.get("kind")))

    # Aliases
    for canon, aliases in SEED["aliases"].items():
        cur.execute("SELECT id FROM symptom WHERE name=?", (canon,))
        row = cur.fetchone()
        if row:
            sid = row[0]
            for a in aliases:
                cur.execute("INSERT OR IGNORE INTO symptom_alias(symptom_id, alias) VALUES (?,?)", (sid, a))

    # Disease ↔ symptom links
    for dname, mapping in SEED["disease_symptom"].items():
        cur.execute("SELECT id FROM disease WHERE name=?", (dname,))
        drow = cur.fetchone()
        if not drow:
            continue
        did = drow[0]
        for sname, (typ, sens, spec, ans) in mapping.items():
            cur.execute("SELECT id FROM symptom WHERE name=?", (sname,))
            srow = cur.fetchone()
            if srow:
                sid = srow[0]
                cur.execute(
                    "INSERT OR REPLACE INTO disease_symptom(disease_id, symptom_id, typicality, sensitivity, specificity, default_answer) VALUES (?,?,?,?,?,?)",
                    (did, sid, typ, sens, spec, ans))

    # Vitals norms
    for v in SEED["vital_norms"]:
        cur.execute("""
            INSERT OR IGNORE INTO vital_norms(age_min,age_max,systolic_min,systolic_max,diastolic_min,diastolic_max,hr_min,hr_max,rr_min,rr_max,spo2_min,spo2_max)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        """, (v["age_min"],v["age_max"],v["systolic_min"],v["systolic_max"],v["diastolic_min"],v["diastolic_max"],
              v["hr_min"],v["hr_max"],v["rr_min"],v["rr_max"],v["spo2_min"],v["spo2_max"]))

    # Scenarios
    for sc in SEED["scenarios"]:
        cur.execute("SELECT id FROM disease WHERE name=?", (sc["disease"],))
        drow = cur.fetchone()
        did = drow[0] if drow else None
        cur.execute(
            "INSERT OR IGNORE INTO scenario(title, disease_id, chief_complaint, onset_minutes, difficulty, seed) VALUES (?,?,?,?,?,?)",
            (sc["title"], did, sc["chief_complaint"], sc["onset_minutes"], sc["difficulty"], sc["seed"])
        )

    # Rubric items
    for i, (code, desc, w) in enumerate(SEED["rubric"], start=1):
        cur.execute("INSERT OR IGNORE INTO rubric_item(id, code, description, weight) VALUES (?,?,?,?)",
                    (i, code, desc, w))

    # Rubric triggers
    for code, expr in SEED["rubric_triggers"]:
        cur.execute("SELECT id FROM rubric_item WHERE code=?", (code,))
        r = cur.fetchone()
        if r:
            cur.execute("INSERT OR IGNORE INTO rubric_trigger(rubric_id, when_expr) VALUES (?,?)", (r[0], expr))

    con.commit()

    # Quick summary
    summary = {}
    for t in ["disease","symptom","symptom_alias","disease_symptom","scenario","vital_norms","rubric_item","rubric_trigger"]:
        cur.execute(f"SELECT COUNT(*) FROM {t}")
        summary[t] = cur.fetchone()[0]

    con.close()
    print(f"Database created: {DB_PATH}")
    for k, v in summary.items():
        print(f"{k:18} {v}")

if __name__ == "__main__":
    run()
