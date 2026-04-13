#!/usr/bin/env python3
"""CubeSat Budget Manager — Full project budget management across all cost categories."""
import json
import sys
import os
import argparse
from datetime import datetime

WORKSPACE = os.path.join(os.path.dirname(__file__), '..', 'workspace')
BUDGET_FILE = os.path.join(WORKSPACE, 'budget.json')

CATEGORIES = [
    "hardware",      # 元件/硬體（規格導向，不需正確料號）
    "personnel",     # 人事費（人數 x 工時 x 時薪）
    "travel",        # 差旅費（TASA 參訪、測試場地）
    "launch",        # 發射費（CubeSat rideshare）
    "testing",       # 測試費（熱真空、振動、EMC）
    "software",      # 軟體授權
    "insurance",     # 保險
    "contingency",   # 管理預備金
]

# Sensible defaults for common CubeSat costs (USD)
COST_DEFAULTS = {
    "launch": [
        {"name": "3U rideshare (SpaceX Transporter)", "qty": 1, "unit_cost": 275000,
         "notes": "SSO 500-600km, typical range $200K-$325K"},
    ],
    "personnel": [
        {"name": "Student assistants (NTD 200/hr)", "qty": 5, "unit_cost": 2400,
         "spec": "80 hrs/month x 6 months", "notes": "NTD 200/hr ~ USD 6.25/hr, per person total"},
        {"name": "Research assistant (NTD 350/hr)", "qty": 1, "unit_cost": 8400,
         "spec": "160 hrs/month x 6 months", "notes": "NTD 350/hr ~ USD 11/hr, per person total"},
    ],
    "testing": [
        {"name": "Thermal vacuum test (TVAC)", "qty": 2, "unit_cost": 7500,
         "spec": "2 weeks", "notes": "$5K-$15K/week"},
        {"name": "Vibration test", "qty": 2, "unit_cost": 5000,
         "spec": "1-3 days", "notes": "$3K-$8K/day"},
        {"name": "EMC/EMI test", "qty": 1, "unit_cost": 3500,
         "spec": "1-2 days", "notes": "$2K-$5K/day"},
        {"name": "Antenna pattern measurement", "qty": 1, "unit_cost": 2000,
         "spec": "1 day", "notes": "$1K-$3K"},
    ],
    "insurance": [
        {"name": "Launch insurance (10-15% of satellite cost)", "qty": 1, "unit_cost": 15000,
         "notes": "Estimated at ~10-15% of hardware cost"},
    ],
    "contingency": [
        {"name": "Management contingency (15-20%)", "qty": 1, "unit_cost": 0,
         "notes": "Calculate as 15-20% of all other categories combined"},
    ],
}


def load_budget():
    """Load budget from file, creating default structure if needed."""
    os.makedirs(WORKSPACE, exist_ok=True)
    if not os.path.exists(BUDGET_FILE):
        data = {
            "categories": {cat: {"items": [], "subtotal": 0} for cat in CATEGORIES},
            "total": 0,
            "currency": "USD",
            "updated": datetime.now().isoformat()
        }
        with open(BUDGET_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    with open(BUDGET_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_budget(data):
    """Recalculate subtotals/total and save."""
    for cat in data["categories"]:
        items = data["categories"][cat]["items"]
        data["categories"][cat]["subtotal"] = sum(item["total"] for item in items)
    data["total"] = sum(data["categories"][cat]["subtotal"] for cat in data["categories"])
    data["updated"] = datetime.now().isoformat()
    with open(BUDGET_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def next_id(data, category):
    """Generate next item ID for a category."""
    items = data["categories"][category]["items"]
    if not items:
        return f"{category[:3].upper()}-001"
    last_num = max(int(item["id"].split("-")[1]) for item in items)
    return f"{category[:3].upper()}-{last_num + 1:03d}"


def add_item(category, name, qty, unit_cost, spec="", notes=""):
    """Add an item to a budget category."""
    if category not in CATEGORIES:
        print(f"Error: Unknown category '{category}'")
        print(f"Valid categories: {', '.join(CATEGORIES)}")
        return
    data = load_budget()
    item = {
        "id": next_id(data, category),
        "name": name,
        "spec": spec,
        "qty": int(qty),
        "unit_cost": float(unit_cost),
        "total": int(qty) * float(unit_cost),
        "notes": notes,
    }
    data["categories"][category]["items"].append(item)
    save_budget(data)
    print(f"Added [{item['id']}] to {category}: {name} x {qty} = ${item['total']:,.2f}")


def remove_item(item_id):
    """Remove an item by its ID."""
    data = load_budget()
    for cat in data["categories"]:
        items = data["categories"][cat]["items"]
        for i, item in enumerate(items):
            if item["id"] == item_id.upper():
                removed = items.pop(i)
                save_budget(data)
                print(f"Removed [{item_id}] {removed['name']} (${removed['total']:,.2f}) from {cat}")
                return
    print(f"Error: Item '{item_id}' not found")


def show_summary():
    """Show full budget summary by category with grand total."""
    data = load_budget()
    total = 0
    print(f"\n{'='*70}")
    print(f"  CubeSat Project Budget Summary")
    print(f"  Currency: {data['currency']}  |  Updated: {data['updated'][:19]}")
    print(f"{'='*70}")

    for cat in CATEGORIES:
        cat_data = data["categories"].get(cat, {"items": [], "subtotal": 0})
        items = cat_data["items"]
        subtotal = cat_data["subtotal"]
        total += subtotal

        print(f"\n  [{cat.upper()}]")
        if items:
            for item in items:
                spec_str = f" ({item['spec']})" if item.get("spec") else ""
                print(f"    {item['id']:>8}  {item['name']:<35}{spec_str}")
                print(f"             {item['qty']:>4} x ${item['unit_cost']:>12,.2f} = ${item['total']:>12,.2f}")
        else:
            print(f"    (no items)")
        print(f"    {'Subtotal':>44}: ${subtotal:>12,.2f}")

    print(f"\n{'='*70}")
    print(f"    {'GRAND TOTAL':>44}: ${total:>12,.2f}")
    print(f"{'='*70}\n")

    # Warn about empty categories
    empty = [cat for cat in CATEGORIES if not data["categories"].get(cat, {}).get("items")]
    if empty:
        print(f"  Note: Empty categories: {', '.join(empty)}")
        print()


def show_category(category):
    """Show items in one category."""
    if category not in CATEGORIES:
        print(f"Error: Unknown category '{category}'")
        print(f"Valid categories: {', '.join(CATEGORIES)}")
        return
    data = load_budget()
    cat_data = data["categories"].get(category, {"items": [], "subtotal": 0})
    items = cat_data["items"]

    print(f"\n  [{category.upper()}] — {len(items)} item(s)")
    print(f"  {'-'*65}")
    if items:
        print(f"  {'ID':<10} {'Name':<30} {'Spec':<15} {'Qty':>4} {'Unit$':>12} {'Total$':>12}")
        print(f"  {'-'*65}")
        for item in items:
            spec = item.get("spec", "")[:14]
            print(f"  {item['id']:<10} {item['name']:<30} {spec:<15} {item['qty']:>4} ${item['unit_cost']:>11,.2f} ${item['total']:>11,.2f}")
            if item.get("notes"):
                print(f"  {'':>10} Notes: {item['notes']}")
    else:
        print(f"  (no items)")
    print(f"  {'-'*65}")
    print(f"  {'Subtotal':>56}: ${cat_data['subtotal']:>12,.2f}\n")


def export_markdown():
    """Export budget as markdown tables for report."""
    data = load_budget()
    total = 0

    print("# CubeSat Project Budget\n")
    print(f"> Currency: {data['currency']} | Updated: {data['updated'][:19]}\n")

    for cat in CATEGORIES:
        cat_data = data["categories"].get(cat, {"items": [], "subtotal": 0})
        items = cat_data["items"]
        subtotal = cat_data["subtotal"]
        total += subtotal

        print(f"## {cat.title()}\n")
        if items:
            print("| ID | Name | Spec | Qty | Unit Cost | Total | Notes |")
            print("|-----|------|------|-----|-----------|-------|-------|")
            for item in items:
                spec = item.get("spec", "")
                notes = item.get("notes", "")
                print(f"| {item['id']} | {item['name']} | {spec} | {item['qty']} | ${item['unit_cost']:,.2f} | ${item['total']:,.2f} | {notes} |")
            print(f"| | | | **Subtotal** | | **${subtotal:,.2f}** | |\n")
        else:
            print("(no items)\n")

    print("## Summary\n")
    print("| Category | Subtotal | % |")
    print("|----------|----------|---|")
    for cat in CATEGORIES:
        subtotal = data["categories"].get(cat, {}).get("subtotal", 0)
        pct = (subtotal / total * 100) if total > 0 else 0
        print(f"| {cat.title()} | ${subtotal:,.2f} | {pct:.1f}% |")
    print(f"| **GRAND TOTAL** | **${total:,.2f}** | **100%** |")


def init_defaults():
    """Initialize budget with sensible CubeSat cost defaults."""
    data = load_budget()
    added = 0
    for cat, defaults in COST_DEFAULTS.items():
        if not data["categories"][cat]["items"]:
            for d in defaults:
                item = {
                    "id": next_id(data, cat),
                    "name": d["name"],
                    "spec": d.get("spec", ""),
                    "qty": d["qty"],
                    "unit_cost": d["unit_cost"],
                    "total": d["qty"] * d["unit_cost"],
                    "notes": d.get("notes", ""),
                }
                data["categories"][cat]["items"].append(item)
                added += 1
    save_budget(data)
    print(f"Initialized budget with {added} default items across {len(COST_DEFAULTS)} categories.")
    print("Run 'summary' to view the full budget.")


def main():
    parser = argparse.ArgumentParser(
        description="CubeSat Budget Manager — Full project budget management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Categories: hardware, personnel, travel, launch, testing, software, insurance, contingency

Examples:
  budget_manager.py add hardware "OBC Zynq-7000 class" 1 150 --spec "ARM+FPGA 50K LUT"
  budget_manager.py add launch "SpaceX Transporter 3U" 1 275000 --notes "SSO 500km"
  budget_manager.py add personnel "Student assistant" 5 2400 --spec "80hr/mo x 6mo"
  budget_manager.py summary
  budget_manager.py category hardware
  budget_manager.py export-md
  budget_manager.py init-defaults
  budget_manager.py remove HAR-001
        """)

    subparsers = parser.add_subparsers(dest="command")

    # add
    add_parser = subparsers.add_parser("add", help="Add item to a budget category")
    add_parser.add_argument("category", choices=CATEGORIES, help="Budget category")
    add_parser.add_argument("name", help="Item name")
    add_parser.add_argument("qty", type=int, help="Quantity")
    add_parser.add_argument("unit_cost", type=float, help="Unit cost (USD)")
    add_parser.add_argument("--spec", default="", help="Specification (for hardware)")
    add_parser.add_argument("--notes", default="", help="Additional notes")

    # remove
    rm_parser = subparsers.add_parser("remove", help="Remove an item by ID")
    rm_parser.add_argument("item_id", help="Item ID (e.g., HAR-001)")

    # summary
    subparsers.add_parser("summary", help="Full budget summary by category")

    # category
    cat_parser = subparsers.add_parser("category", help="Show items in one category")
    cat_parser.add_argument("name", choices=CATEGORIES, help="Category name")

    # export-md
    subparsers.add_parser("export-md", help="Export budget as markdown tables")

    # init-defaults
    subparsers.add_parser("init-defaults", help="Initialize with common CubeSat cost defaults")

    args = parser.parse_args()

    if args.command == "add":
        add_item(args.category, args.name, args.qty, args.unit_cost,
                 spec=args.spec, notes=args.notes)
    elif args.command == "remove":
        remove_item(args.item_id)
    elif args.command == "summary":
        show_summary()
    elif args.command == "category":
        show_category(args.name)
    elif args.command == "export-md":
        export_markdown()
    elif args.command == "init-defaults":
        init_defaults()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
