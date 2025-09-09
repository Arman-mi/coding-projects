# run_demo.py - quick CLI to test the pipeline
# Usage:
#   python run_demo.py emt_sim.db
import sys, json
from db import DB
from engine import Engine
from llm_parser import parse
from grader import grade_run

def main(db_path="emt_sim.db"):
    db = DB(db_path)
    scenarios = db.get_scenarios()
    assert scenarios, "No scenarios found. Run setup_emt_db.py first."
    sc = scenarios[0]
    run_id = db.create_run(sc["id"])

    print(f"Scenario: {sc['title']}  (disease_id={sc['disease_id']})")
    eng = Engine(db, run_id)

    while True:
        try:
            q = input("\nYou: ")
        except EOFError:
            break
        if not q or q.strip().lower() in ("quit","exit"):
            break
        parsed = parse(q)
        out = eng.step(parsed)
        print("Patient:", out["reply_text"])

    # Show action log at the end
    print("\n--- Action Log ---")
    for row in db.list_actions(run_id):
        a = json.loads(row["action"])
        r = json.loads(row["response"])
        print(f"{row['id']:02d}. action={a.get('action_type')} | reply={r.get('reply_text')}")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv)>1 else "emt_sim.db")

    # Grade the run
    from grader import grade_run
    report = grade_run(db, run_id)
    print("\n--- Score ---")
    print(f"Disease: {report['disease']}")
    print(f"Score: {report['score']:.1f} / {report['max_score']:.1f} ({report['percent']}%)")
    print("Details:")
    for d in report["details"]:
        mark = "✔" if d["met"] else "✘"
        print(f"  {mark} {d['code']}: +{d['awarded']:.1f}/{d['weight']:.1f} — {d['rationale']}")
    print("\n" + report["narrative"])
