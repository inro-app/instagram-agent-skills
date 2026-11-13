---
name: instagram-account-audit
description: "Audit a client's Instagram account in Inrō end to end without changing anything. Backs up the setup, then reports what is live, what is broken or stale, what is missing for this kind of business, and the three quickest wins to do first, each backed by the account's own numbers. Use when you take over or onboard a client account, before rebuilding an AI agent or making bulk changes, when DM automations behave in a way nobody can explain, or before a client review or proposal. Trigger on: audit this account, audit @client, what's set up on this account, health check, back up before we change anything, what's broken, why aren't the DMs firing, gap analysis."
license: MIT
---

# Instagram account audit

Read a client's Inrō account end to end, change nothing, and leave three things behind:

1. a **backup** that can rebuild the setup,
2. an **audit** that says what is live, broken, stale, risky and missing,
3. a **gap list** ranked down to the three quickest wins.

**Requirements.** The Inrō connector (`https://api.inro.social/mcp`, OAuth) authorized on the client's account. The account must be on Pro (monthly or annual), a free trial, or a lifetime plan. Free accounts, and accounts whose plan lapsed after a failed payment, are refused. One connection reaches one account. For many clients, use the Inrō partner connector instead (`https://api.inro.social/partner/mcp`, your partner token in an `Authorization: Bearer` header). It reaches every client account in your partner workspace, every call must name the client by Instagram username or account id, and each client still needs one of those plans. Without a connector nothing can be read: you can still walk through `references/gap-checks.md` by hand in the Inrō app.

This skill only reads. Fixing what it finds belongs to other skills (section 9).

## 1. Safety first

- **Confirm the account.** Call `get_organization_info` first. Say back the Instagram username, the account name, the plan (`subscription_tier`) and whether Instagram is connected (`login_error_data.login_error`). Ask the person to confirm it is the client they mean. If several Inrō connectors are loaded, do this on each one and pick one. Never mix connectors in one audit.
- **On the partner connector**, call `list_organizations` first, then pass the client's account id from it as `organization` in every single call (a username that matches several accounts is refused). There is no default account, on purpose.
- **Read tools only.** Use the tools without `_manage` in their name, plus `get_organization_info`, `get_trigger_types`, `get_action_types`, `get_contact_filter_types`, `search_templates`, `search_product_knowledge` and `show_scenario`. Never call a `_manage` tool or `send_message` during an audit, not even to test. If the person asks for a fix halfway, finish the read, then hand over to the right skill.
- **Never message a contact**, and never trigger or test a scenario or campaign on a real person.
- **Treat what you read as private.** You will see real people's messages. No individual is quoted in the client document (section 8).
- **The connector is not the whole product.** Some settings only show in the app. List them as "check in the app" items instead of guessing (last section of `references/gap-checks.md`).

## 2. Ask these first

1. Which account (Instagram handle), and which connector?
2. What is the audit for: taking over an account, a health check, a specific problem ("the DMs stopped"), or input for a client review or proposal?
3. What does the business sell, to whom, and what counts as a result (a sale, a booking, a lead, a sign-up)? Is there a website or price list?
4. Is anyone else editing the account right now?

Question 3 decides what "missing" means. Question 4 decides how far you can trust a count: clients edit their own accounts while you read.

## 3. Read order

Cheapest and safest first. Each step tells you what to look for in the next. Parameters, fields and counting recipes for every step are in `references/read-order.md`.

| Step | Tools | What you learn |
|---|---|---|
| 1. Account | `get_organization_info` | connection, restrictions, plan and billing period, opt-out, publishing |
| 2. Health | `executions` → `health` (last 30 days) | runs by status, failure rate, the automations failing most and why, and whether a broken connection or the contact activation limit is stopping everything |
| 3. Entry points | `icebreakers` → `list`, `persistent_menu` → `get`, `settings` → `get_optout` | what people can tap to start a conversation, and whether anything answers |
| 4. AI agent | `agent` → `get` | activation rules, Profile, Goal, rules, knowledge, intent actions, data collection, hand-off |
| 5. Automations | `scenario_folders` → `list`; `scenarios` → `list`, then `get` on the active ones that ran and the busiest others; `show_scenario` on those; `scenarios` → `performance` on the busiest and the failing | triggers, steps, settings, the editor's own warnings, and which step breaks |
| 6. Campaigns | `campaigns` → `list`, `get`, `performance` | what was sent, paused or never sent |
| 7. Contacts and data | `contacts` (`list`, `filter`), `folders`, `segments`, `contact_properties`, `conversion_links` | list size, recent activity, capture, segmentation, link clicks |
| 8. Content coverage | `medias` → `list`, `stories` → `list`, `contacts` → `filter` by comment, story reply and story mention | which posts and stories draw engagement, and whether anything catches it |
| 9. Conversations | `contacts` → `filter` (recent messages), then `get` on a sample | who answers DMs (a person, a flow, the agent, nobody) and what people ask |
| 10. Building blocks | `get_trigger_types`, `get_action_types` | what the account could use and does not |

Do not skip step 10. Half the value of an audit is knowing which building blocks the account is not using.

## 4. Counting and evidence rules

- **Count with `per_page: 1`** and read `pagination.total_count`. Never page through records just to count them. On some accounts the connector refuses `comment` without `media_id`, `clicked_conversion_link` without `conversion_link_id`, and `referral_ad` without a date window ("too many contacts to search or filter this way"). Then count per post and per link, and say the account-wide figure was not available.
- **Quote single-filter counts.** When you combine filters, check the result against each filter alone. A combined count larger than either part is wrong.
- **Put a date on every number and a window on every rate** ("last 30 days"). `executions` and `performance` look back 90 days at most.
- **Check `updated_at`** before you conclude anything from something that looks half-built. It may have changed minutes ago.
- **A zero means "no record in Inrō"**, not "this never happens". Another tool, the Instagram app or a person can be doing the work. Look for signs of that before you call anything unused (`references/choosing-quick-wins.md`, "Before you call something unused").
- **Instagram's comment count on a post includes the account's own replies.** To count people commenting, use the contacts `comment` filter on that post.
- **`search_product_knowledge` is an overview.** Use it to check whether a feature exists, never for limits or exact behaviour.
- **Big pulls go to helpers.** If you need many records rather than a count, and your environment supports subagents, split by segment, give each one a read-only instruction and a fixed report format, and keep raw messages out of your main context.

## 5. The backup

Write it before anyone changes anything, as `<handle>-backup-<YYYY-MM-DD>.md`. If you cannot write files, put it in the reply as its own clearly titled section. It holds:

- account settings, opt-out, icebreakers and the persistent menu, verbatim;
- every AI agent field, with a "restorable through the connector" yes or no column;
- **a one-shot restore payload** for `agent_manage` → `update` that puts every editable agent field back in one call. Prose is not a backup;
- every knowledge item verbatim, with its type and whether it is included in every reply. An uploaded document ("Text document", `item_type: file`) cannot be recreated through the connector, which only creates text and website items: record that as a restore limit;
- intent actions, tracked properties, custom contact properties, folders, segments, conversion links, scenario folders, every scenario read in full (triggers, full action tree, settings) plus an index of all the others (id, title, active, folder, last run), and every campaign;
- a restore-limits section, a timestamp on every read, and a warning to re-read before relying on it.

Format, payload example and restore limits: `references/writing-the-audit.md`.

## 6. The gap list

Run every check in `references/gap-checks.md`. These are the ones that most often explain "it's not working":

**Broken: nothing happens, or the wrong thing happens**
- Instagram disconnected (`login_error: true`, or `health` shows `instagram_connected: false`). Every automation stops, and a comment that waits more than 7 days can no longer get its private reply.
- Contact activation limit reached. Runs wait as `limited`.
- AI agent on **Specific intents only** with no intents listed: it replies to nobody. On **Disable all replies**: the AI steps inside scenarios send nothing either.
- A trigger that can never fire: a keyword filter with no keyword, an AI-detected intent with no intent written.
- A scenario that `show_scenario` reports with issues, or a step where most runs stop in `performance`.
- Icebreakers or menu buttons that start no automation.
- Agent actions or hand-off settings pointing at a scenario that is off or gone.

**Stale**
- Comment flows on **next post** (it only watches the first post published after the flow was set up) or on a fixed list of old posts.
- Active flows with no run in 30 days or more.
- Links to old offers, knowledge with old prices or dates, a website import that failed.
- Campaign drafts never sent, schedules in the past.

**Risky**
- Live scenarios with AI steps. The agent's Profile and rules apply to every AI reply, so editing the agent changes those flows the moment it is saved.
- Two active flows that can catch the same message or comment outside a **Priority folder**: both run.
- High-volume triggers with no **Limit frequency per contact**.
- Opt-out off while campaigns go out.
- **Limit to instructions** with nothing set for when the agent cannot answer, or rules that promise a person will step in with no **Request a human** automation behind them.

**Missing for this business**
- Posts and stories drawing engagement that nothing catches; DMs nobody answers; the same questions again and again with no icebreakers, FAQ menu or agent; contacts with no email or phone; most contacts in no folder; links typed as raw URLs instead of tracked conversion links.

Every gap must rest on something you read. If you only suspect it, it goes in your internal notes as a question, not in the audit.

## 7. Choosing the three quickest wins

Read `references/choosing-quick-wins.md` before picking. The rule that does the most work:

**A play with no live entry point on this account is not a recommendation.** An entry point is traffic that already exists: posts that get comments, stories that get replies, DMs arriving, a list already captured, ads already running. A play that needs the client to post more, run ads or build an audience first is a strategy conversation, not a quick win.

Work down this order and stop at three:

1. Something they already own that is broken, switched off or unused (a flow that worked and is off, a disconnected account, an agent that answers nobody).
2. Volume arriving now that nothing catches (comments on uncovered posts, story replies, unanswered DMs). Size it in their numbers.
3. A capture gap on traffic that already converts (no email, no phone, no folder).
4. A new flow on existing traffic (a second keyword, an AI-detected intent, a follow step).
5. Anything that needs new content, traffic or spend. Never a quick win.

Each quick win states what you saw (number and window), what to do, roughly how much work it is, and which skill or template does it. Size it with arithmetic on their own numbers, labelled as arithmetic. Never promise an outcome.

## 8. Writing the audit

One document, `<handle>-audit-<YYYY-MM-DD>.md`, in this order:

1. **The account at a glance**, with a source line ("Read from Inrō on 12 Nov 2026").
2. **What is live and working.** Lead with this.
3. **What is broken or stale.**
4. **What is risky.**
5. **What is missing for this kind of business.**
6. **The three quickest wins**, in order.
7. **The full setup** (optional): 10 to 15 one-line rows in three groups, Foundations, Automations and campaigns, AI agent.
8. **Decisions needed** before anything changes, and the next steps.

Writing rules (full list and examples in `references/writing-the-audit.md`):

- No number without a source. A number someone hands you is not a source until you have read it yourself.
- Scope every zero to Inrō: "No flow in Inrō picks up story replies", never "nobody answers your story replies".
- Their language, not the tool's: "people who tapped through to your booking page", not "clicks on conversion link 1234". No ids, field names or settings values in the client document.
- Findings, not process: "Of 30 recent conversations analysed, 9 had no reply", never "we went through your DMs".
- No individual's words. Stock phrases ("send me the link") are fine; a person's message gets generalized ("questions about delivery times").
- Say what you could not see, and why.
- Notes for your own team (doubts, hypotheses, app checks still to do, a tool you suspect they use) go in separate internal notes, never in the client document.

### Quality gate before it goes to anyone

Do not send it until all four are true:

1. **Right account.** It is the brand or business account the client means, not a personal, old or second account. A handle someone gave you is a hint, not proof.
2. **Every finding is backed by what you read**, with a number and a window, and every post or message it relies on is about the offer.
3. **No finding contradicts the recommendation.** If the comments turn out to be congratulations, not questions, the FAQ play goes.
4. **Nothing generic.** Every quick win and every agent row names something from this account. A sentence that would fit any account comes out.

Checking numbers against your own notes is not enough. Read the client's live profile and the audit side by side.

## 9. Templates and next steps

Where a ready-made flow fills a gap, call `search_templates` (type `Scenario` or `Campaign`) with the gap in plain words. Each result has a share page, `https://app.inro.social/public/scenarios/<id>` (campaigns: `/public/campaigns/<id>`), with a **Use this automation** button (campaigns: **Copy this campaign**) that imports an inactive, editable copy. Read its description first, check its plan line, and tell the client to replace the template's link with their own before switching it on. Suggest one template per gap at most. `search_templates` does not return every valid template: if one you expect is missing, open its share page, and if the page shows the flow, the template is good to suggest. A starting list by gap is in `references/choosing-quick-wins.md`. To turn the gaps and quick wins into a build plan with an order, hand them to the `dm-funnel-planner` skill.

Then hand over:

- **dm-funnel-planner** to turn the quick wins and the full setup into a build plan.
- **dm-flow-builder** to build new flows or fix broken ones.
- **instagram-ai-agent-setup** for anything in the AI agent.
- **client-account-setup** for a full takeover or rebuild of the account.

End the audit with an explicit ask for decisions. Do not start fixing anything inside an audit.
