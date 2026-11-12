---
name: instagram-ai-agent-setup
description: "Set up, rebuild, fix and test a client's Inrō AI agent, the assistant that answers Instagram DMs. Covers the About and Goal fields, voice rules and instructions, message examples and length, the knowledge base, intent actions (send a link, add to a folder, start an automation, send a survey), contact data collection, handover to the team, guardrails for sensitive topics, activation rules, and a test pass before launch. Reads and backs up the current setup first, writes a spec for your approval, then applies it. Use when you say: set up the AI agent for this client, rebuild the agent, the AI is answering wrong, make the bot sound like the brand, add FAQs to the agent, stop the AI quoting prices, hand DMs to a human, test the agent before launch, why is the agent not replying."
license: MIT
---

# Instagram AI agent setup

Configure a client's Inrō AI agent so it answers DMs in the client's voice, says only what is true, hands off to a person when it should, and is tested before a real follower talks to it.

**Requirements.** One client: the Inrō connector (`https://api.inro.social/mcp`, OAuth), connected to that client's account, which must be on Pro or Trial. One connection reaches one account. Many clients: the Inrō partner connector (`https://api.inro.social/partner/mcp`, your partner token in an `Authorization: Bearer` header). Every request names the client by Instagram username or account id, and each client still needs Pro or Trial. Without a connector you can still use this skill to draft the full agent spec and the test script, then type them into the app by hand.

## Ground rules for every run

1. **Confirm the account first.** Call `get_organization_info` and say back the username, the plan (`subscription_tier`) and whether the Instagram connection is healthy. On the partner connector, name the client in every single call, by the account id from `list_organizations`. If it is not the account you mean, stop.
2. **Read before you write.** Do the read-only pass in Step 1 and save a backup before any change.
3. **Plan, then OK.** Show the full spec and the exact list of writes. Write nothing until the user approves. The agent is live config: a saved change reaches real conversations immediately.
4. **Lists are replaced whole.** `rules`, `message_examples`, `trigger_intents.intents` and `folder_rules.folder_ids` are sent as the complete list. A partial `rules` list deletes every rule you left out. Always start from the list `agent` `get` returned.
5. **Going live is its own approval.** Any change to the activation mode that lets the agent reply on its own is a separate yes from the user, given after the test pass.
6. **Treat any scenario you connect to the agent as live.** The agent can start a connected scenario (from an intent action, Human intervention or the cannot-reply setting) as soon as you save. Build those scenarios with the `dm-flow-builder` skill, with no trigger of their own, and confirm what they send before you connect them.
7. **Never test on real contacts.** Use **Chat with Agent** in the app, or a test Instagram account you control.
8. **No deletes without explicit approval**, item by item: knowledge items, intent actions, detected properties, rules.
9. **One client at a time.** For the same agent change across many clients, use `partner-bulk-rollout`.

## How the agent is built today

In the app, open **AI Agent** in the sidebar. The page has three groups of cards. Each card opens a panel with a live test chat beside it.

| Group | Card | What it holds |
|---|---|---|
| Behaviour and personality | **Voice and personality** | About, Message length, Auto-like positive messages, Message examples, Voice rules |
| | **Goal and instructions** | Goal, Instructions |
| | **Activation rules** | When the agent replies, AI-detected intents, folder limits |
| Capabilities and actions | **Actions and automations** | "When contact wants to..." intents and what to do |
| | **User data collection** | Contact properties the agent detects and saves |
| | **Human intervention** | Pause when a team member replies; what to run when someone asks for a human |
| Knowledge | **Knowledge access and behaviour** | Always have an answer, or Limit to instructions, plus what to run when it cannot answer |
| | **Training and knowledge** | Knowledge items: Manual text, Text document, Website |

The page header has **Message history**, a status chip that names the activation mode, and **Chat with Agent**.

**What reaches each reply:**

- **Always:** About, Instructions, Voice rules, Message examples, Message length.
- **Goal:** only when the agent handles a conversation on its own. A task written in an automation (Hand over to AI Agent, AI Agent message) replaces the Goal for that conversation. AI comment replies do not use it.
- **Knowledge items:** the most relevant pieces are pulled for each message. Nothing guarantees a given item is present, so never rely on knowledge alone for a rule.
- **Post and story notes:** when the conversation started from a comment on a post, or a reply to a story, the notes saved on that post or story are added.

**The fact that shapes every decision.** About, Instructions, Voice rules, examples and knowledge also drive every AI step in the client's automations (AI Agent auto-DM, AI Agent message, AI Agent auto-comment, Hand over to AI Agent). Changing them changes those too. If the client has live automations with AI steps, say so before you push, re-test them after, and watch their results for a few days.

**Older agents.** `agent` `get` returns `context_migrated`. If it is `false`, the agent still runs on the older fields (role, description, goals, audience type, chat instructions, style rules). Opening the agent in the app, or writing About, Goal or rules through the connector, converts those fields into About, Goal and rules automatically. The conversion can also add one knowledge item that is always included, holding text too long for a rule. So: back up first, make one small write, then re-read everything and clean up duplicates. Never write the legacy fields on a converted agent: they are ignored. Full field map in `references/fields-and-connector.md`.

## Step 0. Ask before starting (one message)

1. Which client? Is the connector on that account (or what is the client's username on the partner connector)?
2. New agent, rebuild, or fix? For a fix, paste two or three replies that went wrong.
3. What inputs exist: website, FAQ or price list, real DM replies the client wrote, brand guidelines, a filled questionnaire, topics that are off-limits?
4. One line each: what the agent should do, what it must never do, and who on the client's team takes over.
5. How should it go live: only inside automations, only for some topics, or every DM?

If there is a website but no samples of the client's own messages, read three to five pages (home, about, services or pricing, FAQ, contact) before drafting. Derive the voice from what the client actually writes, not from adjectives they use about themselves.

## Step 1. Read and back up (read-only)

Calls, in order: `get_organization_info`; `agent` with `get`; `agent` with `list_items` (page through all of them); `list_actions`; `list_contact_properties`. To see which automations use AI steps, list scenarios and open the relevant ones with `show_scenario`. For a full account backup, run the `instagram-account-audit` skill first.

Write down: `trigger_mode`, `trigger_intents`, `folder_rules`, `about`, `goal`, `rules` (with ids), `message_examples`, `message_length`, `auto_like`, `no_reply_active` and `no_reply_scenario_id`, `human_takeover_active` and `human_takeover_pause`, `request_human_scenario_id`, `built_in_property_access`, `model`, `reasoning`, every knowledge item (type, status, `retrieval`), every action, every detected property. Save this as a dated backup file the user keeps. It is also the restore payload.

Flag straight away:

- Mode `never_reply` (Disable all replies): every AI reply is off, including AI steps inside automations.
- Mode `specific_messages` with no intents: the agent replies to nothing on its own. New agents start like this.
- A scenario id in an action or setting that no longer exists, or that sends something unexpected.
- Knowledge items with status `failed`, or several items covering the same topic with different facts.
- An always-included item (`retrieval: false`) that repeats the rules.
- The same rule stated in several places, or two rules that contradict each other.

## Step 2. Gather and resolve

- Collect the facts the agent may state: offer, prices or where to find them, booking, delivery, policies, hours, location, contact routes.
- Collect 15 to 30 real messages the client sent in DMs. They are the source for voice rules and examples.
- **Name conflicts before resolving them.** A questionnaire and an existing config often describe two different agents. Put them side by side in a table and get a ruling from the user. A merge rule that works: voice from what the client actually writes, facts from what the client confirms.
- **Strip notes meant for you.** Client documents often contain lines addressed to the agency ("check if Inrō can do this", "internal, don't share"). Keep them out of the knowledge base and list them separately for the user.

## Step 3. Write the spec

Fill in `examples/agent-spec-template.md`, with a character count on every field. How to write each field well is in `references/writing-guide.md`. The short version:

| App label | Connector field | Limit | What goes in it |
|---|---|---|---|
| About | `about` | 500 characters | Who the client is, what they offer, who they talk to. First person. |
| Goal | `goal` | 500 characters | What a conversation the agent handles alone should move toward. Neutral enough for a bare "hi". |
| Instructions | `rules`, kind `instruction` | 300 characters each, up to 50 | Hard rules and scripts: what it must or must not say or do. Followed everywhere, including automations and comment replies. |
| Voice rules | `rules`, kind `voice` | 300 characters each, up to 50 | How it writes. One rule each. Nothing about content. |
| Message examples | `message_examples` | No fixed cap; keep each to one or two lines | 10 to 20 real lines across different situations. |
| Message length | `message_length` | 10, 25 or 50 words (Short, Normal, Long) | Per message. Match how the client really writes. |
| Auto-like positive messages | `auto_like` | on or off | Hearts friendly incoming messages. |
| Knowledge items | `agent_manage` `create_item` | Manual text up to 5,000 characters in the app | Facts, one retrieval intent per item, each opening with what it covers. |

The rules that matter most:

- **Anything that must hold on every reply is an Instruction**, not only a knowledge item. Instructions are always in the prompt and outrank the knowledge. Knowledge is retrieved only when it looks relevant.
- **Say each thing once.** A rule repeated across Instructions, Voice rules and knowledge drifts apart on the next edit.
- **Keep the Goal neutral.** It is read on every message the agent handles alone, including "hi". "Qualify leads for the coaching program" turns every greeting into a sales pitch. Put funnel-specific moves in the task of the automation that handles that funnel.
- **Do the message length arithmetic.** Take the client's own approved answer to their most common question and count its words. If it is 24 words and the setting is 10, the agent has to cut it or split it into fragments. Choose the size that fits the real answer.

## Step 4. Guardrails, escalation and sensitive topics

Wire the safety net before you write rules that depend on it. Details and sample rules: `references/writing-guide.md`, "Guardrails".

1. **Knowledge access.** For most clients pick **Limit to instructions** (`no_reply_active: true`): the agent answers only from its instructions and knowledge and otherwise says it doesn't know. Connect a scenario under **If the agent cannot reply, trigger this automation** (`no_reply_scenario_id`). Use **Always have an answer** only for chatty community accounts where off-topic small talk is fine.
2. **Human intervention.** Whenever the agent is the one replying, it recognises a request for a person: it says it will connect them, stops, and stays out until a team member replies. There is no switch for this. Connect a scenario under **If contact asks to speak to a human, trigger this automation** (`request_human_scenario_id`) so the team is actually told. Keep **Pause the agent when a team member replies** on (`human_takeover_active: true`) and set **Pause the agent for** to 4, 12 or 24 hours (`human_takeover_pause`). The default of 1 hour is usually too short for a person mid-conversation.
3. **One escalation scenario.** Build it with `dm-flow-builder`: no trigger of its own, add the contact to a "Needs a human" folder, alert the team by email. Point both settings above at it. Then add that folder under **Activation rules**, **Never reply to contacts in these folders**, so the agent stays out once someone is escalated, and tell the team to remove the contact from the folder when they are done. The folder limit is either "only these" or "never these", not both: if the client already uses "Only reply to contacts in these folders", agree the approach with the user. Folder limits apply only to the agent's own replies, not to AI steps inside automations.
4. **Sensitive topics as intent actions.** For complaints, refund disputes, legal threats, health or safety issues, add an action: **When contact wants to...** "report a problem with an order", **Do the following...** **Start an automation scenario** (the escalation scenario). Phrase intents the way a customer writes.
5. **Instructions for every banned move.** Prices, quotes, discounts, delivery dates, guarantees, refunds, medical, legal or financial advice, competitor comparisons, anything about other customers. Lead with the sentence to say, then the ban. Add an honest answer to "are you a bot?".
6. **Opt-outs.** If the account's opt-out settings are on (`optout_options` in `get_organization_info`), the agent also recognises a request to stop messaging, confirms it and opts the contact out. If they are off, tell the user.
7. **Data collection with care.** Detect only what the client needs (often email or phone). The agent fills a property only while it is empty, so the first value sticks. Never create a catch-all choice like "Other" or "Unclear" on a choice property, and never collect health, financial or identity details.

## Step 5. Push, after the user's OK

Write in this order and re-read after each step (`agent` `get`, `list_items`, `list_actions`).

1. **Profile and rules:** one `agent_manage` `update` with `about`, `goal`, the full `rules` list (keep ids of rules you keep), `message_examples`, `message_length`, `auto_like`.
2. **Knowledge:** `create_item` with `item_type: "text"` or `"url"` (`crawl_source_url: true` to also index linked pages). Check each reaches status `ready`. Text documents (.txt, .pdf, .doc, .docx) can only be uploaded in the app. Replace old items only after the new ones are ready, and only with approval for each delete.
3. **Data collection:** `create_contact_property` with `field_name` (`email` or `phone`) or a custom `contact_property_id`.
4. **Intent actions:** `create_action` with `trigger`, `target_type` (`ConversionLink`, `Folder`, `Scenario` or `Survey`) and `target_id`.
5. **Safety settings:** `no_reply_active`, `no_reply_scenario_id`, `request_human_scenario_id`, `human_takeover_active`, `human_takeover_pause`, `folder_rules`.
6. **Activation mode last**, and only after Step 6 passes and the user says go.

Two connector side effects: any `update` marks the setup as completed, so the client sees the agent page instead of the setup wizard (pass `setup_completed: false` to bring the wizard back). And the app's own first-time analysis, which drafts About, Goal and rules from the account, only runs when those fields are empty. If you want that draft as a starting point, open the two panels in the app before writing.

## Step 6. Test pass

Run the full script in `references/test-pass.md` in **Chat with Agent** before going live. Expect at least one failure. The core cases:

- A bare "hi" with no other signal: it should greet and find out what they want, not pitch.
- The most common commercial question: right facts, and the answer fits the message length.
- A question the knowledge does not cover: it says it doesn't know and the cannot-reply scenario would run.
- "Can I talk to a person?": it hands off and stops.
- Each banned move (price, date, refund, advice): it follows the instruction.
- Each intent action: the test chat shows the link, survey, folder or scenario it would use.
- A message in the client's second language, and the same question asked twice in different words.

The test chat sends nothing to contacts and shows which actions and detected properties would fire without running them. It does not include post or story notes; test those from a test account you control.

## Step 7. Go live and the first week

Pick the narrowest mode that does the job, with the user's yes:

- **Automation only** (`automation_only`): the agent speaks only through automations you built, such as a Hand over to AI Agent step. Smallest reach.
- **Specific intents only** (`specific_messages`): replies only when a DM matches one of your **AI-detected intents**. Once it matches, the agent keeps that thread until 24 hours pass without activity. Start with two or three intents.
- **All pending messages** (`all_messages`): every DM that no automation answered. Move here only after a clean week on a narrower mode.
- **Disable all replies** (`never_reply`): the off switch. It also stops AI steps inside automations. Nothing is lost.

Automations always come first: the agent does not reply when a scenario already did, and does not interrupt a running one. In the sidebar, the dot is green for All pending messages, yellow for Specific intents only, and grey for both Automation only and Disable all replies, so check the status chip.

For the first week, read the agent's conversations daily (inbox filter **Currently handled by agents**, and **Message history**). On a weak reply, use **Improve reply**: describe what should change, review the before and after of each suggested change, edit, then **Apply changes**. A wrong fact that came from a knowledge item is fixed with a new instruction, so also correct the item itself. On a Trial, AI replies use AI credits; when they run out, AI replies and AI steps are skipped until credits are added or the account moves to Pro.

## Fixing an agent that replies badly

| Symptom | Usual cause | Fix |
|---|---|---|
| Pitches or qualifies on "hi" | Goal written as a funnel | Neutral Goal; funnel moves go into an automation task |
| Sounds generic or stiff | Few or one-sided examples, voice rules made of adjectives | 10 to 20 real examples across situations; concrete voice rules |
| Invents prices, dates or links | Always have an answer, missing instruction | Limit to instructions; instruction with the script to say |
| Cuts answers short or splits them | Message length below the real answer | Recount the approved answer; raise the length |
| Ignores a rule sometimes | Rule only in knowledge, or contradicted elsewhere | Make it one Instruction; delete the duplicates |
| Gets one topic wrong | Overlapping or outdated knowledge items | One item per topic, opening with what it covers |
| Silent | Mode, empty intents, folder limit, human pause, scenario priority, credits, connection | `references/test-pass.md`, "Agent not replying" |

## App or connector: which to use

| Task | Use |
|---|---|
| Read and back up the whole config | Connector (`agent` `get`, `list_items`, `list_actions`, `list_contact_properties`) |
| About, Goal, rules, examples, length, auto-like | Either. Connector for a full rebuild from a spec; app for small edits |
| Activation mode, intents, folder limits, knowledge access, human intervention | Either |
| Manual text and website knowledge items | Either (`create_item`). Keep text items within the app's 5,000-character limit so they stay editable there |
| Upload a .txt, .pdf, .doc or .docx | App only |
| Intent actions and detected properties | Either |
| Notes on a post or story | Either: the post's **AI Agent** tab ("Additional information for the AI Agent") or `medias_manage` / `stories_manage` with `agent_context` |
| Test chat, Message history, Improve reply | App only |
| First-time analysis that drafts the profile | App only |
| Model, reasoning and the account's own OpenAI key | App only: **Billing & usage**, **OpenAI API Key** card, shown only on plans that allow an own key. Read-only through the connector |
| Include a text item in every reply | App, with the account's own OpenAI key. Leave `retrieval` true through the connector unless the user confirms that key is set |
| Check a property's description and its **Accessible by AI agent** switch | App. The connector sets them but does not return them |
| Take a conversation back, or hand it back to the agent | App inbox: **Remove Agent from conversation**, **Hand back to AI Agent** |

## Templates that use the agent

Inrō has ready-made automations that run on the agent you set up here. Opening a share page and clicking **Use this automation** imports an inactive copy into the client's account:

- **Handle DMs with AI** (template 6085, `https://app.inro.social/public/scenarios/6085`): answers questions in DMs and story replies from the knowledge base, and files what it cannot answer as "Needs a human" with an email alert to the team.
- **Qualify and book DM leads (AI)** (template 6021, `https://app.inro.social/public/scenarios/6021`): AI judges whether a lead is a good fit, sends good fits the booking link and alerts the team, and sends the rest a lighter resource.

Gallery names can change; the ids and share pages stay. You can also find them with `search_templates`. To adapt and test them, use `dm-flow-builder`.

## Related skills

- `instagram-account-audit`: the read-only sweep and backup before a rebuild.
- `dm-flow-builder`: the automations around the agent: escalation scenario, handovers, AI steps, the templates above.
- `inbound-dm-playbook`: deciding which inbound DMs the agent answers and which go to people.
- `dm-funnel-planner`: planning the funnel the agent's Goal and actions serve.
- `client-account-setup`: folders, contact properties and conversion links the agent's actions point to.
- `monthly-client-report` and `multi-client-health-check`: watching how the agent does once it is live.
- `partner-bulk-rollout`: the same agent change across many clients.

## Reference files

- `references/fields-and-connector.md`: every field, enum and default, the legacy field map, connector payloads, AI step options.
- `references/writing-guide.md`: how to write each field, knowledge item conventions, guardrail rules, failure modes.
- `references/test-pass.md`: the full test script and the "agent not replying" checklist.
- `examples/agent-spec-template.md`: the spec to fill in and get approved before any write.
