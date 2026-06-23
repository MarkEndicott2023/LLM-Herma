#!/usr/bin/env python3
"""Generate a mermaid knowledge graph from domains/*.json.

Run: python3 build_graph.py
Output: knowledge_graph.md (preview with VS Code's Markdown: Open Preview).
"""
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOMAINS_DIR = ROOT / "domains"
OUT = ROOT / "knowledge_graph.md"


def load_domains() -> dict:
    out = {}
    for path in sorted(DOMAINS_DIR.glob("*.json")):
        out[path.stem] = json.loads(path.read_text())
    return out


def bucket(m: float) -> str:
    if m >= 0.7:
        return "mastered"
    if m > 0:
        return "learning"
    return "untouched"


def sanitize(s: str) -> str:
    return s.replace('"', "'").replace("[", "(").replace("]", ")")


def main() -> None:
    domains = load_domains()
    today = datetime.now().strftime("%Y-%m-%d")

    out = [
        "# Knowledge Graph",
        "",
        f"_Generated {today} from `domains/*.json`. Regenerate: `python3 build_graph.py`._",
        "",
        "**Legend** — 🟢 mastered (≥ 0.7) · 🟡 learning (0 < m < 0.7) · ⚪ untouched (m = 0)",
        "",
        "## Summary",
        "",
        "| Domain | 🟢 | 🟡 | ⚪ | Total |",
        "|---|---:|---:|---:|---:|",
    ]

    for key, dom in domains.items():
        counts = {"mastered": 0, "learning": 0, "untouched": 0}
        for c in dom["concepts"]:
            counts[bucket(c.get("mastery", 0))] += 1
        out.append(
            f"| {dom.get('name', key)} | {counts['mastered']} | {counts['learning']} | {counts['untouched']} | {len(dom['concepts'])} |"
        )
    out.append("")

    for key, dom in domains.items():
        out.append(f"## {dom.get('name', key)}")
        goal = dom.get("goal")
        if goal:
            out.append(f"_Goal: {goal}_")
        out.append("")
        out.append("```mermaid")
        out.append("flowchart TD")

        for c in dom["concepts"]:
            name = sanitize(c.get("name", c["id"]))
            m = c.get("mastery", 0)
            out.append(f'    {c["id"]}["{name}<br/>m={m:.2f}"]')

        for c in dom["concepts"]:
            for p in c.get("prerequisites", []):
                out.append(f'    {p} --> {c["id"]}')

        out.append("")
        out.append("    classDef mastered fill:#86efac,stroke:#166534,color:#064e3b;")
        out.append("    classDef learning fill:#fde68a,stroke:#b45309,color:#78350f;")
        out.append("    classDef untouched fill:#e5e7eb,stroke:#6b7280,color:#374151;")
        for b in ("mastered", "learning", "untouched"):
            ids = [c["id"] for c in dom["concepts"] if bucket(c.get("mastery", 0)) == b]
            if ids:
                out.append(f"    class {','.join(ids)} {b};")
        out.append("```")
        out.append("")

    OUT.write_text("\n".join(out))
    print(f"Wrote {OUT} ({sum(len(d['concepts']) for d in domains.values())} concepts across {len(domains)} domains)")


if __name__ == "__main__":
    main()
