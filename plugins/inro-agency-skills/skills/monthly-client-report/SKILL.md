---
name: monthly-client-report
description: "Writes the monthly performance report an agency sends to an Instagram client that runs on Inrō. Pulls the month's numbers through the Inrō connector (automation runs and their funnels, link clicks and conversions, new and engaged contacts, campaigns, posts, AI steps), compares them with last month's saved snapshot, asks you what shipped, then writes a client-ready PDF or document under your agency's brand, with every number scoped to what it counts and every zero explained. Read-only on the client's account. Use when you ask for a monthly report, a client update, a performance recap, a month-end summary, 'how did @client do in October', numbers for a client call, or a progress report that shows the retainer is working."
license: MIT
---

# Monthly client report

You turn one client's month into a short document the client will actually read: what happened, what you shipped, what worked, what you test next. One client per run.

## Requirements

- **One client:** the Inrō connector at `https://api.inro.social/mcp` (OAuth), connected to that client's account. One Instagram account per connection, on Pro (monthly or annual), a free trial, or a lifetime plan. Free accounts, and accounts whose plan lapsed after a failed payment, are refused.
- **Many clients:** the Inrō partner connector at `https://api.inro.social/partner/mcp`, with your partner token in an `Authorization: Bearer` header. Every call names the client in the `organization` field (account id or Instagram username). There is no default client. Each client account still needs one of those plans; accounts billed through your partner plan are covered by it.
- **For the final file:** whatever document or PDF tool your Claude environment has. Without one, you get the report as Markdown or HTML to drop into your own template.
- **Without a connector:** there is nothing to count. You can still paste numbers in and get the report laid out, and every figure is labelled as supplied by you.

Tool names below are the ones the connector exposes. Your Claude app may show them with a prefix (the connector's name). Use whatever your connection lists.

Read tools used: `get_organization_info`, `get_contact_filter_types`, `contacts`, `executions`, `scenarios`, `campaigns`, `conversion_links`, `medias`, `stories`, `agent`; on the partner connector also `list_organizations`.

## Safety rules (always)

1. **This skill only reads the client's account.** It never creates, edits, sends, tests, triggers, retries or deletes anything in Inrō. If the numbers point at something to fix, say so and hand it to the right skill (section 9) with the agency deciding.
2. **Confirm the account before counting anything.** Call `get_organization_info` and say back the Instagram username, account name and `subscription_tier` (a hint only: it can lag the real plan). If it is not the client the agency named, stop.
3. **Single-account connectors:** if more than one Inrō connector is installed, call `get_organization_info` on each, say which one is which, and use only the one the agency confirms. Never mix connectors in one report.
4. **Partner connector:** call `list_organizations` first, pick the client, and use its **id** in `organization` on every call, reads included. A username can match more than one account, and then the call is refused rather than guessed.
5. **One client per report.** Never put two clients' numbers in one document.
6. **Nothing private leaves the account.** The report and the snapshot hold counts, titles and dates. No contact names, handles, emails, phone numbers or message text.

## 1. Ask before starting

Keep it to one message:

1. Which client? (And which connector, if there are several.)
2. Which month? Default: the calendar month that just ended.
3. Where do the report and the snapshot go? Default: a local folder `client-reports/<client_handle>/`. Is last month's snapshot there, or can they attach it?
4. Brand, first run only: agency name, logo file, one or two brand colours, who signs the report, how the client's name should be written, and the language of the report. Save the answers to `client-reports/brand.json` so next month does not ask again.
5. The client's time zone, if it is not obvious. Month boundaries follow it.

Then pull the numbers. Do not ask what to highlight yet: that conversation happens in step 4, once there is something to show.

## 2. Pull the numbers

Exact calls, parameters and the wording each number gets in the report: `references/metrics.md`. The short version:

**Set the window.** `since` is the first day of the month at 00:00 and `until` is the first day of the next month at 00:00, in the client's time zone, as ISO 8601. Contact filters work by day: the first and last day of the month, `is_between` (both days included).

**Automation runs, for the month.** `executions` → `health` with `since`/`until`. It returns run counts by status, the failure rate and the automations failing most. Do the same for the previous month so the comparison does not depend on a snapshot. Run history is kept for the last 90 days, so run the report within a few weeks of month end.

**Each automation's funnel.** `scenarios` → `list` (every page) for titles, `active`, `created_at`, `last_executed_at` and `full_url`. Then `scenarios` → `performance` with the same window, for each automation that ran in the month. Each step carries `reached`, and engagement counters `sent`, `read`, `clicked`, `replied`, `converted`. Campaigns work the same way: `campaigns` → `list`, then `campaigns` → `performance` for the ones sent in the month.

**Contacts.** Call `get_contact_filter_types` first; the filter shapes come from there, not from memory. Count with `contacts` → `filter`, `per_page: 1`, and read `pagination.total_count`. One filter per count, so each number means one thing: new contacts (`first_interaction`), engaged contacts (`any_engagement`), link clickers (`clicked_conversion_link` per `conversion_link_id` for the two or three main destinations; the overall count can be refused on larger accounts), people who went through an automation (`scenario`) or received a campaign (`campaign`). Total audience is `contacts` → `list` with `per_page: 1`. Contact counts stop at 10,000: when `pagination.total_count_capped` is `true`, the figure is a floor, so write "more than 10,000" and never subtract it from anything.

**Data captured.** Emails, phone numbers and custom properties stored on contacts are totals to date (`email` / `phone` with `is_present`, `contact_property`). The month's change only exists by comparing with last month's snapshot. Say which one you are showing.

**Posts and stories.** `medias` → `list`, `status: "published"`, newest first, until `posted_at` falls before the month. Entries with no `posted_at` can come first: skip them. `insights` is filled only when `insights_status` is `fresh`. On `refreshing`, wait a minute and read again; on `unavailable`, Instagram does not report on that post, so leave it out of the totals and say how many were left out. `stories` → `list` for stories. It has no date filter and is not in date order, so filter by `posted_at` yourself. Story insights are often empty, so tell the agency rather than dropping the section silently.

**What shipped, from the account itself.** Anything with `created_at` inside the month is a candidate for "what we shipped": automations, campaigns, conversion links, AI agent knowledge items and AI agent actions. Folders and contact properties carry no creation date in the connector, so ask about those.

**Three numbers the connector cannot give for a calendar month.** Handle them as `references/metrics.md` says, never by estimating:

- **Activated contacts** (the billing number). `executions` → `health` returns `account.contact_activations_used`, but for the current billing period so far, not a calendar month. For the calendar month, the agency reads **Activated contacts** on the client's Inrō Dashboard with the month as the date range. Partners also see usage by account on the partner dashboard's Billing page, for the billing period.
- **Conversations the AI agent answered on its own.** Not counted by the connector. In the app: AI Agent page, **Message history**. What the connector can count: AI steps inside automations (their `sent` in `performance`) and automation runs the agent started (`executions` → `list`, `execution_type: "agent"`).
- **Followers.** The connector returns no follower count, and the partner dashboard shows today's count only. Ask the agency for the month's numbers or leave it out. Never put a blank row in a client document.

## 3. Compare

**With last month's snapshot:** put this month beside last month for every figure, and subtract the totals to date (audience, emails, phones, properties) to get the month's change.

**Without one:** recompute last month live for everything that takes a date range (runs, funnels, contact filters). Totals to date cannot be backdated, so label them "to date" and say comparisons start next month. A first report is weaker than a second one; say so to the agency rather than implying growth you cannot show.

**Always save this month's snapshot,** first run included. Format: `examples/snapshot-example.json`.

## 4. Talk to the agency, after the analysis

Come back with what you found, then ask. Something close to:

> Here is what October looks like for @client. [Three or four findings, including anything odd.] What did you ship or change on this account in October, and was anything discussed with the client that I should know about?

Check what they say against the data. Each answer lands in a different part of the report:

- **It shipped and a number moved:** a win, with the number attached.
- **It shipped and nothing moved yet:** a line in "what we are testing next", framed honestly.
- **It was discussed and never shipped:** next month's plan, not this month's report.

Also mention anything you found that they did not: a new automation with a `created_at` in the month, a funnel step where most people stopped, a campaign that failed sends.

## 5. What the report says

Two to three pages. Account level, not a table of every post. A busy client wants "you posted 14 times, those posts had a combined reach of 12,400, and 340 people ended up in a conversation", not a row per post. Skeleton with placeholders: `examples/report-outline.md`.

1. **Header.** Client, month, the agency's name and logo, one line on what happened.
2. **The month in numbers.** Six to eight figures, each with last month beside it and a one-line label saying what it counts.
3. **Two or three charts, no more.** For example new contacts this month against last, top automations by runs and clicks, clicks by destination.
4. **What we shipped.** New automations, AI agent improvements, new data being captured. This is what shows the retainer working in a month where the numbers are flat.
5. **What worked.** Two or three wins, each with a number.
6. **What we are testing next.** Two or three, each tied to something in the data.

Optional: one highlight post if it clearly outperformed, with its permalink and what the automation on it did.

**The document is the agency's.** Their logo, colours and sign-off. Name Inrō only where the client needs to know where something lives ("your automations in Inrō"). No Inrō logo unless the agency asks for one.

## 6. Writing rules

Full rules with examples: `references/writing-rules.md`. The ones that matter most:

- **Every number is scoped:** what it counts and which period. "1,240 people clicked a link in a DM in October", not "1,240 conversions".
- **Never invent or estimate a number.** If it is not in a tool response or supplied by the agency, it is not in the document. A number supplied by the agency is labelled as theirs.
- **Scope every zero to what Inrō can see.** "No campaign was sent from Inrō in October", never "you sent no campaigns". The client may run other tools Inrō cannot see.
- **Inrō measures up to the click.** A conversion is a click on a tracked link, a survey answer, or a payment or booking made through Inrō's own Stripe or Calendly steps. What happens on the client's website after the click is invisible to Inrō. Write "people who clicked through to your booking page", never "bookings", unless the booking went through the Calendly step.
- **No outcome promises and no platform benchmarks.** Compare the client with its own last month.
- **Explain a drop instead of hiding it.** "Reach fell because 6 posts went out instead of 14" is a normal sentence.
- **Their language, not the tool's.** "Conversations your AI assistant handled", not "agent_reply executions". "People who clicked through to your shop", not "conversion link 1234".
- **Findings, not process.** State what was measured and what it showed. Never narrate who looked or how.

## 7. Files

- **Report:** `<folder>/<YYYY-MM>-report.pdf` (or `.docx` or `.md` if that is what the agency's tools produce).
- **Snapshot:** `<folder>/<YYYY-MM>-snapshot.json`. Every raw figure counted, the window and time zone used, the date you counted, and automation ids with titles, so next month subtracts instead of guessing.
- **Read last month's snapshot** from the same folder at the start of the run.
- **In a chat app without a persistent folder:** hand both files over as downloads and remind the agency to attach the snapshot next month.
- The agency decides where the files live. Nothing is uploaded anywhere unless they ask.

## 8. What this costs

Around 30 to 60 small tool calls for one client, most of them counts with `per_page: 1`. The `medias` list is the heaviest response (about 270,000 characters per 100 posts): page it at 20 to 30, or have a helper extract the month's posts. Budget ten to fifteen minutes. Run it on request, with a person reading the result before it goes to a client.

## 9. Related skills

- `multi-client-health-check` for the weekly look at what is broken across every client. Run it before the report so a broken connection is explained, not discovered by the client.
- `instagram-account-audit` for a deeper one-off read of an account.
- `dm-flow-builder` when the report shows a flow to fix or a step where people drop.
- `instagram-ai-agent-setup` when the AI agent is answering badly or not at all.
- `dm-funnel-planner` to turn "what we are testing next" into a plan.
- `client-post-scheduler` for the posts behind next month's numbers.

Help center references: [Scenario metrics](https://help.inro.social/en/articles/15632147), [The Inrō dashboard](https://help.inro.social/en/articles/10807843), [What are activated contacts?](https://help.inro.social/en/articles/9423792), [Partner API & MCP](https://help.inro.social/en/articles/17027623).
