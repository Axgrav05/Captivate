import json

SOURCE = "output/week1_claim_eval_llm.json"
DEST = "output/week1_claim_eval_llm_subset.json"
IDS_TO_KEEP = ["002", "007", "014", "021", "026"]  

with open(SOURCE) as f:
    all_entries = json.load(f)

subset = [entry for entry in all_entries if entry["id"] in IDS_TO_KEEP]

with open(DEST, "w") as f:
    json.dump(subset, f, indent=2)

print(f"✅ Wrote {len(subset)} entries to {DEST}")
