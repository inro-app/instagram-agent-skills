# Reading the account: calls, numbers and traps

Every call here is a read. On the partner connector, add the client (`organization`: username or id) to every call.

Tool names below are the Inrō connector's tools as your assistant sees them. Read tools and write tools are separate: `scenarios` reads, `scenarios_manage` writes. This skill only uses the read tools.

## Account

`get_organization_info`

| Field | What it tells you |
|---|---|
| `username`, `name` | Which account this is. Say it back before anything else. |
| `subscription_tier` | Pro or Trial is needed for the connector. Some steps (AI actions, A/B tests, live comments, webhooks, recurring schedules) are Pro only. |
| `login_error_data.login_error` | `true` means Instagram is disconnected and every automation is paused. First item of the plan: reconnect. |
| `instagram_restrictions` | Anything here limits what can be sent. Mention it. |
| `max_contact_activations` | A number here is a monthly cap on contacts the automations can reach. Big plays can hit it. |
| `optout_options.active` | Whether people can type "stop" to opt out. Off is a foundation gap. |

## Posts, reels and comments

`medias` with `action: list`, `status: published`, `per_page: 50`, newest first. For each post:

- `posted_at`, `media_product_type` (feed or reels), `caption`, `permalink`.
- `insights.comments`, `insights.reach`, `insights.views`, `insights.saved`, `insights.shares`. Insights are only present when `insights_status` is `fresh`. If it says `refreshing`, wait and read again; if `unavailable`, Instagram does not report on that post.
- `like_count`.
- `comment_to_dm`: present when the post already has its own comment automation.

Then count people, not comments:

```json
{ "action": "filter", "action_params": {
  "filters": [{ "filter_type": "comment", "date_operator": "is_on_or_after", "date_mode": "days_ago", "date_days": 30 }],
  "per_page": 1 } }
```

`pagination.total_count` is the number of people who commented in 30 days. Add `media_id` (the post's Instagram id, `instagram_id` on the media) to count one post.

Traps:

- **Check which posts are covered.** A post is covered when an active scenario's comment trigger watches it: all posts, that post selected, a caption keyword it contains, or a URL in its caption. Read the active comment scenarios with `scenarios` get before calling a post uncovered.
- **Read the comments themselves** on the three busiest posts. Spam bursts, giveaway entries, a hostile wave, or the same few friends on every post are not demand.
- **Comments with no question** (praise, emoji) still suit a thank-you or a soft "want the link?" flow, but they are a weaker case than comments asking for something.
- **Older posts.** Instagram only accepts a private reply within 7 days of a comment. Old comments on old posts cannot be reached by DM now.

## Stories

People who replied to any story:

```json
{ "filter_type": "story_reply", "date_operator": "is_on_or_after", "date_mode": "days_ago", "date_days": 30 }
```

People who mentioned the client in their own story: `story_mention`, same shape.

`stories` list shows the client's own stories and their insights (`replies` among them) while Inrō has them.

Trap: an account can post stories every day and get almost no replies. The play needs repliers, not stories.

## DMs

People who sent a DM in the window:

```json
{ "filter_type": "message", "date_operator": "is_on_or_after", "date_mode": "days_ago", "date_days": 30 }
```

Count a repeated question by adding `"value": "price"` (or "how much", "link", "book", the client's product name). The match is a case-insensitive substring of the message, so check a few hits.

To see what people ask, read a small sample: `contacts` filter on `message` sorted by `last_message_at` descending, then `contacts` get on 15 to 30 of them (it returns the latest 10 messages). Group what they want into four or five intents with a count each. Quote patterns in the plan, never a person.

`first_interaction` in the window counts people who wrote for the first time. That is the audience ice breakers and a welcome flow reach.

## Ads, mentions, lives

- `referral_ad` in the window: people who arrived from a click-to-message ad. Above zero means the client runs ads that open DMs.
- `media_mention`: people who tagged the client in a post.
- Lives: there is no count of live comments in the contacts filters. Ask the client whether and how often they go live.

## The list

- Contacts with an email: `email` with `operator: is_present`. Same for `phone`.
- Followers: `is_follower` with `operator: is_true`.
- Folder sizes: `folders` list, then a `folder` filter per folder that matters.
- People still reachable by a campaign right now: `any_engagement` in the last 1 day. Instagram only lets you message people who wrote to you in the last 24 hours, so this, not the total contact count, is the audience a campaign can actually reach today.

## What is already built

- `scenarios` list (`per_page: 100`), then `get` on each active one: trigger, steps, `rate_limit_*`, `interrupt_on_*`, folder.
- `scenarios` performance on each active one, `since` 30 or 90 days back (90 is the maximum): how many runs reached and finished each step, and why the others stopped. This is how you find the step where people drop off.
- Inactive scenarios: `get` and performance on any with a recent `last_executed_at` or real past volume.
- `executions` health for the window: run totals by status, the failure rate, the automations failing most, and account-level blockers.
- `campaigns` list: drafts, sent, scheduled.
- `conversion_links` list: links that exist. A link no flow sends is unused.
- `icebreakers` list: each ice breaker and the automations a tap starts. An empty `automations` list means the tap starts nothing.
- `persistent_menu` get: the menu entries. A `postback` entry can start a scenario; a `web_url` entry only opens a link.
- `agent` get: whether the AI agent is on and what it is told. Do not change it here. Its configuration belongs to `instagram-ai-agent-setup`.

## Measuring later

Name these in the plan so the report can use them:

- Runs per flow and step completion: `scenarios` performance.
- Link clicks: the flow's results in the app (Insights tab), or a `clicked_conversion_link` contacts filter with the link's id.
- Emails or phones collected: `email` present, combined with a `scenario` filter for the flow.
- Folder growth: a `folder` filter.
- Bookings and payments: `appointment` and `payment` filters, when the client uses those integrations.

Inrō records link clicks, not page visits or sales on the client's site. Say "opened the link", not "visited" or "bought", unless the client shares their own numbers.
