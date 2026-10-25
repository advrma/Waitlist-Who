# Class Sniper + Lock In

Two Cubbie Skills for ASU students, built for the Cubbie Hackathon (Track 1).

- **Class Sniper** (`class-sniper/`): reads your DARS and recommends next semester's classes, watches full
  sections on ASU Class Search, calls you the moment a seat opens, and enrolls you when you reply YES.
- **Lock In** (`lock-in/`): turns your classes, Canvas deadlines, meetings and daily routine into one
  time-blocked plan, texts it every morning, nudges you at each block, and re-plans the day when you text
  "I need another hour."

## Install on Cubbie

Text this repository's link to Cubbie and reply "yes" when it asks. Both Skills install.

To install just one, text the link to its folder, for example `.../tree/main/class-sniper`.

## Try Lock In's planner locally

```bash
python3 lock-in/scripts/plan_day.py --sample        # one day
python3 lock-in/scripts/plan_day.py --sample-week   # a whole week, planned backward from deadlines
```

Python 3.9+, standard library only.
