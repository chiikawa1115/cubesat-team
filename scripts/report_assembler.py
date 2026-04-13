#!/usr/bin/env python3
"""CubeSat Report Assembler — Merge agent sections into a single document"""
import json
import sys
import os
from datetime import datetime

WORKSPACE = os.path.join(os.path.dirname(__file__), '..', 'workspace')

REPORT_SECTIONS = [
    {"page": "1", "title": "封面", "agent": "ceo", "file": "cover.md"},
    {"page": "2", "title": "目錄", "agent": "auto", "file": None},
    {"page": "3-4", "title": "Executive Summary", "agent": "ceo", "file": "executive-summary.md"},
    {"page": "5-6", "title": "任務概念 & ConOps", "agent": "systems-engineer", "file": "conops.md"},
    {"page": "7-8", "title": "系統需求", "agent": "systems-engineer", "file": "requirements.md"},
    {"page": "9-10", "title": "系統架構", "agent": "systems-engineer", "file": "architecture.md"},
    {"page": "11-12", "title": "通訊酬載設計", "agent": "comm-payload", "file": "comm-design.md"},
    {"page": "13-14", "title": "AOCS 設計", "agent": "aocs", "file": "aocs-design.md"},
    {"page": "15-16", "title": "軟韌體架構", "agent": "sw-firmware", "file": "sw-architecture.md"},
    {"page": "17", "title": "結構 & 熱控", "agent": "mech-thermal", "file": "structure-thermal.md"},
    {"page": "18-19", "title": "V&V 計畫", "agent": "qa-test", "file": "vv-plan.md"},
    {"page": "20-21", "title": "時程 & WBS", "agent": "pm", "file": "schedule-wbs.md"},
    {"page": "22-23", "title": "預算 & BOM", "agent": "pm", "file": "budget-bom.md"},
    {"page": "24", "title": "風險矩陣", "agent": "pm", "file": "risk-matrix.md"},
    {"page": "25", "title": "團隊 & 分工", "agent": "ceo", "file": "team.md"},
]

def check_status(sprint_dir=None):
    """Check which sections are written and which are missing."""
    if not sprint_dir:
        sprint_dir = os.path.join(WORKSPACE, 'sprints', 'final')

    print(f"\n=== Report Assembly Status ===")
    print(f"Source: {sprint_dir}\n")
    print(f"{'Page':<6} {'Title':<25} {'Agent':<18} {'Status'}")
    print("-" * 70)

    complete = 0
    for sec in REPORT_SECTIONS:
        if sec["file"] is None:
            print(f"{sec['page']:<6} {sec['title']:<25} {sec['agent']:<18} (auto-generated)")
            complete += 1
            continue
        filepath = os.path.join(sprint_dir, sec["file"])
        exists = os.path.exists(filepath)
        status = "ready" if exists else "MISSING"
        if exists:
            complete += 1
        print(f"{sec['page']:<6} {sec['title']:<25} {sec['agent']:<18} {status}")

    total = len(REPORT_SECTIONS)
    print(f"\nProgress: {complete}/{total} sections ({complete/total*100:.0f}%)")

def assemble(sprint_dir=None, output_file=None):
    """Assemble all sections into a single markdown file."""
    if not sprint_dir:
        sprint_dir = os.path.join(WORKSPACE, 'sprints', 'final')
    if not output_file:
        output_file = os.path.join(WORKSPACE, 'report.md')

    parts = []
    toc_entries = []

    for sec in REPORT_SECTIONS:
        if sec["file"] is None:
            continue
        filepath = os.path.join(sprint_dir, sec["file"])
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            parts.append(f"\n---\n\n## {sec['title']}\n\n{content}")
            toc_entries.append(f"- **p.{sec['page']}** -- {sec['title']}")
        else:
            parts.append(f"\n---\n\n## {sec['title']}\n\n> Warning: This section is not yet complete (owner: {sec['agent']})\n")
            toc_entries.append(f"- **p.{sec['page']}** -- {sec['title']} [MISSING]")

    # Build TOC
    toc = "## Table of Contents\n\n" + "\n".join(toc_entries)

    # Assemble full report
    report = f"# CubeSat Project Report\n\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n{toc}\n" + "\n".join(parts)

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"Report assembled: {output_file}")
    print(f"Total length: {len(report)} chars, {len(report.splitlines())} lines")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: report_assembler.py <command>")
        print("Commands: status, assemble")
        sys.exit(1)

    cmd = sys.argv[1]
    sprint_dir = sys.argv[2] if len(sys.argv) > 2 else None

    if cmd == "status":
        check_status(sprint_dir)
    elif cmd == "assemble":
        assemble(sprint_dir)
    else:
        print(f"Unknown command: {cmd}")
