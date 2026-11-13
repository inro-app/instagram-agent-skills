# Read order, tool by tool

Every call here only reads. On the partner connector, add `"organization": "<client account id>"` to each one.

Tool names, fields and values below were checked against the connector and the app in November 2026. If a live response disagrees with this file, the live response wins.

## 1. Account

`get_organization_info` (no parameters). Read:

- `username`, `name`: say both back and get a yes before you go on.
- `subscription_tier`, `current_billing_period_end`: the plan, and when the trial or billing period ends. Read the tier as a hint, since it can lag the real plan. An account the connector does not serve is refused on every call, with a message that says so.
- `login_error_data.login_error` and `login_error_message`: `true` means Instagram is disconnected and every automation is stopped. The fix is in the app: **Instagram account** in the account menu (the account name, bottom left), then reconnect.
- `instagram_restrictions`: anything Instagram currently restricts on the account.
- `can_publish`, `missing_publish_scopes`: only matters if the client publishes posts from Inrō.
- `optout_options`: whether opt-out is on, its keywords, the menu entry and the confirmation message.

**Partner connector:** `list_organizations` first. `connected: false` lists every client account without a working Instagram connection, both broken ones and ones that never connected (`username: null`), which is a useful first look across a roster. Then `get_organization_info` with `organization`.

## 2. Health

`executions` → `health` with `since` set 30 days back (default 7 days, maximum 90). Read:

- `executions` by status. `limited`, `disconnected` and `restricted` are paused runs that can be re-run later. `partially_completed` means a step failed after earlier steps had run.
- `failure_rate`, `top_failing`, `top_reason_codes`.
- `account.instagram_connected`, `account.contact_activation_limit_reached`, `contact_activations_used`, `contact_activations_limit`. Either blocker stops every automation at once, and no edit to a flow fixes it.

For each automation in `top_failing`:

1. `scenarios` (or `campaigns`) → `performance` with the same window. It shows how many runs reached and finished each step, and the reasons behind the rest. This is what says which step breaks.
2. `executions` → `list` with `scenario_id` (or `campaign_id`) and `status: failed`, or a `reason_code`.
3. `executions` → `get` on one or two runs. A run's `action_data` is the step as it was when it ran, which matters if the flow has been edited since.

Show people a run's `status_message`; group runs by `reason_code`. Codes worth knowing:

| Code | What it means |
|---|---|
| `instagram_disconnected`, `account_restricted`, `plan_limit_reached` | an account-level blocker |
| `contact_in_excluded_folder` | skipped on purpose: the scenario excludes a folder the contact is in |
| `contact_matches_exclusion_filter` | skipped by the account-wide filter (Scenarios page, **Exclude specific contacts**) |
| `manual_reply`, `contact_replied`, `conversation_handled_by_human` | stopped because someone replied (the interrupt settings) |
| `scenario_not_active`, `scenario_suspended` | the flow is off, or suspended |
| `action_error`, `unexpected_error` | a step failed: read the run |

## 3. Entry points

- `icebreakers` → `list`. Up to 4 questions on the profile. Each has `automations` (scenario, whether it is active, how it matches). An empty `automations` array means tapping it starts no automation.
- `persistent_menu` → `get`. Up to 5 entries. A `postback` entry sends its payload into the conversation, which a scenario with an `icebreaker` trigger can match on payload. A `web_url` entry only opens a page and reaches no automation. Check every postback has an active scenario that matches it.
- `settings` → `get_optout`: `active`, `keywords`, `menu_message` (the opt-out entry in the menu), `confirmation_message`, `ai_detection` (whether the agent may also recognize an opt-out request in the person's own words).

Icebreakers and the menu are read live from Instagram, so they show what people actually see.

## 4. AI agent

`agent` → `get` returns the whole configuration. Use `agent` → `list_items` to page through knowledge if there are many items.

| Field | Where it is in the app |
|---|---|
| `trigger_mode` | **Activation rules**: All pending messages (`all_messages`), Specific intents only (`specific_messages`), Automation only (`automation_only`), Disable all replies (`never_reply`) |
| `trigger_intents.intents` | **AI-detected intents**, used only with Specific intents only |
| `folder_rules` | **Limit replies based on contact folders** (only these folders, or never these folders) |
| `about` | **Voice and personality** → **Profile** (500 characters, included in every reply) |
| `rules` with `kind: voice` | **Voice and personality** → Voice rules |
| `message_length` | Message length: 10, 25 or 50 words |
| `message_examples`, `auto_like` | Message examples; auto-like |
| `goal` | **Goal and instructions** → Goal (500 characters). A task set inside a scenario (hand over to the agent, AI message) replaces it for that conversation; comment replies don't use it |
| `rules` with `kind: instruction` | **Goal and instructions** → Instructions (one sentence each, 300 characters, up to 50 per kind). Rules apply to every reply, including scenarios and comment replies |
| `no_reply_active`, `no_reply_scenario_id` | **Knowledge access and behaviour**: Limit to instructions (`true`) or Always have an answer (`false`), and the automation to run when the agent cannot answer |
| `items` | **Training and knowledge**: Manual text (`text`), Website (`url`, optionally with other pages of the site), Text document (`file`). `retrieval: false` is the "Include this information in all Agent requests" switch. `status` is ready, processing or failed |
| `actions` | **Actions and automations**: when an intent is detected, send a conversion link, start a scenario, send a survey or add to a folder |
| `contact_properties`, `built_in_property_access` | **User data collection**: which properties the agent detects and saves, and whether it may read the contact's email and phone |
| `human_takeover_active`, `human_takeover_pause` | **Human intervention** → Handled by a team member: pause the agent for 1, 4, 12 or 24 hours after a person replies |
| `request_human_scenario_id` | **Human intervention** → Request a human: the automation to run when someone asks for a person |
| `context_migrated` | `false` means the agent still runs on older fields (`description`, `goals`, `chat_instructions`, `style_rules`, `role`, `account_type`, `audience_type`). The app moves them into Profile (`about`), Goal and rules the first time someone opens the AI Agent page. Back up the old fields too |
| `model`, `reasoning` | only apply when the account uses its own OpenAI key; `null` means the plan default. Not editable through the connector |

Resolve every `actions[].target_id`, `no_reply_scenario_id` and `request_human_scenario_id` against the lists you read in steps 5 and 7. A target that is switched off or no longer exists is dead wiring.

## 5. Automations

- `scenario_folders` → `list`. A **Priority folder** runs only the highest-priority matching scenario. A **Normal folder** runs every match, and so do scenarios in no folder.
- `scenarios` → `list` with `per_page: 100` until done. Per scenario: `active`, `suspended`, `scenario_type`, `last_executed_at`, `metrics` (runs and conversions), `paused_executions` (`limited`, `disconnected`), `excluded_folder_ids`, `rate_limit_enabled` / `rate_limit_unit` / `rate_limit_value`, `interrupt_on_message`, `interrupt_on_reply`, `scenario_folder_id`, `updated_at`.
- `scenarios` → `get` on every active scenario that ran in the window, the five busiest of all time, and any inactive one with real past volume: triggers with their options, and the action tree. On an account with more than about 30 active scenarios, list the rest from the `scenarios` → `list` fields and say so.
- `show_scenario` on the same scenarios. It draws the flow for the person and returns `warnings` (true or false) and `has_issues`, plus each step's own `warnings` list with a severity of `issue` or `suggestion`: the editor's own checks. Issues stop a flow; warnings are suggestions. The editor flags, among others: a raw link typed into a message, a second DM straight after a comment reply with no step that waits for the contact, adding a contact to a folder the scenario excludes, a trigger that can never fire, and a conversion link that no longer resolves.
- `scenarios` → `performance` (`since`, at most 90 days back) on the three to five flows with the most runs and on every flow that fails.

Trigger details that matter (confirm with `get_trigger_types`):

- `comment`: `post_type` is `all_posts`, `select_posts`, `caption_keywords`, `caption_url` or `next_post`. `next_post` only watches the first post published after the trigger was created. `comment_type` is `all_comments`, `comment_keywords` (needs at least one keyword), `ai_detected` (needs `ai_intent`), `hate_spam` or `tag_someone`. `allow_replies` and `exclude_negative` are on or off.
- Keywords match whole words, ignoring case and accents, and keywords of 4 or more characters also match a plural or one extra letter ("link" matches "links", "no" does not match "know").
- `messages`: `message_scope` is any message or the first message only; `content_filter` is any, keywords, only emojis or AI-detected.
- Also: `story_reply`, `story_mention`, `mention_comment`, `mention_media`, `live_comment`, `referral_ad`, `referral`, `icebreaker`, `folder`, `contact_create`, `contact_update`, `recurring`, `webhook`, `custom_event`, `widget`, `outgoing_message`.

A comment-to-DM set on a single post shows as a `comment_to_dm` object on that post in `medias` → `list`.

Older or app-built flows can hold step types that `get_action_types` does not list (for example store, booking or Meta Conversion event steps). Read them and back them up; whether they can be rebuilt through the connector is a "check in the app" item.

## 6. Campaigns

- `campaigns` → `list`, filtered by `status` if useful: `draft`, `running`, `completed`, `scheduled`, `limited`, `canceled`.
- `campaigns` → `get` on recent ones: audience rules (folders and segments, included or excluded) and actions.
- `campaigns` → `performance` on the last few sent: how far each send got, including sends paused by the activation limit or a broken connection.
- `campaign_folders` only keep campaigns tidy. They change nothing about sending.

Campaigns only reach people inside Instagram's messaging window. Inrō's campaign templates describe it as people who messaged the account in the last 24 hours. Size any campaign on recently active contacts, never on the total list.

## 7. Contacts and data

Use `contacts` → `filter` with `per_page: 1` and read `pagination.total_count`. Use `contacts` → `list` with `per_page: 1` for the total. Call `get_contact_filter_types` once if you need more than these.

| Number | Filter |
|---|---|
| Total contacts | `contacts` → `list` |
| Active in the last 30 days | `any_engagement`, `date_operator: is_on_or_after`, `date_mode: days_ago`, `date_days: 30` |
| Messaged in the last 30 days | `message` with the same date fields |
| With an email | `email`, `operator: is_present` |
| With a phone | `phone`, `operator: is_present` |
| In no folder | `folder` with no `value` |
| Opted out | `status`, `operator: is_equal`, `value: optout` |
| Following the account | `is_follower`, `operator: is_true` |
| Came from ads | `referral_ad` with a window (`is_on_or_after`, `days_ago`, 30); `is_present` alone can be refused |
| Clicked a given link | `clicked_conversion_link` with `conversion_link_id` and a window |
| A custom property filled in | `contact_property`, `operator: is_present`, `options: {"contact_property": "property_123"}` |

On larger accounts the connector can refuse some account-wide counts with "too many contacts to search or filter this way": `comment` without `media_id`, `clicked_conversion_link` without `conversion_link_id`, and `referral_ad` without a window. Count per post or per link instead, and say the account-wide figure was not available.

- `folders` → `list` gives names and colours only. For each folder's size: `folders` → `list_contacts` with `per_page: 1`.
- `segments` → `list`, then `get` for filters and `contacts_count` (it can be null; then count with the same filters if the connector allows it).
- `contact_properties` → `list`: title, slug, `property_type`, choices, `auto_detect`. Whether the agent detects a property is in `agent` → `get` → `contact_properties`, not here.
- `conversion_links` → `list`: title, URL, button. The list carries no click counts: count clicks with the filter above, and read conversions from each scenario's `metrics`.

## 8. Content coverage

- `medias` → `list` with `status: published` and `per_page: 100`. Sort by `posted_at` yourself, skip entries with no `posted_at`, and take the last 20 to 30 posts and reels. For each one: `caption`, `media_product_type`, `posted_at`, `comment_to_dm`, and `insights` when `insights_status` is `fresh` (reach, views, likes, comments, saves, shares). Instagram's comment count includes the account's own replies.
- People commenting on one post: `contacts` → `filter` by `comment` with that post's `media_id` (its `instagram_id`) and a window.
- A post is **covered** if it has a `comment_to_dm`, or an active comment scenario reaches it: `all_posts`; `caption_keywords` that appear in its caption; `caption_url` when its caption has a link; `select_posts` that include it; `next_post` only if it is that one post.
- `stories` → `list`. Story `insights` include `replies` when fresh. Stories sync into Inrō as they are posted, so a newly connected account has little story history: say so instead of reading it as "no replies". The list is not in date order (two-year-old stories can come first) and each entry carries long media URLs: filter by `posted_at` yourself and keep the pull in a helper.
- Story replies and mentions arriving: `contacts` → `filter` by `story_reply` or `story_mention` with a 30-day window.

## 9. Conversations, from a sample

1. `contacts` → `filter` by `message` in the last 30 days, `order_column: last_message_at`, `order_direction: desc`, `per_page: 30`.
2. `contacts` → `get` on each one. It returns the latest 10 messages; use `contacts` → `list_messages` if you need more.
3. For each conversation, note: who wrote last; if the contact wrote last, how long ago; who answered, from the sent messages (`received: false`) and their `sent_from`: `instagram` (typed in the Instagram app), `inbox` (typed in Inrō), `agent` (the AI agent), `automation` (a flow), `api` (the API or a connector); and what the person wanted, in a few words. Read past a greeting to the actual request.
4. Group what people ask into four or five intents with a count each. Keep the sample size next to every share.

Inrō imports about six months of conversation history when an account is first connected, so older threads can be there even on a new account. Keep message text out of anything you share.

## 10. Building blocks

`get_trigger_types` and `get_action_types` list what can be built today. Write down the triggers and step types the account never uses. That list feeds "what is missing", filtered by what this business actually has traffic for.
