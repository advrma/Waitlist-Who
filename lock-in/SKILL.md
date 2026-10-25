---
name: lock-in
description: Plans a student's day hour by hour from their classes, Canvas deadlines, meetings and daily routine, texts the plan each morning, nudges them at each block, and re-plans when they fall behind. Use when the student says "lock me in", asks what to do today or this week, says they're behind or need more time on something ("I need another hour on HW4", "running 30 late", "skipped the gym"), wants a morning plan or daily reminders, or wants their routine, classes and deadlines on one schedule. Prefer it over a general study plan whenever the student wants exact times or live rescheduling.
---

# Lock In

Gives the student one plan for the day, with times, built from everything that competes for it: classes,
meetings and interviews, assignment deadlines, and their own routine (wake up, gym, meals). It texts the plan
every morning, nudges them when each block starts, and re-plans the rest of the day whenever they text that
something took longer or got skipped.

Cubbie gathers the data; `scripts/plan_day.py` does the time math so blocks never overlap and deadlines are
checked exactly. The script needs only Python's standard library, so there's nothing to install.

## When to use

- "lock me in for today" / "what do I do today?"
- "I need another hour on HW4"
- "running 30 min late, fix my day"
- "set up my routine: up at 7, gym after class, bed by 12"
- "plan my week"

Do not use it to watch class seats or enroll (that's Class Sniper), or to write the assignments themselves.

## Where things are saved

Keep the student's setup in files under `~/.config/lock-in/`, so it survives restarts and Skill updates:

- `profile.json`: day start and end, the routine, the weekly class schedule with the term's last day, nudge
  and check-in times.
- `tasks.json`: assignments and to-dos with title, course, due ("YYYY-MM-DD HH:MM"), minutes left, priority
  (high, medium or low) and the Canvas link if there is one.
- `day-YYYY-MM-DD.json`: the plan input for one day, in the format of `assets/sample_day.json`.

Also remember the routine and preferences in Cubbie's memory, so setup is never asked twice.

## Setup (once)

Ask one thing at a time, each with a default the student can accept with "yes".

1. **Classes.** Ask for a screenshot of their class schedule from My ASU (any school's schedule page works).
   Read each class: name, days, start and end times, location, and the term's last day. If the student
   prefers and is signed in to My ASU in Cubbie's browser, open the schedule there instead. Show the list
   and ask them to confirm it.
2. **Routine.** Ask for their usual day: wake-up and bedtime, plus anything regular (shower, meals, gym,
   commute, work shifts). For each, ask whether it's at a set time (fixed) or can move within a window
   (flexible, like "gym sometime 5 to 8:30 pm, 1 hour"). Weekday and weekend routines can differ.
3. **Deadlines.** Read the student's Canvas assignments due in the next 14 days, leaving out anything already
   submitted. If Canvas is not connected, ask them to connect it, or to list what's due.
4. **Meetings and interviews.** Search the student's email and Google Calendar for the next 14 days for
   interviews, meetings and appointments. If Google is not connected, ask them to list any.
5. **Calendar.** Offer to put classes (as recurring events until the term's last day) and any meetings found
   in email onto their Google Calendar. Show the list and add it only after one clear yes.
6. **Check-ins.** Propose, then create only after the student says yes:
   - a morning plan every day, 15 minutes after their wake-up time
   - a weekly planning check-in, Sunday at 7 pm
   - nudges at the start of every block (or only study blocks, if they prefer)

## Weekly check-in (Sunday)

1. Refresh `tasks.json` from Canvas (next 8 days) and the email and calendar search above.
2. For each new assignment, ask how long it'll take, one at a time, with a guess as the default:
   "CSE 340 HW4, due Thu. About 2 hours?" Problem sets and labs default to 2 hours, readings to 45 minutes,
   essays and projects to 3 hours split across days. Ask about priority only if two things clash.
3. Text a short week preview: the heaviest day, anything due before Wednesday, and any day with no room.

## Morning plan

1. Build today's `day-YYYY-MM-DD.json`:
   - `date`, `now` (the student's local time), `day_start`, `day_end` from the profile.
   - `fixed`: today's classes (`"kind": "class"`), meetings and interviews from the calendar (`"meeting"` or
     `"interview"`), exams (`"exam"`), and fixed routine items (`"routine"`).
   - `flexible`: flexible routine items with `minutes`, `earliest` and `latest`.
   - `tasks`: everything in `tasks.json` that isn't done, with `minutes_left`, `due` and `priority`.
   Mark Canvas assignments that are now submitted as done first.
2. Run: `python3 scripts/plan_day.py --input ~/.config/lock-in/day-YYYY-MM-DD.json`
3. Text the plan it prints. It already reads well as a text: times, then the block; 🔒 marks things that
   can't move. Add one line on top with the most important thing today.
4. If there's a "Heads up" line, ask what to do about it, with options: shorten or skip a flexible item
   (gym, a meal break), push a low-priority task, or draft an extension email to the professor (Cubbie's
   own professor-email Skill does this; the student sends it).
5. Create today's nudges: run the same command with `--json` and set a one-time reminder at each block's
   `start` (or only for `"kind": "task"` blocks, per the student's choice). Word each one so it stands on its
   own: "Lock In: 9:10 am, start CSE 340 HW4 (part 2 of 2), until 9:40."

## Re-planning ("I need another hour")

Whenever the student says something took longer, they're running late, they finished early, skipped
something, or something new came up:

1. Update the day file: add the extra time to that task's `minutes_left` (or set what's actually left),
   mark finished tasks done in `tasks.json`, remove skipped flexible items, add new fixed events.
2. Run: `python3 scripts/plan_day.py --input ~/.config/lock-in/day-YYYY-MM-DD.json --now HH:MM`
   with the student's current local time.
3. Cancel today's remaining Lock In nudges and create new ones from the new plan.
4. Reply with what changed first, then the rest of the day. For example:
   Got it, HW4 +1h. Moved: ECN reading to 2:55, resume edits to 6 pm.
   Then the updated plan.

Classes, meetings, interviews, exams and fixed routine items never move, and the script enforces this.
Deadlines due today come first; work due later in the week is spread across the days left, so one big
project doesn't swallow a whole night.

## Replies

Keep replies to a few short lines, plain text, no Markdown. The day plan is the one long message; send it
on its own. Lead nudges with the time and the task. Ask one question at a time and suggest a default the
student can accept with "yes". Don't lecture about productivity; just help.

## When something fails

- Canvas or Google not connected: ask the student to connect it or to type the missing items, and keep going.
- The schedule screenshot is unreadable: ask for a clearer one, or for the classes typed out.
- The script prints "Problem in the day file": fix the field it names and run it again. Don't hand-write a
  plan instead, because the times could overlap.
- Nudges can't be created: tell the student once, and offer to put today's blocks on their Google Calendar
  with notifications instead (only after a yes).
- The day is already over or has no room: say so and offer to plan tomorrow.

## Privacy

Keep the schedule, routine and tasks in the student's own files and Cubbie's memory. Don't send them anywhere else.
