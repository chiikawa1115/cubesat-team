#!/usr/bin/env python3
"""CubeSat Team Collaboration — Agent-to-agent discussion and review system."""
import json
import sys
import os
import argparse
from datetime import datetime

WORKSPACE = os.path.join(os.path.dirname(__file__), '..', 'workspace')
DISCUSSIONS_FILE = os.path.join(WORKSPACE, 'discussions.json')

VALID_AGENTS = [
    "ceo", "pm", "systems-engineer", "comm-payload",
    "aocs", "sw-firmware", "mech-thermal", "qa-test",
]

VALID_STATUSES = ["open", "resolved", "blocked"]


def load_discussions():
    """Load discussions from file, creating default structure if needed."""
    os.makedirs(WORKSPACE, exist_ok=True)
    if not os.path.exists(DISCUSSIONS_FILE):
        data = {"threads": []}
        with open(DISCUSSIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    with open(DISCUSSIONS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_discussions(data):
    """Save discussions to file."""
    with open(DISCUSSIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def next_thread_id(data):
    """Generate the next thread ID."""
    if not data["threads"]:
        return "THR-001"
    last_num = max(int(t["id"].split("-")[1]) for t in data["threads"])
    return f"THR-{last_num + 1:03d}"


def new_thread(from_agent, to_agent, topic, message):
    """Start a new discussion thread."""
    if from_agent not in VALID_AGENTS:
        print(f"Error: Unknown agent '{from_agent}'")
        print(f"Valid agents: {', '.join(VALID_AGENTS)}")
        return
    if to_agent not in VALID_AGENTS:
        print(f"Error: Unknown agent '{to_agent}'")
        print(f"Valid agents: {', '.join(VALID_AGENTS)}")
        return
    if from_agent == to_agent:
        print("Error: Cannot create a thread with yourself")
        return

    data = load_discussions()
    now = datetime.now().isoformat()
    thread = {
        "id": next_thread_id(data),
        "topic": topic,
        "created_by": from_agent,
        "created": now,
        "status": "open",
        "participants": [from_agent, to_agent],
        "messages": [
            {
                "from": from_agent,
                "to": to_agent,
                "message": message,
                "timestamp": now,
            }
        ],
        "resolution": None,
    }
    data["threads"].append(thread)
    save_discussions(data)
    print(f"Created thread {thread['id']}: \"{topic}\"")
    print(f"  From: {from_agent} -> To: {to_agent}")
    print(f"  Status: open")
    print(f"  Message: {message[:80]}{'...' if len(message) > 80 else ''}")


def reply(thread_id, from_agent, message):
    """Reply to an existing thread."""
    if from_agent not in VALID_AGENTS:
        print(f"Error: Unknown agent '{from_agent}'")
        print(f"Valid agents: {', '.join(VALID_AGENTS)}")
        return

    data = load_discussions()
    thread_id = thread_id.upper()
    for thread in data["threads"]:
        if thread["id"] == thread_id:
            if thread["status"] == "resolved":
                print(f"Warning: Thread {thread_id} is already resolved. Adding reply anyway.")

            # Add participant if not already in list
            if from_agent not in thread["participants"]:
                thread["participants"].append(from_agent)

            # Determine 'to' — reply to the last person who spoke, or the other participant
            last_msg = thread["messages"][-1]
            to_agent = last_msg["from"] if last_msg["from"] != from_agent else thread["created_by"]

            thread["messages"].append({
                "from": from_agent,
                "to": to_agent,
                "message": message,
                "timestamp": datetime.now().isoformat(),
            })
            save_discussions(data)
            print(f"Reply added to {thread_id} by {from_agent}")
            print(f"  -> {to_agent}: {message[:80]}{'...' if len(message) > 80 else ''}")
            return
    print(f"Error: Thread '{thread_id}' not found")


def resolve(thread_id, resolution):
    """Mark a thread as resolved."""
    data = load_discussions()
    thread_id = thread_id.upper()
    for thread in data["threads"]:
        if thread["id"] == thread_id:
            thread["status"] = "resolved"
            thread["resolution"] = resolution
            save_discussions(data)
            print(f"Thread {thread_id} resolved: {resolution[:80]}{'...' if len(resolution) > 80 else ''}")
            return
    print(f"Error: Thread '{thread_id}' not found")


def block(thread_id, reason=""):
    """Mark a thread as blocked."""
    data = load_discussions()
    thread_id = thread_id.upper()
    for thread in data["threads"]:
        if thread["id"] == thread_id:
            thread["status"] = "blocked"
            if reason:
                thread["messages"].append({
                    "from": "system",
                    "to": "all",
                    "message": f"[BLOCKED] {reason}",
                    "timestamp": datetime.now().isoformat(),
                })
            save_discussions(data)
            print(f"Thread {thread_id} marked as BLOCKED")
            if reason:
                print(f"  Reason: {reason}")
            return
    print(f"Error: Thread '{thread_id}' not found")


def list_threads(status_filter=None):
    """List all threads, optionally filtered by status."""
    data = load_discussions()
    threads = data["threads"]
    if status_filter:
        threads = [t for t in threads if t["status"] == status_filter]

    if not threads:
        filter_str = f" (status={status_filter})" if status_filter else ""
        print(f"No threads found{filter_str}.")
        return

    print(f"\n{'ID':<10} {'Status':<10} {'Topic':<35} {'Created By':<16} {'Messages':>8}")
    print("-" * 85)
    for t in threads:
        topic_str = t["topic"][:34]
        print(f"{t['id']:<10} {t['status']:<10} {topic_str:<35} {t['created_by']:<16} {len(t['messages']):>8}")
    print(f"\nTotal: {len(threads)} thread(s)")

    # Summary counts
    all_threads = data["threads"]
    open_count = len([t for t in all_threads if t["status"] == "open"])
    resolved_count = len([t for t in all_threads if t["status"] == "resolved"])
    blocked_count = len([t for t in all_threads if t["status"] == "blocked"])
    print(f"  Open: {open_count} | Resolved: {resolved_count} | Blocked: {blocked_count}")


def show_thread(thread_id):
    """Show full thread details."""
    data = load_discussions()
    thread_id = thread_id.upper()
    for thread in data["threads"]:
        if thread["id"] == thread_id:
            print(f"\n{'='*70}")
            print(f"  Thread: {thread['id']}  |  Status: {thread['status'].upper()}")
            print(f"  Topic: {thread['topic']}")
            print(f"  Created by: {thread['created_by']}  |  Date: {thread['created'][:19]}")
            print(f"  Participants: {', '.join(thread['participants'])}")
            if thread["resolution"]:
                print(f"  Resolution: {thread['resolution']}")
            print(f"{'='*70}")

            for i, msg in enumerate(thread["messages"]):
                ts = msg["timestamp"][:19]
                print(f"\n  [{i+1}] {msg['from']} -> {msg['to']}  ({ts})")
                print(f"      {msg['message']}")

            print(f"\n{'='*70}\n")
            return
    print(f"Error: Thread '{thread_id}' not found")


def action_items():
    """List all open/blocked threads that need response — grouped by agent."""
    data = load_discussions()
    pending = {}

    for thread in data["threads"]:
        if thread["status"] not in ("open", "blocked"):
            continue
        if not thread["messages"]:
            continue

        last_msg = thread["messages"][-1]
        # The agent being addressed needs to respond
        needs_response_from = last_msg["to"]
        if needs_response_from == "all":
            # If addressed to all, all participants except the sender need to respond
            for p in thread["participants"]:
                if p != last_msg["from"]:
                    pending.setdefault(p, []).append(thread)
        else:
            pending.setdefault(needs_response_from, []).append(thread)

    if not pending:
        print("No pending action items.")
        return

    print(f"\n{'='*70}")
    print(f"  ACTION ITEMS — Open/Blocked Threads Needing Response")
    print(f"{'='*70}")

    for agent in sorted(pending.keys()):
        threads = pending[agent]
        print(f"\n  [{agent}] — {len(threads)} item(s) pending:")
        for t in threads:
            last_msg = t["messages"][-1]
            status_icon = "!" if t["status"] == "blocked" else "?"
            print(f"    {status_icon} {t['id']} ({t['status']}): {t['topic']}")
            print(f"      Last from {last_msg['from']}: {last_msg['message'][:60]}...")

    print(f"\n{'='*70}\n")
    total = sum(len(v) for v in pending.values())
    print(f"Total: {total} action item(s) across {len(pending)} agent(s)")


def main():
    parser = argparse.ArgumentParser(
        description="CubeSat Team Collaboration — Agent discussion & review system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Valid agents: ceo, pm, systems-engineer, comm-payload, aocs, sw-firmware, mech-thermal, qa-test

Examples:
  collab.py new-thread comm-payload systems-engineer "Link Budget margin" "Ka-band margin is only 1.5dB, need 3dB"
  collab.py reply THR-001 systems-engineer "Consider increasing antenna gain by 2dB"
  collab.py resolve THR-001 "Agreed to use 0.3m antenna instead of 0.2m"
  collab.py list --status open
  collab.py show THR-001
  collab.py action-items
        """)

    subparsers = parser.add_subparsers(dest="command")

    # new-thread
    nt = subparsers.add_parser("new-thread", help="Start a new discussion thread")
    nt.add_argument("from_agent", help="Initiating agent")
    nt.add_argument("to_agent", help="Target agent")
    nt.add_argument("topic", help="Thread topic")
    nt.add_argument("message", help="Initial message")

    # reply
    rp = subparsers.add_parser("reply", help="Reply to a thread")
    rp.add_argument("thread_id", help="Thread ID (e.g., THR-001)")
    rp.add_argument("from_agent", help="Replying agent")
    rp.add_argument("message", help="Reply message")

    # resolve
    rs = subparsers.add_parser("resolve", help="Mark thread as resolved")
    rs.add_argument("thread_id", help="Thread ID")
    rs.add_argument("resolution", help="Resolution description")

    # block
    bl = subparsers.add_parser("block", help="Mark thread as blocked")
    bl.add_argument("thread_id", help="Thread ID")
    bl.add_argument("--reason", default="", help="Block reason")

    # list
    ls = subparsers.add_parser("list", help="List all threads")
    ls.add_argument("--status", choices=VALID_STATUSES, default=None, help="Filter by status")

    # show
    sh = subparsers.add_parser("show", help="Show full thread")
    sh.add_argument("thread_id", help="Thread ID")

    # action-items
    subparsers.add_parser("action-items", help="List open threads needing response")

    args = parser.parse_args()

    if args.command == "new-thread":
        new_thread(args.from_agent, args.to_agent, args.topic, args.message)
    elif args.command == "reply":
        reply(args.thread_id, args.from_agent, args.message)
    elif args.command == "resolve":
        resolve(args.thread_id, args.resolution)
    elif args.command == "block":
        block(args.thread_id, reason=args.reason)
    elif args.command == "list":
        list_threads(status_filter=args.status)
    elif args.command == "show":
        show_thread(args.thread_id)
    elif args.command == "action-items":
        action_items()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
