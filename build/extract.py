#!/usr/bin/env python3
import json, os

SRC = "/private/tmp/claude-501/-Users-jean-paulgavini-Documents-Dev-napo/27d1e6f6-0781-4972-b2a7-bf5abb136490/tasks/wm6v4wxcp.output"
OUT = "/Users/jean-paulgavini/Documents/Dev/napo/build"
os.makedirs(os.path.join(OUT, "blocks"), exist_ok=True)
os.makedirs(os.path.join(OUT, "widgets"), exist_ok=True)

with open(SRC, encoding="utf-8") as f:
    data = json.load(f)["result"]

# audit
audit = data.get("audit", {})
with open(os.path.join(OUT, "audit.json"), "w", encoding="utf-8") as f:
    json.dump(audit, f, ensure_ascii=False, indent=2)

# blocks
blocks = data.get("blocks", [])
index = []
for b in blocks:
    bid = b.get("id", "unknown")
    html = b.get("html", "")
    with open(os.path.join(OUT, "blocks", bid + ".html"), "w", encoding="utf-8") as f:
        f.write(html)
    index.append({"id": bid, "where": b.get("where", ""), "len": len(html), "notes": b.get("notes", "")})

# widgets
widgets = data.get("widgets", [])
for w in widgets:
    wid = w.get("id", "unknown")
    html = w.get("html", "")
    with open(os.path.join(OUT, "widgets", wid + ".html"), "w", encoding="utf-8") as f:
        f.write(html)
    index.append({"id": "widget:" + wid, "title": w.get("title", ""), "len": len(html), "notes": w.get("integration_notes", "")})

# glossary + tldr
with open(os.path.join(OUT, "glossary.json"), "w", encoding="utf-8") as f:
    json.dump(data.get("glossary", {}), f, ensure_ascii=False, indent=2)
with open(os.path.join(OUT, "tldr.json"), "w", encoding="utf-8") as f:
    json.dump(data.get("tldr", {}), f, ensure_ascii=False, indent=2)

# print a compact manifest
print("=== AUDIT ===")
print("confirmed:", len(audit.get("confirmed", [])))
print("corrections:", json.dumps(audit.get("corrections", []), ensure_ascii=False))
print("rejected:", json.dumps(audit.get("rejected", []), ensure_ascii=False))
if audit.get("notes"):
    print("notes:", audit["notes"][:1500])
print()
print("=== BLOCKS / WIDGETS ===")
for it in index:
    label = it.get("id")
    extra = it.get("title", it.get("where", ""))
    print(f"{label:28s} {it['len']:6d}  {extra[:70]}")
print()
print("glossary terms:", len(data.get("glossary", {}).get("terms", [])))
print("tldr keys:", list(data.get("tldr", {}).keys()))
