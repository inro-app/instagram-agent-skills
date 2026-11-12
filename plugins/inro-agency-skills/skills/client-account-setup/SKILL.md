---
name: client-account-setup
description: "Set up a client's Instagram DM automation in Inrō end to end, or take over an account someone else built. Covers what to ask the client first, a read-only pass, the baseline every account needs (contact folders, a priority folder for replies and a helpers folder, opt-out, ice breakers and menu, tracked links, a team hold so automations step back when the client's team replies, exclusions and run limits), AI agent guardrails, the standard inbound automations, QA before go-live, and the update message for the client. Works through the Inrō connector or the partner connector and says exactly which steps happen in the app. Use when you say: set up this client, onboard a new client account, take over this account, go-live checklist, what should every account have, the bot replied while we were talking, write the client update."
license: MIT
---

# Client account setup

Take a client's Instagram account in Inrō from "connected" to "live and safe", or take over one that someone else built. This file is the procedure. The detail is in `references/`.

**Requirements.** One client: the Inrō connector (`https://api.inro.social/mcp`, OAuth). One connection reaches one Instagram account, and that account must be on Pro or Trial. Many clients: the Inrō partner connector (`https://api.inro.social/partner/mcp`, your partner token in an `Authorization: Bearer` header). Every partner call names the client in its `organization` field (prefer the account id from `list_organizations`; a username that matches several accounts is refused), and each client still needs Pro or Trial. Without a connector you can still run the intake, write the plan and the client update, and follow the in-app steps by hand.

| File | What it holds | Read it when |
|---|---|---|
| `references/client-intake.md` | The questions to send the client, and what each answer drives | Before you plan anything |
| `references/baseline.md` | Every baseline item with exact settings, the helper scenarios as build specs, and the in-app steps | Before building, and whenever a step says "baseline" |
| `references/qa-and-go-live.md` | Read-back checklist, test plan, go-live order, first-day watch | Before switching anything on |
| `references/client-update.md` | The client message: structure, rules, a filled template | At the end |

## Safety rules (every session, every client)

1. **Confirm the account before anything.** Call `get_organization_info`. Say back the `username`, `name` and `subscription_tier`, and whether `login_error_data.login_error` is true or `instagram_restrictions` is not empty. If several Inrō connectors are installed, check each one, agree with the user which one is this client, and use only that one. On the partner connector, put the client in every call. Never rely on a default.
2. **Read-only pass first.** Know what is live before you plan a change. Re-read anything older than a few minutes before you write to it: the client's team edits too.
3. **Plan, then OK.** Show the exact text and settings of each change and wait for the user's OK. If they say "align with me first", stop after the plan.
4. **New automations start inactive.** Create every scenario with `active: false`. Template copies also arrive inactive. Switch on only after the user approves go-live.
5. **Never message real contacts as a test.** `scenarios_manage` `test` and the editor's **Test scenario** really send messages. Use your agency's own test Instagram account as the contact. Never use `trigger` or `send_message` on a real contact to "see what happens".
6. **Never delete without explicit approval.** Switching a scenario off is the safe default. Runs already waiting keep going after you switch it off.
7. **One client at a time,** unless the user asked for a bulk change (then use `partner-bulk-rollout`).
8. **Read back after every write** and compare with what you meant to do (section 11).

## Related skills (don't redo their work)

- `instagram-account-audit`: full backup and audit of a live account. Run it first on a takeover.
- `inbound-dm-playbook`: which inbound automations this client should have, in which priority order, and which templates to start from.
- `dm-flow-builder`: build or change one automation step by step.
- `instagram-ai-agent-setup`: the AI agent's knowledge, voice and rules.
- `partner-client-onboarding`: getting a new client into your partner workspace and connected.
- `monthly-client-report` and `multi-client-health-check`: after go-live.

## The phases

| # | Phase | What you do | Output |
|---|---|---|---|
| 1 | Confirm and scope | Safety rule 1. New setup, takeover or review? Who approves: each change, or the plan once? | Account confirmed, scope agreed |
| 2 | Client intake | Send `references/client-intake.md`, read the answers | Rules, facts, open questions |
| 3 | Read-only pass | Section 3. Takeover: `instagram-account-audit` first | What exists, with ids |
| 4 | Plan | Baseline gaps plus the automations from `inbound-dm-playbook`, each with exact text | Plan for the user's OK |
| 5 | Build the baseline | Section 5, `references/baseline.md` | Folders, helpers, settings, each read back |
| 6 | Build the automations | `inbound-dm-playbook` and `dm-flow-builder`, all inactive | Scenarios, each read back |
| 7 | In-app steps | What the connector can't set (section 8) | Done in the app, then read back |
| 8 | QA | `references/qa-and-go-live.md` | Pass or fix list |
| 9 | Go live and watch | Switch on one at a time, check real runs | Confirmed behaviour |
| 10 | Tell the client | `references/client-update.md` | Message ready to send |

## 1. Confirm and scope

- Run safety rule 1. Stop if the tier is not Pro or Trial, the Instagram connection shows a login error, or there are restrictions. Tell the user what to fix first.
- Ask whether another DM automation tool is still connected to this Instagram account. Instagram lets one app control a conversation at a time, and two tools cause locked conversations. Help: https://help.inro.social/en/articles/10485960
- Ask whether this is a new setup, a takeover, or a review of something live, and how the user wants to approve changes.

## 2. Client intake

Send the questions in `references/client-intake.md`. Before building, you need at least:

- What the client sells, the prices they are happy to state in DMs, and the links (shop, booking, WhatsApp, sign-up).
- The questions they answer every day, with their real answers.
- Topics the automation must never handle (refunds, medical or legal questions, custom quotes, complaints) and discount codes that must never be given.
- Who answers DMs today, when, and which email address gets which alert (support, partnerships, sales).
- How they write: three to five real replies they sent.

Never guess prices, codes, policies or opening hours. When the client's latest message and an older document disagree, the latest message wins; say which one you used.

## 3. Read-only pass

Read everything that already exists before planning. Note every id you will need later.

- `scenarios` `list` (then `get` on anything that replies to DMs), `scenario_folders` `list`
- `folders` `list`, `contact_properties` `list`, `conversion_links` `list`
- `agent` `get`, `icebreakers` `list`, `persistent_menu` `get`, `settings` `get_optout`
- `executions` `health` for the last 7 days, if anything is live

On a takeover, also read real conversations: `contacts` `list` ordered by `last_message_at` descending, then `contacts` `list_messages` on 15 to 25 recent ones. Look for three things:

1. **Lines the team keeps typing by hand** after an automation (a link, a price, a policy). Each one is a gap an automation should cover.
2. **Automated messages landing in the middle of a team conversation.** That is the problem the team hold (section 6) fixes.
3. **Two automated replies to one message.** That points at overlapping scenarios outside a priority folder.

## 4. Plan

List the baseline gaps (section 5) and the automations `inbound-dm-playbook` recommends for this business. For each item give: what it does, why, the exact customer-facing text, where it is done (connector or app), and whether it needs the client's answer. Put questions as a numbered list with your recommendation first, so the user can answer "1 yes, 2 b".

## 5. The baseline every client account gets

Defaults, unless there is a reason not to. Exact settings and build specs: `references/baseline.md`.

| Item | Default | Where |
|---|---|---|
| Contact folders | Human only, Team hold (24h), Needs a human, Collabs: requested, plus the temporary windows you need | Connector `folders_manage` |
| Scenario folders | **Inbound DMs** (priority folder) for every automation that replies; **Helpers** (normal folder) for silent ones | Connector `scenario_folders_manage` |
| Team hold | Two helper scenarios, section 6 | Connector, then exclusions in the app |
| Human handover | A scenario with no triggers that the agent runs when someone asks for a person | Connector, wired in the agent |
| AI agent guardrails | Section 7 | Connector `agent_manage`, or the app |
| Opt-out | On, keywords checked against how the client's customers write, confirmation message | Connector `settings_manage` |
| Ice breakers | Up to 4, each answered by a scenario | Connector `icebreakers_manage` |
| Persistent menu | 5 entries or fewer, the opt-out entry included | Connector `persistent_menu_manage` |
| Conversion links | One per destination, tracked, reused by every flow | Connector `conversion_links_manage` |
| Exclusions, run limits, interrupts | Section 8 | Run limits and interrupts by connector; folder exclusions in the app |
| Spam | Spam accounts go to the spam list from the inbox (**Move to spam**) | App, or `contacts_manage` |

Two rules carry most of the design:

- **One reply per inbound message.** Every scenario that replies sits in the Inbound DMs priority folder, so a DM that matches two intents gets one answer. Silent helpers sit in Helpers, so they never block a reply.
- **Humans win.** When the client's team replies by hand, running automations stop, the AI agent pauses, and new automations hold off until the team is done.

## 6. Team hold: automations step back while the team is talking

Why: without it, a new automation can start in a chat the client's team is in the middle of. "Interrupt when you reply manually" stops a scenario that is already running, and the agent's own pause keeps the AI quiet, but neither stops a *new* scripted flow from starting. The hold does.

Build it as two small scenarios in the Helpers folder (exact JSON in `references/baseline.md`, section B3):

```
Team hold: start   Trigger: You send a DM, sent from Instagram or the Inrō inbox only
                   Add to folder "Team hold (24h)" → wait 20 seconds → Trigger a scenario: "Team hold: timer"
                   No run limit, no interrupts, no excluded folders.

Team hold: timer   No trigger of its own
                   Wait 24 hours → remove from folder "Team hold (24h)"
                   "Interrupt when you reply manually" ON. Nothing else. No excluded folders.
```

Why two scenarios: Inrō never starts a scenario for a contact while that same scenario is still running for them, and it drops the new trigger silently. A single 24-hour scenario would never hear the team's second message. Split this way, the start finishes in about 20 seconds and is free again. Each new team message stops the waiting timer and runs the start, which launches a fresh timer. The folder comes off 24 hours after the team's **last** message. The 20-second wait makes sure the new timer starts after the message that stops the old one.

Then:

- Add **Team hold (24h)** to the excluded folders of every scenario that replies, and to the agent's folder rule. Never to the account-wide exclusion: that stops the timer too.
- Set "You send a DM" to Instagram and the Inrō inbox only. By default it also counts AI agent messages, which would put everyone the agent talks to on hold.
- Tell the client's team: removing someone from "Team hold (24h)" hands them back to the automations early.
- Check it on the first real double message from the team: the earlier timer run should show as interrupted (`executions` `list`, reason `manual_reply`) and a new one pending.

The same shape works for any "keep X for N days" window that must survive the main flow being interrupted, such as keeping other flows off a partner's follow-ups for 7 days (`references/baseline.md`, B4).

## 7. AI agent guardrails

The agent itself (knowledge, voice, rules) is `instagram-ai-agent-setup`. These are the settings that decide how it fits with the client's team and flows. App labels first, connector field in brackets.

| Setting | Default for a new client | Why |
|---|---|---|
| Activation rules mode (`trigger_mode`) | **Automation only** (`automation_only`) at go-live | The agent only speaks inside flows you built. Widen later, once you trust it |
| Limit replies based on folders (`folder_rules`) | **Never reply to contacts in these folders**: Human only, Team hold (24h), Needs a human | A clean way to keep the AI off anyone, and off people already escalated (the team removes them from Needs a human when done). It doesn't block AI steps inside scenarios: those need the scenario's excluded folders |
| Human intervention, **Pause the agent when a team member replies** (`human_takeover_active`) | On | The AI never answers on top of the team |
| **Pause the agent for** (`human_takeover_pause`) | 24 hours, to match the team hold. Options: 1, 4, 12, 24 (default 1) | Same window everywhere is easier to explain to the client |
| **Request a human**: "If contact asks to speak to a human, trigger this automation" (`request_human_scenario_id`) | The Human handover scenario (`references/baseline.md`, B5) | A request for a person always reaches the team |
| Knowledge access and behaviour (`no_reply_active`) | **Limit to instructions** for service, health, money or legal topics | The agent says it doesn't know instead of guessing |
| "If the agent cannot reply, trigger this automation" (`no_reply_scenario_id`, only with Limit to instructions) | The Human handover scenario, or its own copy with a different alert subject | Unanswered questions reach the team |

Keep the list of "what goes to a person" word for word the same in three places: the agent's rules, the knowledge base item about handovers, and the Human handover alert email. When one changes, change all three.

## 8. Exclusions, run limits and interrupts

| Scenario | Excluded folders | Run limit | Interrupt when you reply manually |
|---|---|---|---|
| Every scenario that replies, plus story-mention and kind-message helpers | Human only, Team hold (24h) | per flow, see `inbound-dm-playbook` | On |
| Flows that could misfire on a partner's or an unhappy customer's follow-ups (prices, buying, bookings, welcome, AI front desk) | also the temporary windows (Collab window (7d), Complaint window (7d)) | | |
| Human handover | Human only | none | Off |
| Team hold: start, window timers | nothing | none | Off |
| Team hold: timer | nothing | none | **On** |
| Account-wide "Exclude specific contacts" | at most one filter: contact status is Spam. Nothing else | | |

- **"Interrupt when contact replies" stays off everywhere.** It doesn't cut a question or "wait for reply" step short, but it does end AI handovers, button and link waits when the contact writes, which breaks most flows.
- **Never use a permanent tag as an exclusion.** "Collabs: requested" as an exclusion would block that partner from every other flow forever. Exclude a temporary window folder instead, removed by a timer.
- **A helper must never exclude the folder it manages.** Excluded folders are checked at every step, so the helper would stop itself.
- **Human only goes on each scenario, not account-wide.** The account-wide exclusion also stops running helpers, so moving someone to Human only while on hold would leave them stuck in Team hold.
- **Where to set them.** Run limits and interrupts: `scenarios_manage` `update` (`rate_limit_enabled`, `rate_limit_unit`, `rate_limit_value`, `interrupt_on_message`, `interrupt_on_reply`) or the editor. Excluded folders: **in the app only** (the connector reads them as `excluded_folder_ids` but can't set them). Steps for both screens: `references/baseline.md`, B12.

## 9. Engine facts that shape this design

Checked against the current product. If a live response disagrees, the live response wins.

| Fact | What it means for you |
|---|---|
| In a priority folder only the top matching scenario runs. Scenarios whose excluded folders match the contact, or that are over their run limit, are skipped first, so the next one down answers | Order from most specific to most general. An excluded flow hands over to the next one cleanly |
| While a scenario in a priority folder runs for a contact, no other scenario in that folder starts for them | Keep waits short in replying flows (link waits of hours, question waits under 24 hours) |
| A scenario already running for a contact doesn't start again for them, and nothing is logged | Long waits can't react to repeat events: use the start plus timer shape |
| Scenarios take priority over the AI agent. A running scenario holds the agent back | The agent fills gaps around flows, never on top of them |
| "Interrupt when you reply manually" stops every waiting run that has it on, including one started by another scenario | How the team hold timer restarts |
| Excluded folders and the account-wide exclusion are checked at every step | A running flow stops at its next step when the person lands in an excluded folder |
| Switching a scenario off doesn't cancel runs already waiting | Neutralise old logic before replacing it |
| Test runs (test code or **Test scenario**) skip triggers, run limits and excluded folders | They prove the steps, not the routing. Test routing with real messages from your own test account |
| A DM started by a comment gets one message until the person replies | Put the important line in the first DM |
| Instagram lets you reply within 24 hours of the person's last message | Reminders go out around 20 hours, not 24 |
| Several messages sent in a row are grouped into one turn | One reply to a burst, not one per line |

## 10. Build order

1. Folders (`folders_manage` `create`). Use the exact names in `references/baseline.md`, B1: template imports reuse a folder with the same name instead of creating a duplicate.
2. Scenario folders: Inbound DMs (`folder_type: priority`) and Helpers (`normal`).
3. Helpers, inactive: Team hold timer first (the start needs its id), then the start, then Human handover.
4. Conversion links, contact properties.
5. The inbound automations (`inbound-dm-playbook`), inactive, each placed in Inbound DMs with `scenario_folder_id` and `scenario_folder_priority`, then the order set with `scenario_folders_manage` `reorder`.
6. Agent guardrails (section 7), opt-out, ice breakers, menu.
7. In-app steps: excluded folders on every scenario, the account-wide card if needed.

## 11. After every write

Re-read through the same tool and compare: for a scenario, `scenarios` `get` (triggers, every action and its parent and branch, `warnings` with severity `issue`, `active`, folder, priority, run limit, interrupt flags, `excluded_folder_ids`), then `show_scenario` so the user sees the flow. `scenarios_manage` `update` with `actions` replaces the whole list: pass every existing action with its `id`, or the ones you leave out are deleted. Keep a dated change log for the client with the reason for each decision.

## 12. QA, go-live and the client update

- QA and go-live: `references/qa-and-go-live.md`. Short version: every scenario reads back clean, every ice breaker has an answer, AI intents tested on real phrasings in the app, routing tested with your own test account, then switch on one at a time and check the first real runs after a few hours with `executions` `health` and `scenarios` `performance`.
- Client update: `references/client-update.md`. Plain language, what their followers and their team will now see, what the team should do differently, and only the questions you can't decide for them.

## When you get something wrong

Say so plainly, fix it, update the change log, and tell the user what changes. A behaviour seen in a test can differ from real traffic, so confirm new helpers on real events before you call them done.
