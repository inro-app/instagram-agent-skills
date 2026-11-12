# Example walkthrough (fictional client)

One quick win from a plan, built end to end. The studio, the handles and the links are invented.

## 1. Confirm

> Connected account: **@example.yoga.studio** (Northside Yoga), plan Pro, Instagram connected, opt-out on. Is this the client we are building for?

User: yes.

## 2. Read first (no changes)

- 3 scenarios, 1 active: "Comments: TIMETABLE to timetable" on one pinned post.
- No other active comment flow, so a flow on posts with TRIAL in the caption will not collide.
- Folders: Commented, Members. No "Intro offer clicked" folder yet.
- Opt-out on. The AI agent is off, so no AI steps in this build.

## 3. The plan shown before any write

> I'll create one scenario, **switched off**:
>
> **Comments: TRIAL to intro offer**
> - Starts when someone comments TRIAL on any post whose caption contains TRIAL. Hateful and negative comments are skipped.
> - Replies under the comment, one of: "Sent, check your DMs" / "Just sent it to your DMs" / "It's in your DMs now", and likes the comment.
> - DM: "Hi {name}! Want the intro offer? Tap below." with one button, "Send it".
> - After the tap: a link card "Intro offer" to https://example.com/intro, button "See the offer".
> - If they open it: added to a new folder "Intro offer clicked" (I'll create this folder).
> - If they don't open it within 3 hours: "Did you get a chance to look at the offer?"
> - Runs once per person. Stops if your team replies by hand.
>
> Shall I create the folder and the scenario?

User: yes, go.

## 4. Build and check

- `folders_manage` create "Intro offer clicked".
- `scenarios_manage` create with `active: false` (shape: recipe 3 in `references/recipes.md`).
- Response warnings: none with severity `issue`.
- `show_scenario` for the user to see the flow.
- `scenarios` get: triggers, branches, link URL, folder id and settings all as planned.

## 5. Test on our own account

> To test without reaching anyone real: open the scenario in Inrō, click **Test scenario**, copy the test code, and comment it from your own Instagram account on an older Northside post. Tell me when it's done.

Then `executions` list with `include_test: true`: the reply, the DM, the tap, the link and the folder step all completed. The comment is deleted afterwards.

> Note: test runs skip the run-once rule and excluded folders, so those were checked in the settings instead.

## 6. Switch on

> The test went through every step. Switch on **Comments: TRIAL to intro offer** now?

User: yes.

- `scenarios_manage` update with the id and `active: true`.

> It's on. Inrō also offers **Catch up** for matching comments from the last 7 days. It shows 37 people. Do you want to send it to them?

User: not now.

## 7. First day

- `scenarios` performance the next morning: runs, how many tapped, how many opened the link.
- A few runs read in `executions` to check that real comments matched as expected.
