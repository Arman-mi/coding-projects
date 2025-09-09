# upgrade_rubric_v2.py — adds new rubric items
import sqlite3, sys
DB_PATH = sys.argv[1] if len(sys.argv) > 1 else "emt_sim.db"
items = [
    ("oxygen_for_hypoxia","Apply oxygen when SpO2 < 94%", 2.0),
    ("bronchodilator_for_asthma","Give bronchodilator for asthma exacerbation", 2.0),
    ("glucose_check_for_neuro","Check glucose in patients with neuro deficits", 2.0),
]
con = sqlite3.connect(DB_PATH); cur = con.cursor()
for code, desc, w in items:
    cur.execute("INSERT OR IGNORE INTO rubric_item(code, description, weight) VALUES (?,?,?)", (code, desc, w))
con.commit(); print("Added/kept rubric items:", [code for code,_,_ in items]); con.close()
