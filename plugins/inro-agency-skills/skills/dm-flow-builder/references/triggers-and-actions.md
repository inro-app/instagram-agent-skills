# Triggers and actions

Checked against `get_trigger_types` and `get_action_types` on 12 November 2026. Call both before every build: the live response wins.

## Triggers

Several triggers on one scenario combine with OR: any one of them starts the flow.

| `trigger_type` | Fires when | Main options |
|---|---|---|
| `messages` | Someone sends a DM | `message_scope`: `any` or `first_message`. `content_filter`: `any`, `keywords`, `only_emojis`, `ai_detected`. `keywords`, `keywords_logic` (`or`/`and`), `strict_keywords_match` (whole message must equal a keyword), `ai_intent` |
| `comment` | Someone comments on a post or reel | All inside `comment_options`. `post_type`: `all_posts`, `select_posts` (+`post_ids`), `caption_keywords` (+`caption_keywords`), `caption_url` (+ optional `caption_url_filters`), `next_post`. `comment_type`: `all_comments`, `comment_keywords` (+`comment_keywords`), `ai_detected` (+`ai_intent`, required), `hate_spam`, `tag_someone`. `allow_replies` (default off), `exclude_negative` (AI check) |
| `story_reply` | Someone replies to a story | `story_filter`: `any`, `caption_keyword` (+`caption_keyword`), `caption_url`, `visual_ai` (+`visual_condition`, AI credits). `content_filter` on the reply: `any`, `keywords`, `only_emojis`, `ai_detected`, with the same keyword options as `messages` |
| `story_mention` | Someone mentions the account in their story | `story_mention_option`: `any`, `keywords` (text legible in the story), `visual_ai` (+`visual_condition`) |
| `live_comment` | Someone comments during a Live | `live_comment_option`: `any` or `keywords`. Pro |
| `mention_media` | Someone tags the account in a post caption | `mention_option`: `any` or `keywords` |
| `mention_comment` | Someone mentions the account in a comment | `mention_option`. Not in the app's trigger menu, works through the connector |
| `referral_ad` | Someone messages from a click-to-message ad | `referral_ad_option`: `keywords` or `ad_id` (+`referral_ad_id`) |
| `referral` | Someone opens an ig.me referral link or QR code, then messages | `referral_code`, `*` wildcard allowed. Fires on their message, not the click |
| `icebreaker` | Someone taps an ice breaker, or a postback entry of the persistent menu | `icebreaker_payload` (survives rewording) or `icebreaker_title` (breaks if the question is reworded). Prefer the payload |
| `outgoing_message` | The account sends a DM | `content_filter`, `keywords` (case-sensitive here), `outgoing_message_sent_from`: instagram, inbox, agent by default; `api` and `automation` optional |
| `folder` | A contact is added to a folder | `folder_id`. Removal does not fire it. Adding also fires `contact_update` |
| `contact_create` | A new contact appears | `contact_status_option`: `active` |
| `contact_update` | A contact's details, folders or properties change | `contact_status_option`. Fires often: use run-once and exclusions |
| `recurring` | On a daily, weekly or monthly schedule, for every contact matching filters | `recurring_frequency`, `recurring_time` (HH:MM, account time zone), `recurring_day_of_week` (0 = Sunday), `recurring_day_of_month`, `recurring_only_new_contacts`, `contact_filters`, `filter_logic`. Pro |
| `webhook` | An external system posts to the scenario's own URL | The request must name an existing contact. Pro |
| `widget` | A website visitor uses the Inrō widget and sends its code | `widget_options`: `header_text`, `button_text`, `custom_style`. Pro |
| `custom_event` | Listed, but has no working firing path today | Do not build on it. Use `webhook` |

Matching rules for keywords: whole words, case and accents ignored, a keyword of 4 or more letters also matches a plural or one extra letter. Emojis work as keywords.

AI-detected intent: write one short sentence of what the person wants ("asks what a first class costs"). Narrow beats broad: "asks a question" matches nearly everything. Two scenarios with overlapping intents both fire. Needs AI features on the account and uses AI credits when it matches. The app has a **Test intent detection** field on the trigger.

## Actions

Children of a branching action go under one of its branch labels (`parent_branch`). Children of a non-branching action have no `parent_branch`. Only one child per branch runs.

### Messages

| `action_type` | Does | Branches | Notes |
|---|---|---|---|
| `message` | Sends text | none | `content`, up to 1,000 characters. A raw URL draws a warning |
| `button_template` | Text with buttons | `option_0`, `option_1`, ... (one per postback button), `option_expired` | `options.buttons`: `[{ "title": "Send it" }]` (postback by default) or `{ "title", "type": "web_url", "url" }`. `expire_duration`, `expire_unit` |
| `media_message` | Image or video | none | `media_file_id`, or `media_file_url`, or up to 10 images with `media_file_ids`. JPEG, PNG, GIF, MP4, MOV |
| `audio_message` | Voice note from an audio file | none | `media_file_id`. No text to speech |
| `send_file` | File with a download button | none | `content` (text above), `media_file_id`, `button_label` (default "Download") |
| `share_media` | Shares one of the account's own posts | none | `media_ig_id` (the post's `instagram_id`) |
| `like` | Likes the contact's last DM | none | Not for comments |
| `ask_for_follow` | Asks for a follow, checks it | `option_followed`, `option_expired` | `content`, `button_label`, `incorrect_label`. One per scenario |
| `card_template` | Carousel of cards | per card button, `option_expired` | Shown to developer accounts only in the app; prefer `button_template` or `conversion_link` |

### Conversions

| `action_type` | Does | Branches | Notes |
|---|---|---|---|
| `conversion_link` | Tracked link card | `option_clicked` (fires even after the timeout), `option_expired` | Inline `conversion_link: { title, url, button_title, subtitle }` or `{ id }`. `expire_duration`, `expire_unit` |
| `payment_link` | Stripe payment card | none | `payment_amount` (required), `payment_description` (80 characters). Pro, needs Stripe connected. Does not wait for payment |
| `survey` | Survey in the DM | `option_filled`, `option_expired` | Reference `survey: { id }` or create one inline with `title`, `survey_type` (`single_choice` or `questions`), options and questions |

Calendly, Shopify and other integration steps exist in the app when the integration is connected. Check in the app.

### Questions and waiting

| `action_type` | Does | Branches | Notes |
|---|---|---|---|
| `ask_question` | Question with quick-reply buttons | `option_0`, `option_1`, ... per option, `option_replied` (any other reply), `option_expired` | `ask_question_options`, `contact_property` to save the answer, `ai_detection` (the **AI Agent Question** in the app, Pro), `autoreply_enabled` + `incorrect_label` + `max_attempts` + `max_attempt_mode` (`expire`/`continue`), `disable_quick_replies` |
| `collect_property` | Asks for an email, phone or property and saves it | `option_property`, `option_expired` | `contact_property` (`email`, `phone` or a custom property key), retries as above, `skip_ai_detection`. **Ask for information** in the app |
| `wait_for_reply` | Waits silently for the next message | `option_replied_0`, `option_replied_1`, ... (one per keyword branch), `option_replied` (any other reply), `option_expired` | `branches: [{ "keywords": [...] }]`, `expire_duration`, `expire_unit` (minutes, hours, days). Cannot save the reply |
| `delay` | Waits | none | `delay_duration`, `delay_unit` |

### Logic

| `action_type` | Branches | Notes |
|---|---|---|
| `scenario_condition` | `option_true`, `option_false` | `condition_type`: `message_contains`, `contact_property`, `variable`, `time`; `condition_operator`, `condition_value` |
| `contact_filter_condition` | `option_true`, `option_false` | `contact_filters` (same format as contact filters), `filter_logic` |
| `ab_testing` | `option_a`, `option_b` | `ratio` = percent to `option_a`. Pro |
| `trigger_scenario` | none | `scenario_id`, `trigger_data`. The target must be active |
| `http_request` | `option_success`, `option_failure` | URL, method, headers, body |

### Contacts

| `action_type` | Notes |
|---|---|
| `folder` | `folder_ids`, `folder_action` (`add`/`remove`). Adding fires `folder` triggers, which is how flows chain |
| `update_property` | `contact_property`, value in `content` (variables allowed) |
| `contact_status` | `contact_status_action`: `opt_in` or `opt_out` |
| `send_email` | Email to the team or the contact. Put it last in its branch |

### Comments

| `action_type` | Notes |
|---|---|
| `comment` | Public reply to the triggering comment. Text goes in `options.comment_variants` (one is picked at random, spintax and variables allowed). `comment_limiting` (progressive limiting on busy posts), `autowrite` (AI rewrite), `like_comment` |
| `like_comment` | Likes the triggering comment |
| `hide_comment` | Hides the triggering comment |

### AI steps

All use the account's global AI agent settings (voice, rules, knowledge). Pro, AI features on, AI credits. When credits run out, AI steps are skipped and the flow continues.

| `action_type` | In the app | Branches | Notes |
|---|---|---|---|
| `agent_reply` | AI Agent auto-DM | none | Replies once to the last message or comment |
| `agent_message` | AI Agent message | none | Instructions in `options.agent_task` (not `content`). `agent_message_length`: the app offers 10, 25, 50 or 100 words; without it, 10 |
| `agent_comment` | AI Agent auto-comment | none | Public reply to the triggering comment, no instructions. Length 5, 10 or 25 words |
| `agent_handover` | Hand over to AI Agent | `option_completed`, `option_expired` | `agent_task` is needed for `option_completed` (the AI judges the task done) |
| `ai_condition` | AI-detected condition | `option_true`, `option_false` | `ai_condition_text`: a plain-language condition read against the conversation |

The AI steps' voice and knowledge are configured in `instagram-ai-agent-setup`. A change there changes every live flow that uses an AI step.

## Scenario settings (create and update)

| Field | Use |
|---|---|
| `title` | Name for the report |
| `active` | `false` on create |
| `scenario_type` | `custom` (default for your builds), `comment_to_dm` (wizard type), `comment_moderation`. Converting a wizard scenario to Custom in the app cannot be undone |
| `rate_limit_enabled`, `rate_limit_unit` (`once`, `seconds` to `weeks`), `rate_limit_value` | Run once per person, or once per period |
| `interrupt_on_message` | Stop pending runs when your team replies by hand |
| `interrupt_on_reply` | Stop pending runs when the contact writes (except at a step waiting for that reply) |
| `scenario_folder_id`, `scenario_folder_priority` | Scenario folder, and priority inside a priority folder (1 = highest) |

Per-scenario excluded folders are set in the app (**Exclude specific folders**).
