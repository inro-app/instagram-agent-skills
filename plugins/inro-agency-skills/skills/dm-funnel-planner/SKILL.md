---
name: dm-funnel-planner
description: Plan which Instagram DM automations to build for a client, and in what order, from what the account actually gets. Reads recent posts and reels with their comment volume, story replies, inbound DMs, existing Inrō automations and how they perform, plus the client's offer and goal. Proposes three quick wins and a fuller funnel, each tied to real traffic, with the trigger, what the DM sends or asks, where it leads and how to measure it, mapped to an Inrō template where one fits. Read-only. The output is a short plan an agency can show its client. Use when someone asks what automations a client needs, where to start with DM automation, for an automation plan or funnel plan, quick wins for an Instagram account, which template to use, or why a client's DMs are not turning into leads.
license: MIT
---

# DM funnel planner

Decide what DM automation to build for one client, and in what order, from the traffic the account already gets. The result is a one or two page plan the agency can put in front of the client. Building it is a separate step (`dm-flow-builder`).

**Requirements.** The Inrō connector (`https://api.inro.social/mcp`, sign in with OAuth), connected to the client's account. The account must be on Pro or Trial, and one connection reaches one account. If you manage many clients, use the Inrō partner connector instead (`https://api.inro.social/partner/mcp`, your partner token in an `Authorization: Bearer` header). On the partner connector every request names the client by Instagram username or account id, and each client still needs Pro or Trial. Without a connector you can still draft a plan from what the client tells you and from their public profile, but mark every number as unverified and keep the plan provisional.

## Ground rules

- **This skill only reads.** It never creates, edits, activates, sends or deletes anything. If the person asks you to build part of the plan, switch to `dm-flow-builder`, which has its own approval steps.
- **Confirm the account first** (section 1). A plan built on the wrong account is worse than no plan.
- **One client at a time.** On the partner connector, name the client in every call, and never carry a number from one client into another client's plan.
- **No recommendation without traffic behind it.** Each item in the plan points at a number from this account: comments, story replies, DMs, contacts, ad arrivals. If you cannot point at one, it is not a quick win.
- **Keep the client's audience private.** The plan talks about counts and patterns. It never names or quotes an individual contact.

## 1. Confirm the account

Call `get_organization_info` (on the partner connector, pass the client's account id from `list_organizations`). Say back to the person:

- the Instagram username and account name,
- the plan (`subscription_tier`): Pro or Trial is needed for the connector to work at all,
- whether Instagram is connected (`login_error_data.login_error`). If it is broken, every automation is stopped and nothing you plan will run until the client reconnects. That becomes the first item of the plan.
- whether opt-out is on (`optout_options.active`). If it is off, note it for the foundations.

Ask the person to confirm this is the right client before you read anything else. If there is more than one Inrō connector in the session, check each one and agree which one is this client.

## 2. Ask what the client wants

Ask only what you cannot read from the account. Usually four things:

1. **The offer.** What do they sell or give away? A product, a booking, a course, a freebie, an event, a store visit.
2. **The goal for the next 30 to 90 days.** Leads (emails or phone numbers), bookings, sales, followers, sign-ups, fewer unanswered DMs.
3. **The destination.** The link, booking page, store, or file people should end up at. If there is no destination yet, a funnel cannot end anywhere; say so.
4. **Limits.** Topics to avoid, words the brand never uses, whether a person must answer certain questions, budget for AI credits.

If the client already filled an onboarding form or an earlier audit exists, read that instead of asking again.

## 3. Read the traffic

This is the core of the plan. Read the last 30 days by default, and the last 90 days for a small account. All calls are reads. The exact calls, parameters and the traps in each number are in `references/signals.md`; read it before you start.

| What you need | Where it comes from |
|---|---|
| Posts and reels, and how many comments each gets | `medias` list (published), each post's `insights.comments` and `like_count`, and whether it already has a `comment_to_dm` automation |
| How many people commented | `contacts` filter, `comment` in the window |
| How many people replied to stories | `contacts` filter, `story_reply` in the window |
| How many people sent a DM, and what they ask | `contacts` filter, `message` in the window; `message` with a `value` such as "price" to count a repeated question; `contacts` get or `list_messages` on a small sample to read the questions themselves |
| Story mentions, post mentions, ad arrivals | `contacts` filter, `story_mention`, `media_mention`, `referral_ad` |
| The list | `contacts` filter on `email` or `phone` present, `folder`, `is_follower` |
| What is already built | `scenarios` list, then `get` and `performance` on each active one |
| What is broken | `executions` health for the window |
| Entry points | `icebreakers` list, `persistent_menu` get, `campaigns` list, `conversion_links` list |
| The AI agent | `agent` get, only to see whether it is on and what it covers |

Write each number down with its source and window. You will quote them in the plan.

Two checks before you trust a number:

- **Read a sample of the comments** on the busiest posts (in Instagram or the Inrō inbox). A wave of spam, a giveaway, or friends congratulating the client is volume, not demand.
- **Posting stories is not the same as getting story replies.** Count the people who replied, never the stories posted.

## 4. Read what is already running

Before proposing anything new, list what exists:

- Every active scenario, its trigger in plain words, and its results over the window (`scenarios` performance gives runs reaching and finishing each step).
- Inactive scenarios that had real volume before. A flow that worked and was switched off is often the cheapest win on the account.
- Ice breakers or menu entries with nothing behind them (`icebreakers` list shows an empty `automations` array when a tap starts nothing).
- Failure clusters from `executions` health. A broken connection or an exhausted contact limit stops every automation at once, and no new flow fixes that.
- Two flows that could fire on the same comment or DM. That is a fix, not a new build.

A zero in Inrō means Inrō has no record, not that the client never does it. Another tool, or a person replying from the Instagram app, can be doing the work. If you see fast replies or repeated reply wording that Inrō did not send, the play changes from "build this" to "move this where you can measure and follow it up".

## 5. Choose the plays

Work down this ranking and stop at three quick wins. The full list of plays, the condition each one needs, and the matching templates are in `references/plays.md`.

1. **Something the client already owns that is off, broken or unused.** A working flow switched off, a dead ice breaker, a disconnected account, a conversion link nothing sends.
2. **Volume arriving now that nothing catches.** Posts with comments and no comment flow. Story replies with no flow. DMs with the same question and no answer.
3. **A capture gap on traffic that already converts.** A link flow that captures nothing (no email, no folder), so the client cannot reach these people again.
4. **A new flow on existing traffic.** A second keyword, follow-gating, a story flow next to a comment flow.
5. **Anything that needs new content, ads or a new audience first.** Never a quick win. It can sit in the fuller funnel, marked as needing that content.

For each candidate, check its condition in `references/plays.md`. If the condition is not true on this account, drop it, however good it sounds.

Three is the right number. An account with eight new flows in week one cannot tell which one works.

## 6. Design each item

For every quick win, and briefly for each fuller-funnel row, write:

- **Traffic behind it.** The number, the window, the source. "212 people commented on the last 8 reels in 30 days; none of those reels has a comment flow."
- **Trigger.** In plain words, and the Inrō trigger it maps to ("comments with the word GUIDE on posts whose caption contains GUIDE").
- **What the DM sends or asks.** The first message, the step that needs a tap or reply, and what comes after.
- **Where it leads.** The link, booking, file, folder, or a person.
- **How to measure it.** Runs, link clicks, emails collected, folder size, bookings, read on the scenario's results or with a contacts filter. Name the number you will report, and when.
- **Template.** The closest template from `references/templates.md`, or "custom build" if none fits. Check the live gallery with `search_templates` (type `Scenario` or `Campaign`) before naming one; the gallery changes.

Design defaults that hold on Instagram:

- **After a comment, Instagram allows one DM until the person replies or taps.** So the first DM asks for a tap or a reply (a button, a question, a follow request, an email request), and the link comes after. This also keeps the link out of the first message, where plain links may get blocked.
- **Send links as a link card** (conversion link), not as a raw URL in the text. Clicks are tracked and delivery is more reliable.
- **One clear button beats several.** One clear keyword per post beats a list.
- **Reply to the comment publicly as well**, so the post keeps moving and the person knows to check their DMs.
- **Keep the first message short and send it straight away.** Most people act soon after they comment, while they are still in the app. Save the waiting for the follow-up.
- **One follow-up, then stop.** Instagram only lets you message people who wrote to you in the last 24 hours, so a follow-up days later mostly never arrives. Put it a few hours after the link.
- **Pick a keyword that never appears by accident.** Keywords match whole words, ignoring case and accents, and a 4+ letter keyword also matches its plural. "Guide" is fine; "yes", "love" or the product's own name are not.

## 7. Write the plan

Keep it to one or two pages. Use the shape in `examples/example-plan.md`:

1. **Where the account is today.** Three to five lines, each with a number. Lead with what is working, then the gaps.
2. **Three quick wins, in order.** One block each, with the fields from section 6. Say "first, then, then", not dates, unless the account is connected and the destination exists.
3. **The fuller funnel.** Ten to fifteen one-line rows in three groups:
   - *Foundations*: ice breakers, persistent menu, opt-out, folders for each stage, an org-wide exclusion for existing customers or the team, run-once rules.
   - *Automations and campaigns*: the flows that carry volume (comment, story, DM keyword, lives, ads, QR), the follow-ups, and campaigns for people still inside the 24-hour window.
   - *AI agent*: what it would answer, what it would collect, and when it hands over to a person. Point to `instagram-ai-agent-setup` for the setup itself. Only put the agent in the quick wins if the account shows repeated questions and has something to train it on (a website, a price list, an FAQ).
4. **Not now, and why.** One line per idea you dropped, with the missing condition ("story replies: 4 in 30 days").
5. **What we need from you.** Links, the freebie file, the booking page, the offer wording, approval of the copy.
6. **How we will measure.** The two or three numbers you will report after two and four weeks.

## 8. Writing rules

- **Never invent a number.** Every figure has a source and a window. If a figure is not available (insights still refreshing, no data for the period), say so.
- **No promised outcomes.** Do not write "this will double your leads". Write what the traffic is and what the flow does with it.
- **Scope every zero.** "No flow in Inrō answers story replies today", not "nobody answers your story replies".
- **The client's language, not the tool's.** "People who opened your booking page", not "conversion link clicks on action 3".
- **One claim per line**, with its number.
- **Plain words, short sentences.** The client should be able to read the plan without a call.

## 9. Hand off

- To build the plan: `dm-flow-builder`, item by item, starting with quick win 1. Pass it the plan as written.
- To set up or tune the AI agent: `instagram-ai-agent-setup`.
- For a full read-only audit before planning on a busy account: `instagram-account-audit`.
- To report on the plan's numbers each month: `monthly-client-report`.
- For how a person should handle the DMs the funnel creates: `inbound-dm-playbook`.
- For the posts and captions that feed the funnel (a comment keyword in the caption, a story with a reply prompt): `client-post-scheduler` and `short-form-content-principles`.
- To roll the same funnel out to many clients: `partner-bulk-rollout`.
