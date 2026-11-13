---
name: inbound-dm-playbook
description: "The standard way to handle inbound Instagram DMs on a client account in Inrō. Sorts and prioritises what comes in (collab pitches, complaints and refunds, bookings, buyers, price questions, general questions, first messages, kind messages, spam), sets the default automations (welcome, keyword and FAQ replies, price answers, bookings, handover to a person, one reminder when someone goes quiet, closures), the exclusions and run limits that stop automations talking over the team, and how to adapt it for coaches, shops, local businesses and service firms. Maps each piece to a ready Inrō template you can import switched off. Use when you say: which DM automations should this client have, set up DM replies, route inbound DMs, answer price questions in DMs, catch collab requests, FAQ buttons, handle DMs with AI, our flows clash, two replies to one message."
license: MIT
---

# Inbound DM playbook

What every client account should do with the DMs that come in, in which order, and which Inrō template to start each piece from. This file is the design. Template details: `references/templates.md`. Ready-to-paste AI intents: `references/intent-library.md`. Per business type: `references/business-types.md`.

**Requirements.** One client: the Inrō connector (`https://api.inro.social/mcp`, OAuth), one Instagram account per connection, on Pro (monthly or annual), a free trial, or a lifetime plan (free accounts are refused). Many clients: the Inrō partner connector (`https://api.inro.social/partner/mcp`, partner token in an `Authorization: Bearer` header); name the client in the `organization` field of every call, and each client still needs one of those plans. AI-detected triggers and AI steps also need AI features and AI credits on the account. Without a connector you can still design the plan with this skill and import templates from their share pages in the app.

## Safety rules

1. Confirm the account with `get_organization_info` before anything, and say back the username and tier. On the partner connector, name the client in every call, by the account id from `list_organizations`.
2. Read what is live first (`scenarios` `list`, `scenario_folders` `list`, `agent` `get`, `icebreakers` `list`). Never add a flow that duplicates one already running.
3. Show the plan, with exact message text, and get the user's OK before any write.
4. Everything you add starts switched off. Template copies arrive inactive; keep them that way until go-live is approved.
5. Never test on real contacts. Test runs really send messages: use your agency's own test account.
6. Never delete without explicit approval. One client at a time unless the user asked for a bulk change.

## How this fits with other skills

- `client-account-setup` owns the baseline this playbook sits on: the folder names, the Inbound DMs and Helpers scenario folders, the team hold, the Human handover scenario, agent guardrails, and the exclusions. Do that first, or check it exists.
- `dm-flow-builder` builds or edits one flow step by step. This skill says which flows and in which order; hand each build to it.
- `instagram-ai-agent-setup` writes the agent's knowledge, voice and rules. The AI front desk below answers from them.
- `dm-funnel-planner` designs comment, story and ad funnels that end in a DM. This skill covers what happens when people write to the client.

## 1. How Inrō decides who answers (the facts this design rests on)

- **Scenarios first, then the agent.** A scenario that matches answers; the AI agent only fills gaps, and stays quiet while a scenario is running for that person.
- **A priority scenario folder gives one answer per message.** Only its top matching scenario runs. Scenarios whose excluded folders match the person, or that are over their run limit, are skipped first, so the next one down answers. While one scenario in the folder is running for a person, no other one in that folder starts for them.
- **A normal folder, or no folder, runs every match.** Two matching scenarios there means two replies. This is the usual cause of "two replies to one message".
- **A scenario already running for a person doesn't start again for them.** The new trigger is dropped without a trace.
- **Several messages in a row are one turn.** The person gets one reply to the burst.
- **Instagram's 24-hour window.** You can reply within 24 hours of the person's last message, so a reminder goes out around 20 hours, not 24.
- **Comments open one DM.** When a flow starts from a comment, the person gets one DM until they reply.

So: every scenario that **replies** goes in one priority folder, **Inbound DMs**. Silent helpers (likes, timers, the team hold) go in a normal folder, **Helpers**, so they never block a reply.

## 2. The inbound map, in priority order

Most specific and highest stakes first; the catch-alls last. Numbers are positions in the Inbound DMs folder.

| # | What came in | What should happen | Start from | Run limit |
|---|---|---|---|---|
| 1 | A brand, creator or agency pitching a collab | File it, alert the client, one short holding reply. Never agree fees, codes or deals | 36429 Catch collab requests in DMs | 7 days |
| 2 | A complaint, refund, cancellation, or a problem with an order or booking | A person handles it. Holding reply, Needs a human, alert, Complaint window (7d) | Build (pattern in section 3.2) | 1 day |
| 3 | Wants to book, or asks about availability | Booking link, one reminder if not opened | 36437 Get bookings from DMs, or 6021 Qualify and book DM leads (AI) | 1 hour to 1 day |
| 4 | Ready to buy: "where can I buy this?", "is it in stock?" | Shop or product link, one gentle reminder | 36432 Shop link to ready buyers (AI) | 1 day |
| 5 | Asks about prices, plans or packages | The price, or the options with a link each. No price on file: a person | 36433 Help people choose a product (menu or ice breaker); DM version built from 36436 | 1 day; none on the menu version |
| 6 | Any other question about products, services, hours or orders | AI answers from the client's information; what it can't answer goes to the team | 6085 Handle DMs with AI | 1 day |
| 7 | A first message nothing above caught ("hi", an emoji) | Greet, ask what they need with two to four options, route | Build (section 3.7) | once |

Entry points that feed this list, not extra rows: **ice breakers** and **persistent menu** (36428 FAQ buttons in your DMs, or an ice breaker trigger on the flow that already answers that topic), **story replies** (add a story-reply trigger with the same AI intent to the flow that answers it), and **click-to-message ads** (`dm-funnel-planner`).

In **Helpers** (silent, every match runs): Team hold: start and timer, window timers, Human handover (`client-account-setup`), 6223 Auto-like positive messages, 6086 Like stories that mention you.

Handled by settings, not flows: **opt-out** ("unsubscribe", the menu entry), **spam** (Move to spam in the inbox), **asks for a person** while the agent is talking (the agent's Request a human, wired to Human handover).

## 3. The default automations, one by one

Each one: what it does, what to set after import, and the trap to avoid. Exact steps and folders each template creates: `references/templates.md`.

**3.1 Collab requests (36429).** AI spots pitches, files them in "Collabs: requested", emails the client, waits 5 seconds and sends a short holding reply. After import: the alert address, the holding reply in the client's voice. Add the Collab window (7d) helper (`client-account-setup`, baseline B4) so price, booking and AI flows stay off the partner's follow-ups for a week. Never exclude "Collabs: requested" itself anywhere: it is permanent.

**3.2 Complaints, refunds, order problems (build).** Trigger: Someone sends you a DM, AI-detected intent (text in `references/intent-library.md`), same intent on story replies. Steps: add Needs a human and Complaint window (7d), start the window timer, alert email with `{{contact.username}}` and `{{trigger.message}}`, wait 5 seconds, holding reply ("Thanks for telling us. Someone from the team will reply here today."). For shops whose orders live in another store, a short "where did you order?" question with buttons before the alert saves the team a step. Never promise a refund, a timeline or an outcome.

**3.3 Bookings (36437 or 6021).** 36437 sends the booking link on a keyword (default RESERVE) and one reminder. Switch its trigger to an AI-detected intent if people don't use a keyword, and add an ice breaker or menu trigger for "Book". 6021 asks what they need, lets AI judge fit, sends hot leads the booking link with an alert, and the rest a free resource: right for coaches and high-ticket services. After import: the client's booking URL in the link step, the alert address, the fit description.

**3.4 Ready to buy (36432).** AI spots buying intent and sends the shop or product link with one reminder. After import: the link, the intent tuned to the client's products. Exclude Complaint window (7d), so someone mid-complaint doesn't get a shop link.

**3.5 Prices (36433, 36436).** 36433 is a profile question ("Which one is right for me?") with up to three options, each sending its own link. Good when the client has two or three plans or packages. 36436 answers "PRICE" *comments* with a DM; for price questions *in DMs*, make a copy without its public comment-reply step and give it a DM trigger with the price intent. Only state prices the client confirmed. No price on file means the flow ends with a person, not a guess.

**3.6 AI front desk (6085).** Hands any question to the AI agent with a narrow task: answer from the knowledge base in one or two short messages; done only when they have their answer or link. Completed: "Front desk: resolved". Expired after 24 hours: Needs a human and an alert with the first and latest message. It sits low on purpose, because its intent is wide. It only works as well as the agent's knowledge (`instagram-ai-agent-setup`), and the agent must not be set to **Disable all replies**.

**3.7 Welcome, first message only (build).** Trigger: Someone sends you a DM, **First message only**, any content. Lowest position, so a first message with a clear intent goes to that flow instead. Steps: a one-line greeting and **Ask a question** with two to four options matching the flows above ("Prices", "Book", "Something else"). Each option sends its link or hands to the AI with a task; "Something else" and any free-text reply go to the AI front desk task or a person. No reminder on the welcome.

**3.8 Kind messages and story mentions (6223, 6086).** Likes, no text. Put them in Helpers and exclude Human only and Team hold (24h). Check how the client's team reacts to mentions today before adding any message.

**3.9 FAQ buttons (36428).** Up to three ice breakers answered in one scenario: each tap is checked with a condition on the tapped text (`{{trigger.message}}` contains "pricing", "availability") and gets its answer; "Can I talk to a person?" alerts the team. After import the template's ice breakers don't exist on the client's profile: create the client's ice breakers, point each trigger at its payload, and **change the condition values to words in the client's own questions**, or the taps fall through. When a topic needs a full flow (bookings, a plan picker), give that flow the ice breaker trigger instead.

## 4. Follow-ups, dead ends and closures

- **No dead ends.** Every branch ends in a reply, an AI handover, or an alert to the team. Expiry branches count: an AI handover that expires sends an alert, a question nobody answered ends cleanly.
- **One reminder, then stop.** The templates use one: "Have you checked the link yet?" on the link's expired branch, after about 2 hours. A question waits up to about 20 hours. Never chain reminders.
- **Never promise what no flow does.** "Message me when you want the link" needs a flow that catches it. Under **Automation only** nothing else will. Send the link now instead: "No rush, here's the link for whenever you're ready."
- **Going quiet after a team reply is fine.** The team hold keeps automations out; don't build a follow-up on top of the team's own conversation.
- **Closures and holidays.** Inbox settings → **Time-off** sends an auto-reply to the first message anyone sends until the last day you pick. There is no opening-hours schedule for flows. For "outside hours", let the AI front desk answer and make every handover message honest about when a person replies ("The team replies Monday to Friday, usually the same day").
- **Re-engaging people who went cold** is a campaign, not an inbound flow. Leave it out of this playbook.

## 5. Writing the AI intents

The shape the templates use, and the one that tests best: one sentence of what fires, in plain words, then "Not ..." naming the neighbouring flows.

```
Wants to buy, or asks where to buy, if it is in stock or how to order, in their own words.
Not a button reply, a complaint, a return or a collab pitch.
```

- Write it the way the client's customers write, not as a category ("asks how much it costs", not "pricing inquiry").
- "Not a button reply" stops a flow from firing on ice breaker and menu taps that another flow answers.
- Use the same intent text on the DM trigger and the story-reply trigger of a flow.
- **Test before switching on.** Open the trigger in the app and use **Test intent detection** with 5 to 10 real messages from the client's inbox (`contacts` `list_messages`), including near misses from the neighbouring flows. Each near miss should fail. There is no connector tool for this test.
- Ready-made texts for every row of the map: `references/intent-library.md`.

## 6. Exclusions, run limits and interrupts for these flows

How to set them, and why each rule exists: `client-account-setup` (section 8 and baseline B12). Folder exclusions: `scenarios_manage` `update` with `excluded_folder_ids`, or **Exclude specific folders** in the app (section 8, step 5).

| Flow | Excluded folders | Run limit | Interrupt when you reply manually |
|---|---|---|---|
| Every flow in Inbound DMs | Human only, Team hold (24h) | as in the map | On |
| Bookings, buying, prices, AI front desk, welcome | also Collab window (7d), Complaint window (7d) | | |
| Collab requests, complaints | only Human only and Team hold (24h) | | |
| Flows reached only by an ice breaker or menu tap | | none: a limit makes a repeat tap get no answer from that flow | On |
| Likes on kind messages and story mentions (Helpers) | Human only, Team hold (24h) | 1 day | On |

"Interrupt when contact replies" stays off on all of them: it would end AI handovers, button and link waits the moment the person writes.

## 7. Adapt it to the business

Same map, different emphasis. Full versions with ice breakers, menu and sensitive topics: `references/business-types.md`.

| Business | Lead with | Usually skip | Watch out for |
|---|---|---|---|
| Coach or course creator | 6021 qualify and book; 36433 programmes | 36432 shop link | Health and results claims; refunds on programmes |
| Online shop | 36432 ready to buy; complaints and order problems high; 36436 for price comments | 6021 | Delivery promises, returns, discount codes |
| Local business (salon, clinic, studio, restaurant) | 36437 bookings; 36428 FAQ buttons for hours, prices, location | 6021 | Medical or allergy questions go to a person; Time-off for closures |
| Service firm or B2B | 6021 qualify, then a call; prices go to a call, not a number | 36432, 36436 | Quotes and contracts are always a person |
| Creator or personal brand | 36429 collabs at the top; 6223 and 6086 likes | Bookings | Keep close contacts in Human only |

## 8. Importing a template

1. Find it: `search_templates` (`type: "Scenario"`, a plain query like "collab requests"), or use the id from `references/templates.md`. The newest templates (ids 36428 to 36438) aren't in the template library yet, so `search_templates` doesn't return them: use the id. Preview it on its share page, `https://app.inro.social/public/scenarios/<id>`.
2. Import with the user's OK: `scenarios_manage` `create` with `template_id` and, optionally, the client-facing `title` (no triggers, actions or prompt in that call). This works for every id in `references/templates.md`, the newest ones included. In the app: the share page's **Use this automation** button, or **New scenario**, then **or choose a template** (the newest ones aren't listed there yet, so use their share page). Both import into the account you're logged in to, so check the organisation switcher first.
3. The copy arrives inactive, with its own copies of the template's links, and its folders matched by exact name (created when the client has none with that name).
4. Fix before anything else: every link URL, every alert email address (templates ship empty, which shows as an issue), ice breaker triggers (point at the client's payloads), keywords, the AI intent text, the message text in the client's voice, run limit and interrupts. When you change a step's options (an alert address), send the step's whole `options` from `get` with your change in it: options are replaced, not merged, so anything you leave out is wiped.
5. Place it: `scenarios_manage` `update` with `scenario_folder_id` (Inbound DMs or Helpers) and `scenario_folder_priority`, then `scenario_folders_manage` `reorder` for the whole folder. Then the excluded folders (section 6): `scenarios_manage` `update` with `id` and the full `excluded_folder_ids` list, in a call of its own (it is ignored on `create` and in an update that also sends triggers or actions). Or **Exclude specific folders** in the app.
6. Read back (`scenarios` `get`, `show_scenario`): no warnings with severity `issue`, still inactive, `excluded_folder_ids` exactly as intended. Read the folder order with `scenarios` `list` (`scenario_folder_id` as a string, `order_column: "scenario_folder_priority"`, `order_direction: "asc"`); `scenario_folders` `get` shows only the count. Go-live follows `client-account-setup` (QA and go-live).

## 9. One week after go-live

- `executions` `health`, then `scenarios` `performance` on each flow: which step loses people.
- Read 10 to 20 conversations. Sort every miss into: wrong flow (fix the intent's "Not" list or the order), right flow and wrong answer (fix the text or the knowledge base), automation over the team (check the team hold and exclusions), dead end (add the missing branch), two replies (a replying flow outside Inbound DMs).
- Lines the team still types by hand after a flow ran are the next flow to add.
