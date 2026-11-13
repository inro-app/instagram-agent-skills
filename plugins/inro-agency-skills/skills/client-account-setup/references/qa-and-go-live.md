# QA, go-live and the first day

Nothing goes live until every check below passes or the user has accepted the gap in writing.

## 1. Read-back checklist (connector, read-only)

Run it on the confirmed account (`get_organization_info` first). On the partner connector, name the client in every call.

**Every scenario you built or changed** (`scenarios` `get`, then `show_scenario`):
- [ ] `active` is false until go-live.
- [ ] Triggers are the ones in the plan. AI-detected intents have their text; keyword triggers have at least one keyword.
- [ ] Every action is present, with the right parent and branch. No action shows a warning with severity `issue` (an empty alert email, a deleted link, a raw URL in text, a second DM straight after a comment reply).
- [ ] Every branch ends in a reply, an AI handover, or an alert to the team, including the "expired" branches.
- [ ] Every link step points at the client's real URL, not a template placeholder.
- [ ] Every alert email has the client's recipient address.
- [ ] `excluded_folder_ids` includes Human only and Team hold (24h) on replying flows (section 8 of SKILL.md), and no helper excludes the folder it manages.
- [ ] Run limit and interrupt flags as planned. "Interrupt when contact replies" (`interrupt_on_reply`) is off.
- [ ] Folder and priority: replying flows in Inbound DMs in the planned order (read the order back with `scenarios` `list`: `scenario_folder_id` as a string, `order_column: "scenario_folder_priority"`, `order_direction: "asc"`; `scenario_folders` `get` shows only the count), silent ones in Helpers.

**Account settings:**
- [ ] `icebreakers` `list`: 4 or fewer, each answered by the scenario you built (or by the agent). The list also shows switched-off scenarios, so after go-live check again that each entry has an `automations` entry with `active: true`.
- [ ] `persistent_menu` `get`: 5 entries or fewer including opt-out, postbacks reuse ice breaker payloads, links have tracking parameters.
- [ ] `settings` `get_optout`: on, keywords reviewed for false positives, confirmation message set.
- [ ] `agent` `get`: mode, folder rule, human takeover and pause, request-human and cannot-reply scenarios as planned (SKILL.md section 7).
- [ ] The handover list is the same in the agent's rules, the knowledge base and the Human handover email.

**Text:**
- [ ] Every customer-facing message is short, in the client's voice, and states nothing the client didn't confirm (prices, codes, policies, hours).
- [ ] No message promises something later that no flow will do ("message me when you want the link" with nothing behind it).

## 2. Testing without touching real contacts

- **AI intents:** open each AI-detected trigger in the app and use **Test intent detection** with 5 to 10 real phrasings, taken from the client's inbox (`contacts` `list_messages`), including near misses that belong to a neighbouring flow. Fix the intent's "Not" list until the near misses fail. There is no connector tool for this test.
- **The steps of a flow:** in the editor, **Test scenario** gives a test code. Send that code as a DM from your agency's own test Instagram account, or pick your test account as the contact. `scenarios_manage` `test` does the same through the connector, for one contact. These really send messages, so only ever use your own test account. Test runs skip triggers, run limits and excluded folders, and are kept out of metrics.
- **Routing (priority, exclusions, team hold):** test runs don't prove routing. With the scenarios switched on, send real DMs from your test account to the client's account: one per intent, one that matches two intents, and one after a manual reply from the client's inbox. Put your test account in the "Internal test" folder first.
- **AI agent answers:** the AI Agent page has a test chat. Reset it between questions so earlier answers don't carry over. Details: `instagram-ai-agent-setup`.

## 3. Go-live order

Get the user's OK for go-live, then switch on one at a time with `scenarios_manage` `update` `{id, active: true}`, reading each back:

1. Human handover and the window timers (they only run when called).
2. Team hold: timer, then Team hold: start, only after every replying flow excludes Team hold (24h).
3. The replying flows in Inbound DMs, highest priority first.
4. Silent helpers (likes on kind messages and story mentions).
5. Agent mode last, if it changes.

If a comment-triggered flow is switched on, the app offers a one-time option to run it on matching comments from the last 7 days. That messages real people: only use it when the client asked for it.

## 4. The first day

Check a few hours after go-live, and again the next day:

- `executions` `health` for the account: run totals, failure rate, and account-level blockers (a broken Instagram connection or a plan limit stops everything at once).
- `scenarios` `performance` on each new flow: how many runs reached each step and why the rest stopped.
- `executions` `list` with `reason_code` to read the stops. Expected ones: `manual_reply` (the team stepped in), `contact_in_excluded_folder` (an exclusion did its job), `conversation_handled_by_human` (an AI step met a team takeover), `dm_held_private_reply` (a comment DM waiting for the person to reply). Unexpected ones (`action_error`, `instagram_disconnected`, `plan_limit_reached`) need a fix.
- Team hold: on the first real double message from the team, the earlier timer run shows as interrupted and a new one is pending.
- Read a handful of real conversations end to end with `contacts` `list_messages`. Look for a wrong flow, a wrong answer, an automation talking over the team, and dead ends.

## 5. An independent review (recommended)

The person who built it grades their own work generously. Before go-live, ask someone else, or a second read-only agent session, to check the account against the plan:

- Scope: read-only. The exact connector and client to use. No writes of any kind.
- The intended state as numbered checks: folder order, exclusions, triggers, menu, ice breakers, agent settings, helper flows, texts.
- A flow walk: every branch's ending, rule breaks in message text, ways two flows could both answer one message, leftovers from testing.
- Report: pass or fail per check with evidence, then findings ranked high, medium, low, with the situation where each one bites and a suggested fix (not applied).
