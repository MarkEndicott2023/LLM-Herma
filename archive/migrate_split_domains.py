#!/usr/bin/env python3
"""One-shot migration: split knowledge_state.json into per-domain files.

Before:
  knowledge_state.json  # { learner, domains: { key: {...} } }

After:
  learner.json          # { name, session_count, last_session }
  domains/<key>.json    # { name, goal, created, concepts: [...] }
  knowledge_state.json.pre-split-YYYY-MM-DD.bak
"""
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STATE = ROOT / "knowledge_state.json"
LEARNER_OUT = ROOT / "learner.json"
DOMAINS_DIR = ROOT / "domains"
BACKUP = ROOT / f"knowledge_state.json.pre-split-{datetime.now().strftime('%Y-%m-%d')}.bak"


def main() -> None:
    if not STATE.exists():
        sys.exit(f"No {STATE.name} to migrate (already split?).")
    if DOMAINS_DIR.exists() and any(DOMAINS_DIR.glob("*.json")):
        sys.exit(f"Refusing to overwrite: {DOMAINS_DIR} already contains files.")

    data = json.loads(STATE.read_text())
    learner = data.get("learner", {})
    domains = data.get("domains", {})

    shutil.copy2(STATE, BACKUP)
    print(f"Backup:  {BACKUP.name}")

    LEARNER_OUT.write_text(json.dumps(learner, indent=2) + "\n")
    print(f"Wrote:   {LEARNER_OUT.name}")

    DOMAINS_DIR.mkdir(exist_ok=True)
    for key, payload in domains.items():
        out = DOMAINS_DIR / f"{key}.json"
        out.write_text(json.dumps(payload, indent=2) + "\n")
        print(f"Wrote:   domains/{out.name}  ({len(payload.get('concepts', []))} concepts)")

    STATE.unlink()
    print(f"Removed: {STATE.name} (backup preserved)")

    print(f"\nMigrated {len(domains)} domains + learner record.")


if __name__ == "__main__":
    main()
