# Gap checks

Run every check. Report only the ones that are true, each with what you read, the number and the date. The tag says where it goes in the audit: **[Broken]**, **[Stale]**, **[Risky]** or **[Missing]**.

"Missing" is always relative to this business and its traffic. A building block the account does not use is only a gap if there is an entry point for it (see `choosing-quick-wins.md`).

## Account and connection

- **[Broken]** `login_error: true`, or `health` → `account.instagram_connected: false`. Every automation is stopped. Runs wait as `disconnected` (`paused_executions.disconnected` on each scenario) and can be re-run after reconnecting, except comments that waited past Instagram's 7-day window for a private reply.
- **[Broken]** `contact_activation_limit_reached: true`. Automations and campaigns pause as `limited` until the limit resets or the plan changes.
- **[Broken]** `instagram_restrictions` not empty, or `account_restricted` in the reason codes.
- **[Risky]** A trial or billing period ending soon (`current_billing_period_end`). Say what stops if the plan lapses rather than guessing; check the plan in the app.
- **[Missing]** `can_publish: false` with `missing_publish_scopes`, only if the client wants to publish from Inrō.

## Entry points

- **[Broken]** An icebreaker whose `automations` array is empty: tapping it starts no flow. The agent may still answer it if its activation rules let it, which is worth saying.
- **[Broken]** A persistent menu `postback` entry that no active scenario matches. Skip the opt-out entry (`source: optout`, payload `INRO_OPTOUT`): Inrō handles it.
- **[Missing]** No icebreakers on an account that receives DMs, when the same opening questions repeat in the sample.
- **[Risky]** Opt-out off (`optout_options.active: false`) on an account that sends campaigns. People cannot unsubscribe by keyword.
- **[Risky]** Opt-out on but `menu_message` blank (no opt-out entry in the menu) or `confirmation_message` blank (no confirmation sent). A choice, but say it.

## AI agent

Dead wiring:
- **[Broken]** `trigger_mode: specific_messages` with no intents in `trigger_intents.intents` (the field can also come back as `{}`). The agent replies to no message. The app warns about this ("No intents added") but lets it save.
- **[Broken]** `trigger_mode: never_reply` while active scenarios contain AI steps (`agent_reply`, `agent_message`, `agent_comment`, `agent_handover`). Those steps send nothing.
- **[Stale]** Intents listed under AI-detected intents while the mode is not Specific intents only. They do nothing.
- **[Broken]** An agent action, `no_reply_scenario_id` or `request_human_scenario_id` pointing at a scenario that is off or deleted, a folder or link that no longer exists.
- **[Broken]** Knowledge items with `status: failed` (usually a website that could not be read), or still `processing` long after they were added.
- **[Risky]** Rules that promise a person will step in ("a team member will get back to you") while `request_human_scenario_id` is empty: the agent pauses, and nobody is told.
- **[Risky]** `no_reply_active: true` (Limit to instructions) with no `no_reply_scenario_id`: when the agent has no answer it says it doesn't know, and nobody on the team hears about it.
- **[Risky]** `human_takeover_active: false`: the agent can keep answering on top of a team member. `human_takeover_pause: 1` is short for a person still mid-conversation.

Configuration:
- **[Missing]** Profile (`about`) or Goal empty, or no rules at all.
- **[Stale]** `context_migrated: false`: the agent still runs on the older fields. Nothing is broken, but the first person to open the AI Agent page triggers the move to Profile, Goal and rules. Back up first.
- **[Risky]** The same rule written in voice rules, instructions and a knowledge item at once, or two rules that contradict each other.
- **[Risky]** A Goal that is a style note or a guardrail rather than an outcome ("be friendly" instead of "book a consultation").
- **[Risky]** `message_length` shorter than the answers the client actually needs (10 words for questions that need 50).
- **[Risky]** Live scenarios with AI steps. The Profile and rules apply to every AI reply, so any agent edit changes those flows the moment it is saved. Name them.

Knowledge:
- **[Risky]** Long items with `retrieval: false` ("Include this information in all Agent requests"). They go into every reply, which slows replies and costs more. A leftover item that repeats the Goal or the rules adds nothing.
- **[Risky]** Notes written to the agency or the team ("ask the client about this") sitting in the knowledge, where the agent reads them as facts.
- **[Risky]** One huge item covering many topics, items that refer to each other ("see the pricing note"), or items whose first lines don't say what they cover.
- **[Stale]** Prices, dates, offers or opening hours that no longer match the client's website.

Data collection:
- **[Missing]** The goal is leads or bookings but neither email nor phone is tracked (`contact_properties` on the agent), or `built_in_property_access` is empty while the rules ask the agent to use the email.
- **[Broken]** A custom property the rules ask the agent to collect that is not tracked (not in the agent's `contact_properties` from `agent` → `get`).
- **[Risky]** Single or multiple choice properties with placeholder choices ("Option 1"), or two properties that would catch the same answer.

## Automations

Dead wiring:
- **[Broken]** `show_scenario` returns `has_issues: true`. Read the flow and say which step.
- **[Broken]** A comment trigger with `comment_keywords` and no keyword, or `ai_detected` with no `ai_intent`. A messages or story reply trigger with keywords as the filter and none written. Before calling any trigger dead, run `executions` → `list` with `scenario_id`: a trigger on a selected post that was a draft when picked, or a scenario with no trigger at all (started from outside Inrō), can still have recent runs.
- **[Broken]** In `performance`, a step where most runs stop. Read two failing runs with `executions` → `get` before naming the cause.
- **[Broken]** `suspended: true`.
- **[Broken]** A Meta Conversion event step with no event name, or an email alert step with no address. Imported templates often still have an empty alert email.
- **[Broken]** A link step still pointing at a template's example page or a placeholder URL.
- **[Risky]** `warnings: true` with only `suggestion` severities: a raw link in a message, a second DM straight after a comment reply with nothing that waits for the contact, adding contacts to a folder the scenario excludes.

Stale:
- **[Stale]** A comment trigger on `next_post` whose post is weeks old, or `select_posts` covering only old posts.
- **[Stale]** An active scenario with `last_executed_at` 30 or more days ago, unless it is attached to a scheduled post (`medias` → `list`, `status: scheduled`, `comment_to_dm`) and waiting for it.
- **[Stale]** Several scenarios with the same name and different content, or test copies left active.

Risky:
- **[Risky]** Two or more active scenarios that can match the same message, comment or story reply, with no Priority folder between them. Both run, and the contact gets two flows.
- **[Risky]** A `messages` trigger on any message with no filter: it fires on every DM, and the agent does not reply to a message a scenario has already answered.
- **[Risky]** High-volume triggers (any comment, any message, contact updated, recurring) with no **Limit frequency per contact**.
- **[Risky]** Lead or sales flows with no **Exclude specific folders**, when a customers folder exists.
- **[Risky]** Long follow-up sequences with **Interrupt when you reply manually** off: the flow keeps sending after a person has taken over.
- **[Risky]** `paused_executions` above zero: people waiting for a message that has not gone out.

Opportunity:
- **[Missing]** An inactive scenario with real past volume and conversions at or above the live ones. A switched-off asset is usually the best quick win.

## Campaigns

- **[Stale]** Drafts never sent, `scheduled` in the past, or `limited` sends never re-run.
- **[Risky]** Campaigns sent with no exclusion of customers or opted-out contacts, or with opt-out off.
- **[Missing]** Contacts active in the last few days and no campaign ever sent from Inrō. Size it on recently active contacts only.

## Contacts and data

- **[Missing]** Email or phone on almost no contacts while flows hand out freebies or book calls.
- **[Missing]** Most contacts in no folder, on an account with a few hundred contacts or more.
- **[Missing]** No folder that marks customers, or one used for exclusion, so there is no simple way to keep buyers out of lead flows.
- **[Stale]** Custom properties that no contact has filled in.
- **[Stale]** Segments nothing uses, or folders with zero contacts referenced by live flows.

## Content coverage

- **[Missing]** Recent posts or reels drawing comments that no comment flow covers. Size it with commenters per post over 30 days.
- **[Missing]** Comments that ask for the same thing in other words than the keyword flow expects. An AI-detected intent next to the keyword catches them.
- **[Missing]** Stories posted with replies arriving (story insights `replies`, contacts with `story_reply`) and no active `story_reply` flow. Size it on replies, never on the number of stories.
- **[Missing]** Story mentions arriving with no `story_mention` flow.
- **[Missing]** Contacts arriving from ads (`referral_ad`) with no `referral_ad` flow.
- **[Missing]** Lives with comments and no `live_comment` flow, only if the client goes live.

## Conversations and inbox

From the sample in `read-order.md`, step 9:

- **[Missing]** Conversations where the contact wrote last and nothing answered. Give the count, the sample size and how long they have waited.
- **[Missing]** The same questions repeating (price, delivery, booking, opening hours) with nothing that answers them: icebreakers, a menu entry, an AI-detected intent or the agent.
- **[Risky]** Every reply typed by hand (`sent_from: instagram` or `inbox`) on a busy account, or every reply from a flow with no person ever stepping in on a sales conversation.
- Before you call anything unanswered or manual, check for another tool (see `choosing-quick-wins.md`).

## Tracking

- **[Missing]** Links typed into messages as plain URLs instead of conversion links. They are not tracked and may not send.
- **[Missing]** Conversion points with no folder or property step, so converted people cannot be told apart later.
- **[Missing]** Ads running with no Meta Conversion event step, if the client measures ads by conversions.

## What the connector cannot see: check in the app

Say these are unchecked rather than guessing. Ask the person to look, or list them as decisions:

- The account-wide **Exclude specific contacts** filter (card on the **Scenarios** page). You only see it indirectly, through the `contact_matches_exclusion_filter` reason code.
- Integrations (account menu → **Integrations**): Shopify, Calendly, Stripe, Make, Meta Conversions API, and whether the Meta Conversions API card asks for a reconnect or refresh.
- AI credits on accounts that are not on Pro. When they run out the agent stops silently.
- Team members and their access (account menu → **Profile** → Team members, including "Prevent access to inbox").
- Inbox state: unread conversations, who is handling each one.
- The agent's AI model and reasoning level, which only apply with the account's own OpenAI key.
- Website widget appearance, and anything published outside Instagram.
- **Platform logs** (account menu): the API & MCP, Automations and API errors tabs, with each call's full request and response. Use them when a run's reason code is not enough. Logs are kept for a limited time, so copy out what you need.
