# Recipes

Each recipe is a starting shape. Replace the example text, links and ids with the client's own, call `get_trigger_types` and `get_action_types` first, and keep `active: false`. After every create or update, call `show_scenario` and read the warnings in the response.

Ids in the examples (`4521`, `111`, `222`, `333`) are placeholders. Take real ones from `medias` list, `folders` list and `conversion_links` list.

## 1. From a template

1. `search_templates` with `type: "Scenario"` (or `"Campaign"`) and a plain query ("story replies link", "collect emails"). Pick one with the user. See `templates.md`.
2. `scenarios_manage` create with `template_id` and a `title`. The copy arrives switched off.
3. `scenarios` get on the new id and go through every step:
   - **Link steps**: the copy has its own link with the template's example URL. Read `options.conversion_link_id`, then `conversion_links_manage` update that id with the client's `url`, `title` and `button_title`.
   - **Trigger**: set the keyword and the posts. Update the trigger by its `id` so the other triggers are kept.
   - **Folder steps**: `options.folder_ids` must be the client's folders. Fix any that are missing or empty.
   - **Alert emails** (`send_email`): fill in the team address.
   - **Copy**: every message, in the client's voice.
4. `scenarios_manage` update with the full actions list (each step's `id`, plus the fields you change), then `show_scenario`.

The same template can be opened by the client on its public share page, where **Use this automation** copies it into their account, switched off.

## 2. Comment to DM on one post (the shortcut)

`medias_manage`, action `attach_comment_to_dm`:

```json
{
  "id": 4521,
  "active": false,
  "comment_options": {
    "comment_type": "comment_keywords",
    "comment_keywords": ["GUIDE"],
    "exclude_negative": true
  },
  "conversion_link": { "url": "https://example.com/guide", "button_title": "Get the guide" },
  "question_type": "button_template"
}
```

- `question_type`: `button_template` (tap a button, lowest friction), `message` (plain DM, link sent when they reply), `ask_for_follow` (must follow first, verified), `collect_property` (email before the link).
- `conversion_link`: `{ "url": ... }` builds a new card from the page's title and image; add `title`, `subtitle`, `button_title` or `image_url` to override; or `{ "id": 7 }` sends an existing link unchanged.
- The other steps (public reply, the question, the follow-up, folder tagging, a pixel event) are copied from the account's most recent comment-to-DM automation, or default wording if there is none. So read them back: `medias` get on the post shows `comment_to_dm` with its scenario id, then `scenarios` get, and fix the copy with `scenarios_manage` update.
- Calling it again on the same post updates that post's automation instead of adding a second one.
- On a new post, pass the same object as `comment_to_dm` to `medias_manage` create, with `"active": false` inside it. The automation starts matching when the post goes live.

## 3. Comment to DM on every post with a caption word

Keyword trigger plus an AI-intent trigger, public reply, a button, the link, a folder for clickers, one reminder. `scenarios_manage` create:

```json
{
  "title": "Comments: GUIDE to free guide",
  "active": false,
  "rate_limit_enabled": true,
  "rate_limit_unit": "once",
  "interrupt_on_message": true,
  "triggers": [
    { "trigger_type": "comment", "options": { "comment_options": {
      "post_type": "caption_keywords", "caption_keywords": ["guide"],
      "comment_type": "comment_keywords", "comment_keywords": ["GUIDE"],
      "allow_replies": false, "exclude_negative": true } } },
    { "trigger_type": "comment", "options": { "comment_options": {
      "post_type": "caption_keywords", "caption_keywords": ["guide"],
      "comment_type": "ai_detected",
      "ai_intent": "asks how to get the free guide or for the link to it",
      "exclude_negative": true } } }
  ],
  "actions": [
    { "action_key": "reply", "action_type": "comment",
      "options": { "comment_variants": ["Sent, check your DMs", "Just sent it to your DMs", "It's in your DMs now"],
                   "comment_limiting": true, "like_comment": true } },
    { "action_key": "ask", "parent_key": "reply", "action_type": "button_template",
      "content": "Hi {{contact.name}}! Want the free guide? Tap below.",
      "options": { "buttons": [{ "title": "Send it" }], "expire_duration": 24, "expire_unit": "hours" } },
    { "action_key": "link", "parent_key": "ask", "parent_branch": "option_0", "action_type": "conversion_link",
      "conversion_link": { "title": "The free guide", "url": "https://example.com/guide", "button_title": "Open the guide" },
      "options": { "expire_duration": 3, "expire_unit": "hours" } },
    { "action_key": "tag", "parent_key": "link", "parent_branch": "option_clicked", "action_type": "folder",
      "options": { "folder_ids": [111], "folder_action": "add" } },
    { "action_key": "nudge", "parent_key": "link", "parent_branch": "option_expired", "action_type": "message",
      "content": "Did you get a chance to open the guide?" }
  ]
}
```

Why this shape: the public reply tells them to look; the button is the one DM Instagram allows after a comment, and the tap opens the conversation; the link comes after the tap; the reminder goes out a few hours later, inside the 24-hour window.

Variants:

- **All posts**: `"post_type": "all_posts"`. **Chosen posts**: `"select_posts"` with `post_ids` (Inrō media ids). **The next post only**: `"next_post"`, which watches the first post published after the trigger is created.
- **Email first**: replace `ask` with `collect_property` (`"contact_property": "email"`, a prompt in `content`), and hang the link on `option_property`. Hang a second copy of the link on `option_expired` if people who skip the email should still get it.
- **Follow first**: `ask_for_follow`, link on `option_followed`.
- **Tag-a-friend**: `"comment_type": "tag_someone"`.

## 4. DM keyword reply

Someone already wrote, so the conversation is open and several messages can follow each other.

```json
{
  "title": "DM: price question to price list",
  "active": false,
  "interrupt_on_message": true,
  "triggers": [
    { "trigger_type": "messages", "options": {
      "message_scope": "any", "content_filter": "keywords",
      "keywords": ["price", "cost", "how much"], "keywords_logic": "or" } },
    { "trigger_type": "messages", "options": {
      "message_scope": "any", "content_filter": "ai_detected",
      "ai_intent": "asks what the classes or memberships cost" } }
  ],
  "actions": [
    { "action_key": "like", "action_type": "like" },
    { "action_key": "answer", "parent_key": "like", "action_type": "message",
      "content": "Hi {{contact.name}}! Here are our prices and what each option includes." },
    { "action_key": "link", "parent_key": "answer", "action_type": "conversion_link",
      "conversion_link": { "title": "Prices", "url": "https://example.com/prices", "button_title": "See prices" },
      "options": { "expire_duration": 3, "expire_unit": "hours" } },
    { "action_key": "nudge", "parent_key": "link", "parent_branch": "option_expired", "action_type": "message",
      "content": "Any questions about which option fits you? Just reply here." }
  ]
}
```

If the AI agent also answers DMs, decide which one handles prices. A running scenario takes priority over the agent for that conversation, but two answers to the same question still confuse people.

## 5. Story reply to a link

```json
{
  "title": "Story replies: LINK to timetable",
  "active": false,
  "rate_limit_enabled": true, "rate_limit_unit": "hours", "rate_limit_value": 24,
  "triggers": [
    { "trigger_type": "story_reply", "options": {
      "story_filter": "any", "content_filter": "keywords",
      "keywords": ["LINK"], "keywords_logic": "or" } }
  ],
  "actions": [
    { "action_key": "link", "action_type": "conversion_link",
      "conversion_link": { "title": "This week's timetable", "url": "https://example.com/timetable", "button_title": "Open timetable" },
      "options": { "expire_duration": 3, "expire_unit": "hours" } },
    { "action_key": "tag", "parent_key": "link", "parent_branch": "option_clicked", "action_type": "folder",
      "options": { "folder_ids": [111], "folder_action": "add" } },
    { "action_key": "nudge", "parent_key": "link", "parent_branch": "option_expired", "action_type": "message",
      "content": "Here when you're ready to book. Just reply if you have a question." }
  ]
}
```

A story reply arrives as a DM, so the one-message rule of comments does not apply. To match only stories with a word or a link in the caption, use `"story_filter": "caption_keyword"` with `caption_keyword`, or `"caption_url"`. Caption matching needs stories created in the Instagram app.

## 6. Welcome on the first message

```json
{
  "title": "DM: welcome menu on first message",
  "active": false,
  "rate_limit_enabled": true, "rate_limit_unit": "once",
  "interrupt_on_message": true,
  "triggers": [
    { "trigger_type": "messages", "options": { "message_scope": "first_message", "content_filter": "any" } }
  ],
  "actions": [
    { "action_key": "menu", "action_type": "ask_question",
      "content": "Hi {{contact.name}}, thanks for writing! What can I help with?",
      "options": { "ask_question_options": [{ "title": "Prices" }, { "title": "Book a class" }, { "title": "Something else" }],
                   "expire_duration": 24, "expire_unit": "hours" } },
    { "action_key": "prices", "parent_key": "menu", "parent_branch": "option_0", "action_type": "conversion_link",
      "conversion_link": { "title": "Prices", "url": "https://example.com/prices", "button_title": "See prices" } },
    { "action_key": "book", "parent_key": "menu", "parent_branch": "option_1", "action_type": "conversion_link",
      "conversion_link": { "title": "Book a class", "url": "https://example.com/book", "button_title": "Book" } },
    { "action_key": "human", "parent_key": "menu", "parent_branch": "option_2", "action_type": "message",
      "content": "Tell me a bit more and someone from the team will reply here." },
    { "action_key": "human_tag", "parent_key": "human", "action_type": "folder",
      "options": { "folder_ids": [222], "folder_action": "add" } },
    { "action_key": "other", "parent_key": "menu", "parent_branch": "option_replied", "action_type": "folder",
      "options": { "folder_ids": [222], "folder_action": "add" } }
  ]
}
```

A first message is often a real question. If people type instead of tapping, `option_replied` files them for a person. Turning on `ai_detection` on the question (the **AI Agent Question** in the app) matches typed answers to the closest button.

## 7. Ice breakers

Ice breakers live on the Instagram profile: up to 4 questions shown when someone opens a chat for the first time. Changing them changes the live profile at once, so get the OK on the exact wording first.

1. `icebreakers` list. Each one shows the automations a tap starts; an empty list means nothing answers it.
2. `icebreakers_manage` create with the `question`. The response returns its `payload`.
3. A scenario with `{ "trigger_type": "icebreaker", "options": { "icebreaker_payload": "<payload>" } }` and the answer (a message plus a link card, or a short question). Switched off, tested, then switched on.
4. To reword later, `icebreakers_manage` update with the same `payload`: the trigger keeps working. A trigger on `icebreaker_title` stops firing when the wording changes.

Between steps 2 and 3, the new ice breaker shows on the profile with nothing behind it. Keep that gap short. In the app, the ice breakers card also offers ready-made ways to answer an unanswered one.

## 8. Persistent menu

The menu inside every DM thread. Keep it to 5 entries or fewer; titles are cut at 30 characters. Changes are live on Instagram at once.

- A link entry: `persistent_menu_manage` add with `"type": "web_url"`, `title`, `url`. It opens the page and starts no automation.
- An automated entry: add with `"type": "postback"` and a `title`; the response gives its `payload`. Build a scenario with an `icebreaker` trigger on that payload.
- The opt-out entry is kept in step with the opt-out setting. Deleting it turns opt-out off. Leave it alone.

## 9. Follow-ups and chaining

- **Inside a flow**: hang one message on the `option_expired` branch of the link, question or button step. Keep the timeout in hours. Instagram only lets you message people who wrote in the last 24 hours; a message outside that is held, retried, and dropped if they do not write again.
- **Next flow**: end with a `folder` add. A second scenario with a `folder` trigger on that folder starts for them.
- **Hand to a person**: a `folder` step into a "Needs a human" folder plus a `send_email` alert, last in the branch. With `interrupt_on_message: true`, the flow stops when the team replies.
- **Hand to the AI agent**: `agent_handover` with a one or two sentence `agent_task` ("Find out which class time suits them, then send the booking link"). Check the agent is set up first (`instagram-ai-agent-setup`).
- **On a schedule** (Pro): a `recurring` trigger with contact filters. Turn on `recurring_only_new_contacts` so nobody gets it twice. The same 24-hour rule applies, so a weekly message reaches only people who wrote recently.

## 10. Campaigns

A campaign is a draft until it is sent, and sending messages real people. It reaches active contacts who can receive a DM now, which in practice means people who wrote in the last 24 hours.

1. If the campaign sends a link, create the link first with `conversion_links_manage` create, and reference it by `options.conversion_link_id`. Campaign actions take no inline link or media.
2. `campaigns_manage` create:

```json
{
  "title": "Launch day: waitlist",
  "actions": [
    { "action_key": "hello", "action_type": "message",
      "content": "It's open! You asked to hear first, so here it is." },
    { "action_key": "link", "parent_key": "hello", "action_type": "conversion_link",
      "options": { "conversion_link_id": 333, "expire_duration": 6, "expire_unit": "hours" } }
  ],
  "campaign_rules": [
    { "list_type": "folder", "rule_type": "inclusion", "destination_id": 111 },
    { "list_type": "folder", "rule_type": "exclusion", "destination_id": 222 }
  ]
}
```

3. `show_campaign`: the user sees the flow, who is included and excluded, and how many contacts it will reach.
4. `campaigns_manage` test with `campaign_id` and your own contact. A test contact who is also in the audience gets it again on the real send, so test with someone outside it.
5. Send only when the user approves the audience and the count in writing: `campaigns_manage` send, then poll `batch_tasks` get with the returned id. Scheduling (`scheduled_at`) is also a send decision.

Or clone a campaign template with `template_id` (see `templates.md`).

## 11. Moderation

To hide abusive comments across posts, the **Comment moderation** option in the New scenario window builds it, or template "Hide hateful comments". By hand: a `comment` trigger with `"comment_type": "hate_spam"` and a `hide_comment` step. On that trigger leave `exclude_negative` off, because it would filter out the comments the flow is meant to catch.
