# Example: rewriting a client's reel script

A fictional client: a small physiotherapy clinic. Goal of the reel: get people with knee pain to ask for the clinic's free at-home exercise sheet, so the front desk can follow up and book an assessment.

## The script the client sent

> Hi everyone! At our clinic we see a lot of patients with knee pain, and today we wanted to share some tips. Knee pain is really common and can be caused by many different things. It's important to strengthen the muscles around the knee. Here are some exercises that can help. If you have any questions, feel free to send us a message! Don't forget to like and follow for more tips.

What's wrong with it, in short:
- The first line is a greeting. The viewer has learned nothing and has a reason to leave.
- "A lot of patients", "many different things", "some exercises": nothing to picture.
- The value never arrives; it's announced.
- The call to action is three asks with no reason to do any of them.

## The rewrite

**Viewer:** a runner in her forties whose knee aches going down the stairs, who has tried stretching and wonders if she should stop running.

**Idea in one sentence:** the stairs ache usually means weak hips, and one exercise tells you.

| Beat | Spoken | On screen | We see |
|---|---|---|---|
| 1 | "If your knee hurts going down the stairs, the problem is probably not your knee." | NOT YOUR KNEE? | Close-up of a foot stepping down a staircase, wince |
| 2 | "Stand on one leg in front of a mirror and do a small squat." | 1 LEG. SMALL SQUAT. | Physio demonstrates, mirror in frame |
| 3 | "Watch the knee. If it drifts in, like this, your hip isn't holding it." | KNEE DRIFTS IN = HIP | Slow-motion of the knee caving in, arrow |
| 4 | "That's what loads the knee on every step down." | | Cut back to the stairs |
| 5 | "The fix starts with this one: side-lying leg lifts, slow, ten each side." | 10 EACH SIDE, SLOW | Physio on a mat, side view |
| 6 | "We give every runner who walks in a sheet with the next four. Comment SHEET and I'll send it to you." | COMMENT "SHEET" | Physio holding up the sheet, smiling |

What changed:
- The opening names a moment she recognises and contradicts what she expects. She wants to know what it is, if not the knee.
- A test she can do right now arrives by beat 2, the answer by beat 3.
- Every line shows something: the stairs, the mirror, the knee drifting.
- The ask comes after the value, says exactly what she gets, and gives a reason (the clinic gives the same sheet to patients).

## Caption

> Knee hurts on the way downstairs? Comment SHEET for the four exercises we give runners at their first visit.
>
> Try the mirror test from the video before you change your shoes again. We'll send the sheet to your DMs.
>
> #kneepain #runninginjury #physiotherapy

## What the automation needs

- Keyword: SHEET (comments containing it, any case). Not KNEE: people write that word anyway ("my knee does this too"), and every one of them would get the DM.
- First DM: a short line and a button, then the link card to the sheet.
- Follow-up: one nudge a few hours later if the link wasn't tapped (within the 24 hours after their last message, so it can still be delivered).
- Folder: "Knee sheet", so the front desk can offer an assessment later.
- A note on the post for the clinic's AI agent: what an assessment costs and how to book.

Hand this to `client-post-scheduler` to attach it while scheduling the reel, or to `dm-flow-builder` if the clinic wants the DM to ask a question or book an assessment before sending the sheet.
