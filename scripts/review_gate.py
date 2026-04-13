#!/usr/bin/env python3
"""CubeSat Peer Review Gate — Checklist validation"""
import json
import sys
import os
from datetime import datetime

WORKSPACE = os.path.join(os.path.dirname(__file__), '..', 'workspace')
REVIEWS_DIR = os.path.join(WORKSPACE, 'reviews')

CHECKLIST = [
    "技術正確性 — 設計參數與計算符合物理原理和參考文獻",
    "需求可追溯 — 每項設計決策可對應到系統需求 ID",
    "格式完整性 — 符合模板格式，章節完整",
    "Budget 合理性 — mass/power/data budget margin ≥ 20%",
    "介面一致性 — 與 ICD 定義吻合，connector/protocol/format 明確",
]

def create_review(deliverable, author, reviewer1, reviewer2):
    """Create a new peer review record."""
    os.makedirs(REVIEWS_DIR, exist_ok=True)
    review_id = f"PR-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    review = {
        "id": review_id,
        "deliverable": deliverable,
        "author": author,
        "reviewers": [
            {"name": reviewer1, "verdict": "pending", "checks": {c: None for c in CHECKLIST}, "comments": ""},
            {"name": reviewer2, "verdict": "pending", "checks": {c: None for c in CHECKLIST}, "comments": ""}
        ],
        "final_verdict": "pending",
        "created": datetime.now().isoformat()
    }
    filepath = os.path.join(REVIEWS_DIR, f"{review_id}.json")
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(review, f, ensure_ascii=False, indent=2)
    print(f"Review created: {review_id}")
    print(f"  Deliverable: {deliverable}")
    print(f"  Author: {author}")
    print(f"  Reviewers: {reviewer1}, {reviewer2}")
    print(f"\nChecklist ({len(CHECKLIST)} items):")
    for i, c in enumerate(CHECKLIST, 1):
        print(f"  {i}. {c}")
    return review_id

def submit_review(review_id, reviewer_name, checks_json, verdict, comments=""):
    """Submit a reviewer's assessment."""
    filepath = os.path.join(REVIEWS_DIR, f"{review_id}.json")
    with open(filepath, 'r', encoding='utf-8') as f:
        review = json.load(f)

    for r in review["reviewers"]:
        if r["name"] == reviewer_name:
            r["checks"] = checks_json if isinstance(checks_json, dict) else json.loads(checks_json)
            r["verdict"] = verdict  # approve, approve-with-comments, reject
            r["comments"] = comments
            break

    # Check if both reviewers are done
    verdicts = [r["verdict"] for r in review["reviewers"]]
    if "pending" not in verdicts:
        if "reject" in verdicts:
            review["final_verdict"] = "rejected"
        elif all(v in ("approve", "approve-with-comments") for v in verdicts):
            review["final_verdict"] = "approved"

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(review, f, ensure_ascii=False, indent=2)

    print(f"Review {review_id}: {reviewer_name} → {verdict}")
    if review["final_verdict"] != "pending":
        print(f"  FINAL VERDICT: {review['final_verdict'].upper()}")

def list_reviews(status=None):
    """List all reviews."""
    if not os.path.exists(REVIEWS_DIR):
        print("No reviews yet.")
        return
    found = False
    for fname in sorted(os.listdir(REVIEWS_DIR)):
        if not fname.endswith('.json'):
            continue
        with open(os.path.join(REVIEWS_DIR, fname), 'r', encoding='utf-8') as f:
            r = json.load(f)
        if status and r["final_verdict"] != status:
            continue
        verdicts = "/".join(rv["verdict"] for rv in r["reviewers"])
        print(f"  {r['id']}  {r['final_verdict']:<10}  [{verdicts}]  {r['deliverable']}")
        found = True
    if not found:
        print("No reviews found.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: review_gate.py <command> [args]")
        print("Commands: create, submit, list")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "create" and len(sys.argv) >= 6:
        create_review(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    elif cmd == "submit" and len(sys.argv) >= 5:
        submit_review(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5] if len(sys.argv) > 5 else "")
    elif cmd == "list":
        list_reviews(sys.argv[2] if len(sys.argv) > 2 else None)
    else:
        print(f"Unknown command: {cmd}")
