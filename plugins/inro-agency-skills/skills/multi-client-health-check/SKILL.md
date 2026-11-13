---
name: multi-client-health-check
description: "Weekly health check across every Instagram client your agency runs on Inrō. Reads each account through the Inrō partner connector, or one connector per client, and writes one short list ranked by urgency: Instagram disconnected or restricted, plan or activation limits hit, automations failing, switched off or gone quiet, runs paused and waiting, AI agent switched off, failed campaign sends and posts, and sudden drops against last week. Read-only, never changes an account. Use when you ask for the weekly check, the Monday check, 'are any of my clients broken', 'what needs fixing this week', 'check all my accounts', a client health report, or a quick check before client calls. Works from a small client roster file you keep."
license: MIT
---

# Multi-client health check

Find what is broken on your clients' accounts before your clients do, once a week, on one page you can read in two minutes.

## Requirements

- **Many clients (the natural fit):** the Inrō partner connector at `https://api.inro.social/partner/mcp`, with your partner token in an `Authorization: Bearer` header (token from the partner dashboard at app.inro.social/partners, **API & MCP**). One connector covers every client account in your partner workspace. Every call names the client in the `organization` field; there is no default client.
- **Or one connector per client:** the Inrō connector at `https://api.inro.social/mcp` (OAuth), added once per client account. One account per connection. Your Claude app allows one connector per URL, so give each one a unique dummy query string, for example `https://api.inro.social/mcp?client=acme`. The query string changes nothing else.
- **Each client account must be on Pro (monthly or annual), a free trial, or a lifetime plan.** Free accounts, and accounts whose plan lapsed after a failed payment, are refused. Accounts billed through your partner plan are covered by it. A refused client is refused on its own while the others keep working, and that refusal is itself a finding. Judge by the refusal, not by `subscription_tier`: the tier can lag the real plan, and a brand-new partner account can read `free` and work normally.
- **A roster file** listing the clients you expect to see. Template: `references/roster-template.md`. Without one, the check still runs on every account it can reach, and says that it could not tell whether anyone is missing.

Tool names below are the ones the connector exposes. Your Claude app may show them with a prefix (the connector's name). Use whatever your connection lists.

Read tools used: `list_organizations` (partner connector only), `get_organization_info`, `executions`, `scenarios`, `campaigns`, `batch_tasks`, `agent`, `medias`, `icebreakers`.

## Safety rules (always)

1. **This check only reads.** It never edits, activates, deactivates, retries, resends, sends, tests or deletes anything. It reports. Fixes happen afterwards, one client at a time, with your OK (section 6).
2. **On the partner connector, name the client on every call,** reads included, using the account **id** from `list_organizations`. A username can match more than one account, and then the call is refused rather than guessed.
3. **With one connector per client,** call `get_organization_info` on each connector first and match it to a roster line by username. Never assume a connector's name tells you which account it reaches.
4. **A missing client is the loudest finding.** A clean report that quietly covered fewer clients than the roster is worse than no report. Reconcile before writing anything.
5. **No contact data in the report.** Counts, automation titles and links only. No contact names, handles or message text.

## 1. Set up the run

1. **Find the roster.** Default: `clients.md` in the folder the agency works from. If there is none, offer to create one from the template, filled from `list_organizations` (partner connector) or from the connected accounts.
2. **Find last week's check.** Default folder: `health-checks/`. The most recent file's snapshot block (section 5) gives the comparisons. If there is none, say this is the first run, flag only what needs no history, and note that comparisons start next week.
3. **Pick the window.** The last 7 days up to now, unless the agency asks for another range (up to 90 days back). Say at the top whether it was a scheduled or an on-demand run.

## 2. Reconcile the roster with what you can reach

**Partner connector:** call `list_organizations`. It returns every account in your partner workspace with `id`, `name`, `username`, `instagram_connected`, `subscription_tier` and `created_at`.

**One connector per client:** list every Inrō connector in the session and call `get_organization_info` on each.

Then compare with the roster:

- **On the roster, not reachable:** a top finding. Partner connector: the account is not in your workspace, or its calls are refused (plan, suspension). Per-client connectors: the connector is missing, broken or connected to a different account.
- **Reachable, not on the roster:** a new client nobody added. Include it in the run and say the roster needs a line for it.
- **`instagram_connected: false` with no `username`:** the account was created but Instagram was never linked. A finding only if the roster says the client should be live.

If a connector you expect seems absent at the start of a session, search for its tools once more before calling it unreachable. Connectors sometimes register late.

## 3. Read each client

Per client, in this order. About 6 to 10 calls each. Exact fields and conditions: `references/checks.md`.

1. **`get_organization_info`.** Connection (`login_error_data`, `instagram_restrictions`, `instagram_linked_at`), publishing (`can_publish`, `missing_publish_scopes`), plan (`subscription_tier`, `current_billing_period_end`, `max_contact_activations`).
2. **`executions` → `health`,** `since` 7 days ago. Run counts by status, `failure_rate`, the automations failing most (`top_failing`), the most common reasons (`top_reason_codes`), and account blockers (`account.instagram_connected`, `account.contact_activation_limit_reached`, activations used against the limit). This one call answers most of the check.
3. **`scenarios` → `list`,** paginate to the end. Per automation: `active`, `suspended`, `last_executed_at`, `paused_executions`, `metrics`, `full_url`.
4. **`scenarios` → `performance`** on each automation in `top_failing` (and `campaigns` → `performance` for a campaign there). It names the step where runs break and why.
5. **`campaigns` → `list`,** `per_page: 10`. `status`, `sent_at`, `metrics.failed`, `metrics.running`, `full_url`.
6. **`batch_tasks` → `list`,** `per_page: 10`. `status` and `error_message`. Empty is normal.
7. **`agent` → `get`.** `trigger_mode` and `setup_completed`. Compare with what the roster says the agent should do.
8. **Only where the roster says so:** `medias` → `list` with `status: "scheduled"` for clients whose posts you schedule, and `icebreakers` → `list` for clients that use ice breakers.

Do not pull contacts, messages or post insights. They are not part of a health check.

## 4. Rank the findings

One list across all clients, ranked by urgency, not grouped by client. Within a level, an account-wide problem comes before a single automation, and a busy account before a quiet one. Full conditions: `references/checks.md`.

**Fix today** (the account, or part of it, is cut off):
- Client on the roster but not reachable, or its calls refused.
- Instagram disconnected, or an error flagged on the connection. An account that never connected (`username: null`) is "not connected": a finding only if the client should be live.
- Meta blocking all DMs or DMs with links on the account.
- Activation limit reached: automations stop messaging new people.
- An automation suspended by the platform.
- Runs paused by a disconnection or the activation limit, waiting to be re-run once the cause is fixed.

**This week** (something is failing or silent):
- An automation failing a meaningful share of its runs, with the failing step named.
- An active automation that never ran, or stopped running, when it used to.
- Failed campaign sends, a campaign stuck in `limited`, or a failed batch task.
- AI agent switched off (`never_reply`, or "Specific intents only" with no intents) when the roster says it should answer, or AI steps showing an "AI features disabled" warning.
- Publishing permission missing, or a scheduled post that failed, for clients whose posts you publish.
- An ice breaker that starts nothing when tapped.
- A trial ending, or activation usage near a real cap, within the week (on Pro the activation limit is a price bracket, not a cap).

**Keep an eye on** (needs last week to see):
- Runs down by half or more against last week with no known reason.
- An automation that was converting last week and converted nothing this week.
- Meta rate limiting (usually minutes), or many DMs held by Instagram's own rules.

**Never report as a problem:** reach, likes or follower movement; zero conversions on flows with no link or survey (a flow that asks a question or tags a folder shows zero conversions forever); runs that ended for normal reasons, such as the contact replied, a person on your team took over, or the contact is in an excluded folder.

## 5. Write the report

Save to `health-checks/<YYYY-MM-DD>-health-check.md`, or wherever the agency says. In a chat app without a folder, give it as a download and remind them to attach it next week. Format with a filled example: `examples/health-check-example.md`.

Four parts, in this order, nothing else:

1. **Headline.** Week covered, clients checked out of clients on the roster, how many need action today. One plain sentence with the single most important thing.
2. **The ranked list.** Fix today, This week, Keep an eye on. One numbered item per issue.
3. **All clients at a glance.** One row per client: connection, automations switched on, runs this week, failure rate, paused runs, plan and renewal.
4. **Snapshot for next week.** A fenced JSON block with the raw figures per client. Next week's run reads it.

Rules for each item in the list:

- **Start with the client and the problem in one bold clause.** "@client_handle: Instagram disconnected since 3 Nov."
- **Say what the thing does in plain words,** so a reader who has forgotten this client's setup still follows: "the flow that DMs the price list to people who comment PRICE", not just its title.
- **Link every automation and campaign** with its `full_url`.
- **Say what the numbers show and the next step.** "41 of 60 runs failed at step 3, the link card, mostly `action_error`. Open the failed runs in the scenario's History tab before changing anything."
- **One item per issue.** A problem shared by two clients gets an item each, and each says the other is affected too, since it is probably one fix. Several silent automations on one client are one item: list up to five with links, then "and N more".
- **Plain language, not field names,** except a reason code in backticks when it helps the person who opens the account.
- A client with nothing to report appears only in the at-a-glance table. A good-news line is allowed at the end, only when something really improved.

## 6. After the check: fixes

This skill does not fix anything inside the run. When the agency picks an item to fix, that is a separate, approved change on one client:

- **Instagram disconnected:** the client (or whoever owns the Instagram login) reconnects in Inrō. Partner accounts show a **Reconnect** button on the partner dashboard card. Once reconnected, the paused runs need re-running: in the app, a dashboard card lists scenarios with paused runs, each with **Run paused executions** and a window (**Last 24 hours**, **Last 7 days**, **All history**). Runs outside the chosen window are cancelled.
- **Failed runs:** fix the cause first, then in the scenario's Insights view use **Retry all failed** from the menu next to a step's Failed count, or retry single runs from the History tab. Through the connector, `executions_manage` → `retry` re-runs one run (or one step with `step_id`); confirm the client, the run and the cause with the agency before each one.
- **Campaign sends paused:** `campaigns_manage` → `resend` with `scope` `disconnected` or `limited` previews first and sends nothing until called again with `confirm`. Show the preview and get a yes.
- **A flow that is wrong:** `dm-flow-builder`. **The AI agent:** `instagram-ai-agent-setup`. **A deeper look at one account:** `instagram-account-audit`.

The platform logs in the app (account menu, the account name bottom left, then **Platform logs**) show each run, each API and connector call, and the errors Instagram returned. They keep only a few days, so look soon after the check.

## 7. Data traps

Details in `references/checks.md`. The ones that cause wrong reports:

- **`metrics.executions.last_7_days` on a scenario is a cached counter,** refreshed when the automation runs or is opened in the app. On a flow that has gone quiet it keeps an old number and can disagree with `last_executed_at`. For week numbers, use `executions` → `health` and `performance`, which compute the window when asked. Use `last_executed_at` to decide whether a flow ran.
- **`metrics` comes in three shapes on automations:** `{}` on one that never ran, partial with only `total`, or complete. Campaign drafts return `metrics: null`. Handle all of them.
- **Paused is not failed.** `limited`, `disconnected` and `restricted` runs are held, not lost. `failure_rate` counts only `failed` and `partially_completed`.
- **The window is rolling:** 7 days back from the moment of the call, not Monday to Sunday. Say the dates in the headline.
- **Health and performance numbers are cached for about a minute.** A number read just after a retry may predate it.

## 8. What this costs

About 6 to 10 calls per client, plus one `list_organizations` on the partner connector. Ten clients take a few minutes. It is read-only, so it is safe to schedule, for example every Monday morning, with a person reading the result.

## 9. Related skills

- `monthly-client-report` for the client-facing monthly document. Run this check first so a broken connection is explained in the report, not discovered by the client.
- `partner-client-onboarding` for adding a new client, and `partner-bulk-rollout` for one change across many clients.
- `dm-flow-builder`, `instagram-ai-agent-setup` and `instagram-account-audit` for fixes, as above.

Help center references: [Partner API & MCP](https://help.inro.social/en/articles/17027623), [The Partner Dashboard](https://help.inro.social/en/articles/17027622), [Platform logs](https://help.inro.social/en/articles/17027626), [Retry failed executions](https://help.inro.social/en/articles/14895231), [Scenario metrics](https://help.inro.social/en/articles/15632147), [When Instagram disconnects an account](https://help.inro.social/en/articles/14956396).
