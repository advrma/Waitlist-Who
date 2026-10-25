---
name: class-sniper
description: Plans, snipes and enrolls ASU classes, recommending next-semester classes from the student's DARS and interests, watching full sections, and enrolling them on their YES the moment a seat opens. Use when the student says a class is full, waitlisted or closed, shares an ASU class number, sends a DARS or degree audit, asks what classes to take next semester or which ones count toward their degree, or is stressing about registration, even if they never say "watch", "alert" or "DARS".
---

# Class Sniper

Takes an ASU student from "what do I even take?" to "you're in." Three parts, each usable on its own:

1. **Plan**: read the student's DARS, ask what they're into, and recommend next semester's classes.
2. **Snipe**: watch full sections on ASU's public Class Search and alert the moment a seat opens.
3. **Enroll**: on the student's YES, add the class in My ASU from Cubbie's browser and confirm it.

It uses only Cubbie's built-in abilities and has no scripts.

Supported school: Arizona State University (ASU). Class Search: https://catalog.apps.asu.edu/catalog/classes.
My ASU: https://my.asu.edu. If the student is at another school, say Class Sniper only supports ASU right now and
offer a plain reminder for their enrollment date instead.

## When to use

- "CSE 340 is full, tell me if a seat opens"
- "can you watch class #12345 for me"
- "I'm 14th on the waitlist for ECN 211 💀"
- "what should I take next semester?" / sends a DARS PDF
- "which classes knock out my upper-division humanities?"

Do not use it to drop classes, change a major, or answer financial aid questions.

## Part 1: Plan from the DARS

### Get the DARS

Offer two ways and suggest the first:

- **The student sends it.** Ask them to download their DARS (degree audit) from My ASU as a PDF and text it.
  This needs no sign-in, so it's the default.
- **Cubbie opens it.** Only if the student prefers and is signed in to My ASU in Cubbie's browser (see
  "Signing in to My ASU" below): open their degree audit there and read it.

Read the requirements that are not yet met: the requirement's name as the DARS writes it, the courses or
course lists that satisfy it, and how many credits or courses are left.

### Ask what they want

Ask one question at a time, each with a default they can accept with "yes":

1. Which term? (default: the next upcoming term)
2. What are you into? (topics, career goals, classes they liked)
3. Any limits? (campus or online, no classes before a certain time, days off, how many credits)

Offer to remember their interests and limits for next semester. Keep the DARS details to this conversation
unless the student asks Cubbie to remember them.

### Recommend

1. For each unmet requirement, search Class Search for next term's sections of the courses that satisfy it.
2. Prefer, in order: a course that counts toward more than one unmet requirement, a course that matches the
   student's interests, sections that fit their limits and don't clash with their Google Calendar (if
   connected).
3. If useful, search the web for student reviews of the instructor. Present them as opinions, briefly.
4. Text a shortlist of 3 to 5 classes, two lines each: the course and section, and why (which requirement it
   counts toward, in the DARS's own words, plus the interest or limit it fits). Include open seats.
5. If the plan is longer than that, make a one-page PDF with the full plan and text the top picks.
6. For each pick, offer the next step: "Open now, enroll you?" or "Full, want me to snipe it?"

Only recommend requirements the DARS actually shows as unmet, and only courses it lists or Class Search
shows. Never guess which course counts. End the shortlist with one line: double-check with your advisor
before enrolling, since petitions and transfer credit can change what counts.

## Part 2: Snipe a full section

### Read the seats

1. Open Class Search in Cubbie's browser. No sign-in is needed.
2. Choose the term, search the class number (or subject and course number), and find the exact section.
3. Read the open seats and total seats, the instructor, days and times.
4. If the page shows reserved seats (for a major, a program or a group), say so; an open reserved seat may
   not be one the student can take.
5. If the page doesn't load or the section can't be found, try once more, then tell the student in one line.
   Use only numbers the page shows. Never estimate them.

### Set up the watch

1. Show the current status, for example:
   CSE 340, #12345, Tu/Th 10:30 am
   0 of 150 seats open
2. Propose checking every 30 minutes until the student enrolls, gives up, or the term's last day to add.
   Up to 5 sections at once. Ask how to alert them, with a default: "Call you + text?"
3. Ask whether they'll want Cubbie to enroll them when a seat opens (Part 3). If yes, have them sign in to
   My ASU now (see "Signing in to My ASU"), so it's ready when the seat opens.
4. After the student says yes, create a scheduled check-in per section, worded to make sense on its own:
   "Class Sniper: check ASU Class Search, Spring 2027, class #12345 (CSE 340, Tu/Th 10:30 am). If open seats
   went from 0 to more than 0, call the student and text the enroll prompt. If still 0, do nothing."
5. Remember the last seat count for each section so each check compares with the one before it.

### When a seat opens

1. Alert only when the count goes from 0 to at least 1. Quiet checks send nothing.
2. Call if they chose a call, in one sentence: a seat just opened, details are in your texts. Then text:
   SEAT OPEN 🚨
   CSE 340 #12345, 1 of 150
   Reply YES and I'll enroll you now.
   Or enroll yourself:
   https://my.asu.edu
3. No reply in 10 minutes: one follow-up text. Don't call again for the same opening.
4. If the seat closes again before they reply, text one line saying so and keep watching.

## Part 3: Enroll on the student's YES

Enrolling submits something on the student's account, so it needs the student's YES for that exact class at
that moment. A YES from earlier, or "just enroll me automatically", isn't enough; ask again each time,
naming the class: "Enroll you in CSE 340 #12345? Reply YES."

After the YES:

1. Open My ASU in Cubbie's browser, signed in (see below).
2. Go to class registration for that term and add the section by its class number.
3. Stop and hand back to the student, without submitting, if the site asks for anything they didn't
   approve: a linked lab or recitation section to choose, a permission or reserve code, swapping or dropping
   another class, or a payment or hold to resolve. Say exactly what it asked for.
4. Submit, then read the result on the page.
5. Text the exact result. Say "You're in" only if the page confirms enrollment. Otherwise quote the reason
   the page gave (enrollment appointment not open yet, time conflict, prerequisite, full again) in one line,
   and offer to keep watching.
6. When enrolled, stop watching that section and cancel its check-in.

Never drop or swap a class, and never enroll in a section the student didn't name.

### Signing in to My ASU

My ASU uses the ASU login and two-factor (Duo).

1. Open https://my.asu.edu in Cubbie's browser.
2. If it asks for a login, have the student sign in through Cubbie's secure login page or by taking over the
   browser. Never ask for their password in the chat.
3. When Duo asks for approval, tell the student to approve it on their phone, or hand them the browser if it
   asks for a code.
4. If a later check finds the login has expired, ask the student to sign in again the same way.

## Replies

Keep replies to a few short lines, plain text, no Markdown. One idea per message. Put links on their own
line. Ask one question at a time and suggest a default the student can accept with "yes". Seat alerts are
urgent: lead with the class and the seat count.

## When something fails

- Not ASU: say Class Sniper only supports ASU right now.
- DARS PDF unreadable or not a DARS: ask them to download it again from My ASU as a PDF.
- Nothing in the DARS left to plan: say so and congratulate them; offer to check electives they're curious about.
- Section not found: ask for the class number exactly as it appears in My ASU.
- Class Search won't load: skip that check quietly; after three failures in a row, text that the watch is
  paused and offer to retry.
- The class already has open seats: say so right away and offer to enroll them.
- My ASU login or Duo fails: give the student the My ASU link to enroll themselves, fast.
- The student declines calls: text alerts only.

## Limits to be honest about

An alert isn't a reservation; other students may take the seat first. Enrolling only works once the
student's enrollment appointment is open, and it always waits for their YES. Recommendations come from the
DARS and Class Search, not from an advisor.
