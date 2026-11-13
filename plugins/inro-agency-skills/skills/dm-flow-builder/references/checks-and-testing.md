# Checks, testing and fixing

## Before you show it to the user

Read the scenario back with `scenarios` get, call `show_scenario`, and go through this list.

**Trigger**
- [ ] The trigger type and options are what the brief says, including which posts a comment trigger watches (all, chosen, caption word, next post).
- [ ] Keywords are distinctive, and checked against the client's captions and recent comments.
- [ ] An AI intent is one short, narrow sentence, and does not overlap another active flow's intent.
- [ ] No other active scenario fires on the same comment, story reply or DM, or both sit in a priority scenario folder in the right order.

**Steps**
- [ ] One root step, one step per branch, every step on a branch its parent actually has.
- [ ] After a comment, the first DM asks for a tap or reply; the link comes after it.
- [ ] No raw URL in message text. Links go in link cards.
- [ ] Every link card points at the client's URL, not a template or example URL.
- [ ] Every folder step points at one of the client's folders.
- [ ] Alert emails have a real address. In your own builds they sit last in their branch. Some templates put the alert mid-branch: leave it there, and if you remove it, give the step after it a new parent.
- [ ] Timeouts are in hours, inside the 24-hour window.
- [ ] Messages read well with variables filled in, and no two consecutive messages are identical.
- [ ] AI steps: the agent is set up for this topic (`agent` get), and the account has AI features and credits.
- [ ] The flow does not contradict the client's guardrails (a booking link where the brand never pushes calls, a discount the client did not approve).

**Settings**
- [ ] `active` is false.
- [ ] Run once (or once per period) is on for lead flows.
- [ ] `interrupt_on_message` is on wherever a person may step in.
- [ ] Customers and the team are excluded per scenario: `excluded_folder_ids` in `scenarios` get lists the right folders (set with `scenarios_manage` update or **Exclude specific folders** in the app). The account-wide **Exclude specific contacts** card is for spam only.
- [ ] Opt-out is on for the account.
- [ ] The name says the entry point and the outcome.

**Warnings**
- [ ] No warning with severity `issue` in the create or update response, or in `show_scenario`.
- [ ] Every `suggestion` is either fixed or explained to the user.

Common warnings and what they mean:

| Warning says | Fix |
|---|---|
| Meta may block messages containing links | Move the link into a link card |
| This message might not be received | A second DM straight after a comment, with nothing waiting for the person. Put a button, question or wait step first |
| Only one action can start the flow | Several root steps. Chain them |
| 2 actions share this branch, but only one runs | Chain them one after the other |
| This action never runs: the branch ... does not exist on the action above | Use one of the branch labels it lists |
| Email address is empty | Add the team's address to the alert email (templates ship without one) |
| No event selected (a Meta pixel step) | Pick the client's pixel event, or delete the step if the client has no pixel |
| The ice breaker this trigger answers is no longer on your Instagram profile | Point the trigger at a payload from the client's `icebreakers` list |
| The key is used by several actions | Make every `action_key` unique |
| No link selected / the link no longer exists | Pick or recreate the link |
| A keyword branch has no keywords | Add keywords or remove the branch |
| The selected scenario is inactive | A `trigger_scenario` target must be active |
| AI features disabled / AI agent messages are disabled | Turn AI on for the account, or remove the AI step |

## Testing without messaging real contacts

Never test on a customer, and never use `scenarios_manage` `trigger`, `campaigns_manage` `send` or `resend` as a test.

**Option 1: the test code.** Open the scenario in the app, click **Test scenario**, and copy its test code. From your own or a team member's Instagram account:
- send the code as a DM to the client's account, for DM, story and welcome flows;
- or comment the code on one of the client's posts, for a comment flow. The flow will reply publicly under that comment, so use an older post and delete the comment after.

The flow runs as a test for that account only, even while the scenario is switched off.

**Option 2: test on a contact.** `scenarios_manage` `test` with `scenario_id` and `contact` (`username`, `id` or `email`) set to your own account's contact. It runs once, even if switched off, and really sends the messages to that contact. If that contact has not written to the client's account in the last 24 hours, the DM is held: send the test code by DM first, then test again.

**Campaigns.** `campaigns_manage` `test` with `campaign_id` and your own contact. It works on a draft or a scheduled campaign and sends nothing to the audience.

**What a test does not prove.** Test runs are kept out of the results, and they skip the run-once limit, excluded folders and the account exclusion filter. The run records a note for each rule it skipped. Check those rules by reading the settings, not from the test.

**Read the test run.** `executions` list with `scenario_id` and `include_test: true`, then `executions` get on the run: every step, its status, and any error. For AI steps, each test on a contact starts clean, so earlier test answers do not leak into a new test.

## After switching on

- Within the first day, read `scenarios` performance (runs reaching and finishing each step) and a few real runs in `executions`.
- In the app, the scenario's **Results** show runs, conversions (link clicks, survey completions, payments) and per-step numbers; any non-zero number opens the list of people behind it. The **History** tab lists every run.
- A step with failed runs can be retried from the app, or one by one with `executions_manage` retry. Retrying sends messages to real people, so it needs the user's OK.
- Editing a live scenario applies to new runs. People already in the flow continue on the version they started.

## When a flow does not fire

Work in this order, all reads:

1. `get_organization_info`: is Instagram connected? A broken connection pauses every automation.
2. `executions` health: account-level blockers (disconnection, contact limit reached) and the flows failing most.
3. `scenarios` get: is it active? Is the trigger what you think? For a comment flow, is the post still the same post (a deleted and re-uploaded post has a new id)?
4. `scenarios` performance: which step people reach and why the others stopped (`reason_code`).
5. `executions` list filtered by `scenario_id` and status or `reason_code`, or by `contact_id` to answer "did it ever run for this person?". An empty result for a contact means the cause is before the flow: the trigger never matched.

Usual causes:

| Cause | What you see |
|---|---|
| Scenario switched off or suspended | `active` false, or a suspended badge in the app |
| Keyword never used as written, or AND logic needing every keyword | No runs at all |
| Run once already used for that person | No new run for that contact |
| Contact in an excluded folder, or matching the account exclusion | `contact_in_excluded_folder`, `contact_matches_exclusion_filter` |
| Another scenario in the same priority folder won | A sibling ran instead |
| Comment older than 7 days | Nothing can be sent: Instagram no longer accepts a private reply to it |
| A second DM after a comment, and the person never replied or tapped | `dm_held_private_reply` |
| Person outside the 24-hour window | `dm_held_window` |
| Contact limit for the month reached | `plan_limit_reached`, runs shown as limited |
| Another tool connected to the account holds the conversation | The thread ownership error in the app |
| Message step over 1,000 characters | The step fails |

## Changing a flow safely

- `scenarios` get first. Build the update from it.
- Send the complete actions list: `{ "id": 123 }` keeps a step as it is; `{ "id": 124, "content": "New text" }` changes one field. `options` counts as one field and is replaced whole: send the step's full `options` from `get` with your change in it, or the other options are wiped (an alert email loses its subject and body). A step without `id` is new and needs an `action_key` and a parent. Anything left out is deleted.
- Triggers: include `id` on the triggers you change, and the others are kept. A triggers list with no ids replaces every trigger, and a webhook trigger then gets a new URL.
- For big structural changes to a live flow, switch it off first (with the user's OK), change it, test, then switch it back on.
- If updates keep failing on one scenario, build a corrected copy as a new scenario, switched off, test it, and switch the old one off on approval. Delete the old one only if the user explicitly asks.
