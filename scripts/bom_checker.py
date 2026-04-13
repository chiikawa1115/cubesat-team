#!/usr/bin/env python3
"""CubeSat BOM Checker — Component list management"""
import json
import sys
import os
from datetime import datetime

WORKSPACE = os.path.join(os.path.dirname(__file__), '..', 'workspace')
BOM_FILE = os.path.join(WORKSPACE, 'bom.json')

def load_bom():
    os.makedirs(WORKSPACE, exist_ok=True)
    if not os.path.exists(BOM_FILE):
        with open(BOM_FILE, 'w', encoding='utf-8') as f:
            json.dump({"components": [], "updated": datetime.now().isoformat()}, f, ensure_ascii=False, indent=2)
    with open(BOM_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_bom(data):
    data["updated"] = datetime.now().isoformat()
    with open(BOM_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_component(subsystem, name, part_number="TBD", qty=1, unit_price=0, url="", notes=""):
    data = load_bom()
    comp = {
        "id": len(data["components"]) + 1,
        "subsystem": subsystem,
        "name": name,
        "part_number": part_number,
        "qty": int(qty),
        "unit_price": float(unit_price),
        "total": int(qty) * float(unit_price),
        "url": url,
        "notes": notes,
        "status": "quoted" if float(unit_price) > 0 else "pending"
    }
    data["components"].append(comp)
    save_bom(data)
    print(f"Added: {name} ({subsystem}) x {qty} = ${comp['total']:.2f}")

def update_price(comp_id, unit_price, url=""):
    data = load_bom()
    for c in data["components"]:
        if c["id"] == int(comp_id):
            c["unit_price"] = float(unit_price)
            c["total"] = c["qty"] * float(unit_price)
            if url:
                c["url"] = url
            c["status"] = "quoted"
            save_bom(data)
            print(f"Updated #{comp_id}: ${unit_price} x {c['qty']} = ${c['total']:.2f}")
            return
    print(f"Component #{comp_id} not found")

def show_summary():
    data = load_bom()
    if not data["components"]:
        print("BOM is empty.")
        return

    print(f"\n{'ID':>3} {'Subsystem':<12} {'Component':<25} {'Qty':>4} {'Unit$':>10} {'Total$':>10} {'Status'}")
    print("-" * 85)

    total = 0
    by_subsystem = {}
    for c in data["components"]:
        print(f"{c['id']:>3} {c['subsystem']:<12} {c['name']:<25} {c['qty']:>4} {c['unit_price']:>10.2f} {c['total']:>10.2f} {c['status']}")
        total += c["total"]
        by_subsystem[c["subsystem"]] = by_subsystem.get(c["subsystem"], 0) + c["total"]

    print("-" * 85)
    print(f"{'TOTAL':>52} ${total:>10.2f}")
    print(f"\nBy subsystem:")
    for sub, subtotal in sorted(by_subsystem.items()):
        print(f"  {sub:<20} ${subtotal:>10.2f}")

    pending = len([c for c in data["components"] if c["status"] == "pending"])
    if pending:
        print(f"\nWarning: {pending} component(s) still need pricing")

def export_markdown():
    """Export BOM as markdown table for reports."""
    data = load_bom()
    print("| # | Subsystem | Component | Part Number | Qty | Unit Price | Total | Status |")
    print("|---|-----------|-----------|-------------|-----|------------|-------|--------|")
    total = 0
    for c in data["components"]:
        total += c["total"]
        print(f"| {c['id']} | {c['subsystem']} | {c['name']} | {c['part_number']} | {c['qty']} | ${c['unit_price']:.2f} | ${c['total']:.2f} | {c['status']} |")
    print(f"| | | | **TOTAL** | | | **${total:.2f}** | |")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: bom_checker.py <command> [args]")
        print("Commands: add, update-price, summary, export-md")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "add" and len(sys.argv) >= 4:
        add_component(sys.argv[2], sys.argv[3],
                      sys.argv[4] if len(sys.argv) > 4 else "TBD",
                      sys.argv[5] if len(sys.argv) > 5 else 1,
                      sys.argv[6] if len(sys.argv) > 6 else 0)
    elif cmd == "update-price" and len(sys.argv) >= 4:
        update_price(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else "")
    elif cmd == "summary":
        show_summary()
    elif cmd == "export-md":
        export_markdown()
    else:
        print(f"Unknown command: {cmd}")
