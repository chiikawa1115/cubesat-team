#!/usr/bin/env python3
"""CubeSat Sprint Tracker — JSON-based backlog CRUD"""
import json
import sys
import os
from datetime import datetime

WORKSPACE = os.path.join(os.path.dirname(__file__), '..', 'workspace')
BACKLOG_FILE = os.path.join(WORKSPACE, 'backlog.json')
PROJECT_FILE = os.path.join(WORKSPACE, 'project.json')

def ensure_workspace():
    """Create workspace directory and files if they don't exist."""
    os.makedirs(WORKSPACE, exist_ok=True)
    os.makedirs(os.path.join(WORKSPACE, 'sprints'), exist_ok=True)
    os.makedirs(os.path.join(WORKSPACE, 'reviews'), exist_ok=True)
    if not os.path.exists(BACKLOG_FILE):
        with open(BACKLOG_FILE, 'w', encoding='utf-8') as f:
            json.dump({"items": [], "current_sprint": 1}, f, ensure_ascii=False, indent=2)

def load_backlog():
    ensure_workspace()
    with open(BACKLOG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_backlog(data):
    with open(BACKLOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def cmd_add(title, assignee, priority="medium", sprint=None):
    """Add a backlog item."""
    data = load_backlog()
    item_id = max([i["id"] for i in data["items"]], default=0) + 1
    item = {
        "id": item_id,
        "title": title,
        "assignee": assignee,
        "status": "todo",
        "priority": priority,
        "sprint": sprint or data["current_sprint"],
        "review_result": None,
        "created": datetime.now().isoformat(),
        "updated": datetime.now().isoformat()
    }
    data["items"].append(item)
    save_backlog(data)
    print(f"Added item #{item_id}: {title} → {assignee} (Sprint {item['sprint']})")

def cmd_update(item_id, **kwargs):
    """Update a backlog item's fields."""
    data = load_backlog()
    for item in data["items"]:
        if item["id"] == int(item_id):
            for k, v in kwargs.items():
                if v is not None:
                    item[k] = v
            item["updated"] = datetime.now().isoformat()
            save_backlog(data)
            print(f"Updated item #{item_id}: {kwargs}")
            return
    print(f"Item #{item_id} not found")

def cmd_list(sprint=None, status=None, assignee=None):
    """List backlog items with optional filters."""
    data = load_backlog()
    items = data["items"]
    if sprint:
        items = [i for i in items if i["sprint"] == int(sprint)]
    if status:
        items = [i for i in items if i["status"] == status]
    if assignee:
        items = [i for i in items if i["assignee"] == assignee]

    if not items:
        print("No items found.")
        return

    print(f"{'ID':>4} {'Status':<12} {'Priority':<8} {'Sprint':<7} {'Assignee':<15} {'Title'}")
    print("-" * 80)
    for i in sorted(items, key=lambda x: (x["sprint"], x["id"])):
        print(f"{i['id']:>4} {i['status']:<12} {i['priority']:<8} S{i['sprint']:<6} {i['assignee']:<15} {i['title']}")

def cmd_dashboard():
    """Show sprint dashboard with counts."""
    data = load_backlog()
    sprint = data["current_sprint"]
    items = [i for i in data["items"] if i["sprint"] == sprint]

    todo = len([i for i in items if i["status"] == "todo"])
    in_progress = len([i for i in items if i["status"] == "in-progress"])
    review = len([i for i in items if i["status"] == "review"])
    done = len([i for i in items if i["status"] == "done"])

    print(f"\n=== Sprint {sprint} Dashboard ===")
    print(f"  Todo:        {todo}")
    print(f"  In Progress: {in_progress}")
    print(f"  In Review:   {review}")
    print(f"  Done:        {done}")
    print(f"  Total:       {len(items)}")

    if items:
        progress = done / len(items) * 100
        print(f"  Progress:    {progress:.0f}%")

def cmd_next_sprint():
    """Advance to next sprint."""
    data = load_backlog()
    data["current_sprint"] += 1
    save_backlog(data)
    print(f"Advanced to Sprint {data['current_sprint']}")

def cmd_init_project(name, orbit_alt, form_factor, payload_type):
    """Initialize project definition."""
    ensure_workspace()
    project = {
        "name": name,
        "orbit_altitude_km": int(orbit_alt),
        "form_factor": form_factor,
        "payload_type": payload_type,
        "created": datetime.now().isoformat(),
        "sprints": [
            {"number": 1, "phase": "A", "goal": "Mission Concept & Requirements"},
            {"number": 2, "phase": "B", "goal": "Preliminary Design & PDR"},
            {"number": 3, "phase": "C", "goal": "Detailed Design & CDR"},
            {"number": 4, "phase": "D", "goal": "Integration & Final Report"}
        ]
    }
    with open(PROJECT_FILE, 'w', encoding='utf-8') as f:
        json.dump(project, f, ensure_ascii=False, indent=2)
    print(f"Project initialized: {name}")
    print(f"  Orbit: {orbit_alt} km, Form: {form_factor}, Payload: {payload_type}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: sprint_tracker.py <command> [args]")
        print("Commands: init, add, update, list, dashboard, next-sprint")
        sys.exit(1)

    cmd = sys.argv[1]
    args = sys.argv[2:]

    if cmd == "init" and len(args) >= 4:
        cmd_init_project(args[0], args[1], args[2], args[3])
    elif cmd == "add" and len(args) >= 2:
        cmd_add(args[0], args[1], args[2] if len(args) > 2 else "medium")
    elif cmd == "update" and len(args) >= 3:
        cmd_update(args[0], **{args[1]: args[2]})
    elif cmd == "list":
        filters = {}
        for i in range(0, len(args), 2):
            if i+1 < len(args):
                filters[args[i].lstrip('-')] = args[i+1]
        cmd_list(**filters)
    elif cmd == "dashboard":
        cmd_dashboard()
    elif cmd == "next-sprint":
        cmd_next_sprint()
    else:
        print(f"Unknown command or missing args: {cmd}")
