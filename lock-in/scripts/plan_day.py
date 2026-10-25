#!/usr/bin/env python3
"""Lock In day planner: turns a day's fixed events, flexible routine items and tasks into a
time-blocked plan. Standard library only.

Usage:
  python3 scripts/plan_day.py --sample             # bundled example, touches nothing
  python3 scripts/plan_day.py --input DAY.json      # plan the day in DAY.json
  python3 scripts/plan_day.py --input DAY.json --now 13:20   # re-plan from 1:20 pm
  add --json for machine-readable output (block list for reminders)

All times are the student's local time ("HH:MM", 24-hour). Deadlines are "YYYY-MM-DD HH:MM".
Exit codes: 0 plan printed, 2 input problem (one line on stderr).
"""
import argparse
import json
import os
import sys
from datetime import date, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
SAMPLE = os.path.join(HERE, "..", "assets", "sample_day.json")
SAMPLE_WEEK = os.path.join(HERE, "..", "assets", "sample_week.json")

TRAVEL_KINDS = {"class", "meeting", "interview", "exam"}
PRIORITY_RANK = {"high": 0, "medium": 1, "low": 2}
DEFAULTS = {"buffer_minutes": 10, "max_block_minutes": 90, "break_minutes": 10, "min_block_minutes": 25}


class InputError(Exception):
    pass


def to_min(hhmm, field):
    try:
        h, m = hhmm.strip().split(":")
        h, m = int(h), int(m)
        if not (0 <= h <= 24 and 0 <= m < 60):
            raise ValueError
        return h * 60 + m
    except Exception:
        raise InputError(f"{field}: expected a time like 14:30, got {hhmm!r}")


def fmt(minute):
    h, m = divmod(minute, 60)
    suffix = "am" if h < 12 or h == 24 else "pm"
    h12 = h % 12 or 12
    return f"{h12}:{m:02d}", suffix


def clock(minute):
    t, s = fmt(minute)
    return f"{t} {s}"


def fmt_range(a, b):
    (ta, sa), (tb, sb) = fmt(a), fmt(b)
    return f"{ta}–{tb} {sb}" if sa == sb else f"{ta} {sa}–{tb} {sb}"


def subtract(segments, a, b):
    """Remove [a, b) from a sorted list of free segments."""
    out = []
    for s, e in segments:
        if b <= s or a >= e:
            out.append((s, e))
            continue
        if s < a:
            out.append((s, a))
        if b < e:
            out.append((b, e))
    return out


def plan(day):
    cfg = dict(DEFAULTS)
    cfg.update(day.get("settings") or {})
    try:
        plan_date = date.fromisoformat(day["date"])
    except Exception:
        raise InputError("date: expected YYYY-MM-DD")

    day_start = to_min(day.get("day_start", "07:00"), "day_start")
    day_end = to_min(day.get("day_end", "23:00"), "day_end")
    now = to_min(day.get("now", day.get("day_start", "07:00")), "now")
    now = -(-now // 5) * 5  # round up to the next 5 minutes
    t0 = max(day_start, now)
    if t0 >= day_end:
        raise InputError("now is after day_end; nothing left to plan today")

    blocks, warnings, overflow, skipped = [], [], [], []
    free = [(t0, day_end)]

    # 1. Fixed items never move.
    for i, ev in enumerate(day.get("fixed", [])):
        s = to_min(ev["start"], f"fixed[{i}].start")
        e = to_min(ev["end"], f"fixed[{i}].end")
        if e <= s:
            raise InputError(f"fixed[{i}] ({ev.get('title')}): end must be after start")
        kind = ev.get("kind", "event")
        if e <= t0:
            continue  # already over
        blocks.append({"start": s, "end": e, "title": ev["title"], "kind": kind, "moves": False})
        buf = cfg["buffer_minutes"] if kind in TRAVEL_KINDS else 0
        free = subtract(free, s - buf, e + buf)

    # 2. Flexible routine items (gym, lunch): one piece inside their window, tightest window first.
    flex = list(day.get("flexible", []))
    flex.sort(key=lambda f: to_min(f.get("latest", "23:59"), "latest"))
    for i, f in enumerate(flex):
        need = int(f["minutes"])
        lo = max(to_min(f.get("earliest", "00:00"), f"flexible[{i}].earliest"), t0)
        hi = to_min(f.get("latest", "23:59"), f"flexible[{i}].latest")
        if hi - need < t0 and hi <= t0:
            continue  # its window is already over today; nothing to warn about
        placed = False
        for s, e in free:
            start = max(s, lo)
            if min(e, hi) - start >= need:
                blocks.append({"start": start, "end": start + need, "title": f["title"],
                               "kind": f.get("kind", "routine"), "moves": True})
                free = subtract(free, start, start + need)
                placed = True
                break
        if not placed:
            skipped.append(f["title"])

    # 3. Tasks: due today first (soonest deadline), then by priority, then deadline.
    far = datetime.max
    tasks = []
    for i, t in enumerate(day.get("tasks", [])):
        mins = int(t.get("minutes_left", 0))
        if mins <= 0:
            continue
        due_dt = None
        if t.get("due"):
            try:
                due_dt = datetime.strptime(t["due"], "%Y-%m-%d %H:%M")
            except ValueError:
                raise InputError(f"tasks[{i}].due: expected YYYY-MM-DD HH:MM, got {t['due']!r}")
        pr = PRIORITY_RANK.get(str(t.get("priority", "medium")).lower(), 1)
        due_today = due_dt is not None and due_dt.date() <= plan_date
        tasks.append((0 if due_today else 1, due_dt or far, pr, i, t, mins, due_dt, due_today))
    tasks.sort(key=lambda x: x[:4])

    min_block, max_block, brk = cfg["min_block_minutes"], cfg["max_block_minutes"], cfg["break_minutes"]
    later = []
    for _, _, _, _, t, mins, due_dt, due_today in tasks:
        cutoff = day_end
        if due_today:
            cutoff = min(day_end, due_dt.hour * 60 + due_dt.minute) if due_dt.date() == plan_date else t0
        # Spread work that isn't due today across the days left, so Friday's project
        # doesn't swallow Monday night. Work due early in the morning counts the day before.
        # Only big work (more than one block) is spread; short tasks are done in one sitting.
        target = mins
        if due_dt is not None and not due_today and mins > max_block:
            days_left = (due_dt.date() - plan_date).days + (1 if due_dt.hour >= 12 else 0)
            days_left = max(days_left, 1)
            share = -(-mins // days_left)
            target = min(mins, max(-(-share // 5) * 5, min_block))
            if mins - target < min_block:
                target = mins  # don't leave a scrap for another day
        remaining, chunks = target, []
        # Short tasks go in one piece when a gap fits them, unless that would push the start
        # back more than 90 minutes compared with starting in the first usable gap.
        first_usable = next((s for s, e in free if min(e, cutoff) - s >= min(min_block, target)), None)
        if target <= max_block and first_usable is not None:
            for s, e in free:
                if min(e, cutoff) - s >= target:
                    if s - first_usable <= 90:
                        chunks.append((s, s + target))
                        remaining = 0
                    break
        if remaining > 0:
            for s, e in list(free):
                if remaining <= 0:
                    break
                cursor, seg_end = s, min(e, cutoff)
                while remaining > 0 and seg_end - cursor > 0:
                    size = min(remaining, max_block, seg_end - cursor)
                    leftover = remaining - size
                    if 0 < leftover < min_block:
                        size = remaining - min_block  # never leave a scrap smaller than a block
                    if size < min_block:
                        break  # gap too short to be worth starting
                    chunks.append((cursor, cursor + size))
                    remaining -= size
                    cursor += size + brk
        chunks.sort()
        for a, b in chunks:
            free = subtract(free, a, b + brk)
        n = len(chunks)
        for k, (a, b) in enumerate(chunks):
            label = t["title"] if n == 1 else f"{t['title']} ({k + 1}/{n})"
            blocks.append({"start": a, "end": b, "title": label, "kind": "task", "moves": True,
                           "task": t["title"]})
        if remaining > 0:
            if due_today and due_dt.date() < plan_date:
                warnings.append(f"{t['title']} was due {due_dt.strftime('%b')} {due_dt.day} (overdue)")
            elif due_today:
                warnings.append(f"{t['title']} is due {clock(cutoff)}: only {target - remaining} "
                                f"of {target} min fit before then")
            overflow.append({"title": t["title"], "minutes": remaining, "due_today": due_today})
        if mins - target > 0:
            when = f"due {due_dt.strftime('%a')} {clock(due_dt.hour * 60 + due_dt.minute)}"
            later.append({"title": t["title"], "minutes": mins - target, "when": when})

    if skipped:
        warnings.append("No room today for: " + ", ".join(skipped))

    blocks.sort(key=lambda b: (b["start"], b["end"]))
    return {"date": plan_date.isoformat(), "from": t0, "blocks": blocks,
            "overflow": overflow, "later": later, "warnings": warnings}


def plan_week(week):
    """Plan several days in a row. Work scheduled on one day is taken off before the next, so
    unfinished work rolls forward and every deadline is checked across the whole week."""
    tasks = [dict(t) for t in week.get("tasks", [])]
    days_out, problems = [], []
    for i, day in enumerate(week.get("days", [])):
        d = dict(day)
        d.setdefault("settings", week.get("settings") or {})
        d["tasks"] = [t for t in tasks if int(t.get("minutes_left", 0)) > 0]
        if i > 0 or "now" not in d:
            d["now"] = d.get("day_start", "07:00")
        res = plan(d)
        done = {}
        for b in res["blocks"]:
            if b.get("task"):
                done[b["task"]] = done.get(b["task"], 0) + (b["end"] - b["start"])
        for t in tasks:
            t["minutes_left"] = int(t.get("minutes_left", 0)) - done.get(t["title"], 0)
        dd = date.fromisoformat(res["date"])
        label = f"{dd.strftime('%a %b')} {dd.day}"
        for w in res["warnings"]:
            problems.append(f"{label}: {w}")
        days_out.append({"date": res["date"], "label": label, "study": done, "result": res})
    unplanned = [t for t in tasks if t["minutes_left"] > 0]
    return {"days": days_out, "unplanned": unplanned, "problems": problems}


def hours(m):
    h, r = divmod(m, 60)
    return f"{h}h{r:02d}" if h and r else (f"{h}h" if h else f"{r}m")


def render_week(wk):
    lines = ["Week plan"]
    for d in wk["days"]:
        work = " · ".join(f"{k} {hours(v)}" for k, v in d["study"].items()) or "free"
        lines.append(f"{d['label']}: {work}")
    if wk["unplanned"]:
        lines.append("")
        lines.append("Still not planned by the end of the week:")
        for t in wk["unplanned"]:
            due = f", due {t['due']}" if t.get("due") else ""
            lines.append(f"- {t['title']} ({hours(t['minutes_left'])}{due})")
    if wk["problems"]:
        lines.append("")
        lines.append("Heads up:")
        for p in wk["problems"]:
            lines.append(f"- {p}")
    return "\n".join(lines)


def render_text(result):
    d = date.fromisoformat(result["date"])
    t, s = fmt(result["from"])
    lines = [f"{d.strftime('%a %b')} {d.day} plan, from {t} {s}"]
    for b in result["blocks"]:
        lock = "" if b["moves"] else " 🔒"
        lines.append(f"{fmt_range(b['start'], b['end'])}  {b['title']}{lock}")
    if result["overflow"]:
        lines.append("")
        lines.append("Didn't fit today:")
        for o in result["overflow"]:
            lines.append(f"- {o['title']} ({o['minutes']} min)")
    if result["later"]:
        lines.append("")
        lines.append("Saved for later days:")
        for o in result["later"]:
            lines.append(f"- {o['title']} ({o['minutes']} min, {o['when']})")
    if result["warnings"]:
        lines.append("")
        lines.append("Heads up:")
        for w in result["warnings"]:
            lines.append(f"- {w}")
    return "\n".join(lines)


def to_json(result):
    def hhmm(m):
        return f"{m // 60:02d}:{m % 60:02d}"
    out = dict(result)
    out["from"] = hhmm(result["from"])
    out["blocks"] = [dict(b, start=hhmm(b["start"]), end=hhmm(b["end"])) for b in result["blocks"]]
    return json.dumps(out, indent=2, ensure_ascii=False)


def main():
    ap = argparse.ArgumentParser(description="Lock In day planner")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--input", help="day file (JSON)")
    src.add_argument("--sample", action="store_true", help="plan the bundled sample day")
    src.add_argument("--week", help="week file (JSON with days and tasks): plan every day in a row")
    src.add_argument("--sample-week", action="store_true", help="plan the bundled sample week")
    ap.add_argument("--now", help="re-plan from this local time (HH:MM), overriding the file")
    ap.add_argument("--json", action="store_true", help="print JSON instead of text")
    args = ap.parse_args()

    weekly = bool(args.week or args.sample_week)
    if args.sample_week:
        path = SAMPLE_WEEK
    else:
        path = SAMPLE if args.sample else (args.week or args.input)
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        if weekly:
            if args.now and data.get("days"):
                data["days"][0]["now"] = args.now
            wk = plan_week(data)
            if args.json:
                print(json.dumps({"days": [{"date": d["date"], "minutes_by_task": d["study"]}
                                           for d in wk["days"]],
                                  "unplanned": wk["unplanned"], "problems": wk["problems"]},
                                 indent=2, ensure_ascii=False))
            else:
                print(render_week(wk))
            return 0
        day = data
        if args.now:
            day["now"] = args.now
        result = plan(day)
    except FileNotFoundError:
        print(f"Day file not found: {path}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"Day file is not valid JSON: {exc}", file=sys.stderr)
        return 2
    except (InputError, KeyError, ValueError, TypeError) as exc:
        print(f"Problem in the day file: {exc}", file=sys.stderr)
        return 2
    print(to_json(result) if args.json else render_text(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
