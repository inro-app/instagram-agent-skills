---
name: client-post-scheduler
description: "Writes an Instagram caption and hashtags in a client's brand voice for an image, carousel, reel or story, then saves it as a draft, schedules it or publishes it on the client's account through Inrō once you approve. Works from a brand-voice file you fill once per client, converts times to the client's time zone, and can add a comment-to-DM automation so people who comment a keyword get a DM with a link. Use when an agency says 'write a caption for this', 'schedule this post for my client', 'post this reel Friday at 6pm', 'draft next week's posts', 'reschedule the Tuesday post', 'what is scheduled for this client', 'set up a brand voice for a new client' or 'add comment to DM to this post'."
license: MIT
---

# Client post scheduler

You write the caption, the agency approves it, and the post goes into the client's Inrō account as a draft, a scheduled post or a live post. One client at a time.

## Requirements

- **One client:** the Inrō connector at `https://api.inro.social/mcp` (OAuth). One Instagram account per connection, and that account on Pro (monthly or annual), a free trial, or a lifetime plan (free accounts are refused).
- **Many clients:** the Inrō partner connector at `https://api.inro.social/partner/mcp`, with the partner token in an `Authorization: Bearer` header. Every call names the client in the `organization` field (prefer the account id from `list_organizations`; a username that matches several accounts is refused). There is no default client. Each client still needs one of those plans. `list_organizations` lists the clients you can act on.
- **Instagram publishing permission:** scheduling and publishing only work when the client's Instagram connection has granted Instagram's content-publishing permission. `get_organization_info` returns `can_publish`. When it is `false`, drafts still work, and the client opens `publishing_reauth_url` in a browser to grant the permission.
- **Without a connector** the skill still writes the caption, hashtags, alt text and the approval card. You then post by hand.

Tool names below are the ones the connector exposes. Your Claude app may show them with a prefix (the connector's name). Use whatever your connection lists; never assume a prefix from an example.

- Read: `get_organization_info`, `medias`, `stories`, `media_files`, `scenarios`, `show_scenario`
- Write: `media_files_manage`, `medias_manage`, `stories_manage`

Exact call shapes, every field, formats and limits: `references/publishing-reference.md`.

## Safety rules (always)

1. Confirm the account before anything else. Call `get_organization_info` and say back the Instagram username you are connected to. If it isn't the client the agency named, stop.
2. On the partner connector, put `organization` on every single call, reads included. Prefer the account id: a username can match more than one account, and then the call is refused.
3. Read first, write second. Nothing is uploaded, drafted, scheduled or published until the agency has seen the approval card (Step 6) and said yes to it.
4. An approval covers exactly the posts on the card. A post added later needs its own yes.
5. "Publish now" gets one more confirmation, because a published post can't be edited from Inrō and Instagram shows it at once.
6. Never publish as a test. To check how something looks, save a draft and look at it in Inrō under **Content**.
7. A comment-to-DM automation is created switched off and turned on only when the agency says so. Test it from an account your team controls, never by messaging real followers.
8. Never delete without an explicit yes for that item. Deleting a published post through Inrō also removes it from Instagram.
9. One client at a time, unless the agency asked for the same change across several clients.

## Step 1. Confirm the client and the account

- Single connector: `get_organization_info`. Note `username`, `subscription_tier`, `can_publish`, `missing_publish_scopes`.
- Partner connector: `list_organizations` if you need the id, then `get_organization_info` with `organization` set to the client.
- If the account isn't on Pro, a trial or a lifetime plan, every call is refused, reads included, with a message saying so. `subscription_tier` is a hint only: it can lag the real plan, so go by the refusal. Tell the agency: nothing can be read or drafted until the plan changes.
- If `can_publish` is false, say so now: you can still save drafts, and the client needs to re-authorize from `publishing_reauth_url` before anything can be scheduled.

## Step 2. Load the client's brand-voice file

Each client gets one brand-voice file, filled once and reused for every post. The template is in `references/brand-voice-template.md`.

- If the agency has the file (attached, pasted, or in the Claude Project for that client), read it before writing anything.
- If not, offer to fill it now. Ask the questions in the template in one go, accept "skip" for any of them, and hand the finished file back so the agency can save it where they keep client files (a Claude Project for that client works well). Don't hold up an urgent post for it: at minimum get the **time zone**, the **voice in three words**, and **words or claims to avoid**.
- The file decides the defaults: time zone, approval route (agency only, or client sign-off), default action (draft or schedule), hashtag set, keyword conventions, and links for DM offers.

## Step 3. Look at the media

- Look at what is actually there: subject, setting, any text on the image, product, people, mood. Write for this image, not for the topic.
- For a reel you can't watch, ask for the script or a two-line description and the first frame. Don't invent what a video shows.
- If the file is already in Inrō and you can't see it, you only have its `caption` (Inrō's AI description) and `media_dimensions` from `media_files` `get`. Say so, and ask the agency to confirm what's in the picture before you write.
- Check the format before you write (details in the reference): carousel 2 to 10 items, feed images between 4:5 portrait and 1.91:1 landscape, reels and stories vertical. Images and audio up to 25 MB, video up to 250 MB.
- Ask whether the visual was made with AI. Photorealistic AI content needs Instagram's AI label (`is_ai_generated`), and it can only be set before publishing.

## Step 4. Write the caption

Follow the brand-voice file. Then:

- **First line does the work.** Only the first line or two show before "more". Make it a reason to stop, in the client's voice. For hooks, `short-form-content-principles` has the thinking.
- **Short paragraphs, plain words.** No filler openers, no hype the client can't back up, no em dashes.
- **One call to action**, chosen for the post's goal: save, share, comment a keyword, book, visit the profile. If the post will carry a comment-to-DM automation, the call to action is "Comment KEYWORD and we'll DM you the X", using the exact keyword the automation listens for.
- **Hashtags: up to 5.** Instagram now allows at most 5 hashtags on a post or reel (check the app if a post is refused). Pick specific ones from the client's approved set, put them at the end.
- **Mentions** only for accounts the agency or the brand file names. Tagging an account notifies it.
- **Length:** 2,200 characters at most, including hashtags.
- **Alt text:** write one line describing the image for screen readers, unless the brand file says otherwise.
- Stories have no caption. For a story, you only need the media, optional people tags and the time.

Give one caption you recommend. Add one alternative first line only if the agency asked for options.

## Step 5. Pick the time

- Use the client's time zone from the brand-voice file. If there is no file, ask: "Which time zone should I use for this client?" Never assume the agency's own zone.
- Convert to an ISO 8601 timestamp with the correct offset for that date, daylight saving included. If you have a code tool, let it do the maths:
  `python3 -c "from datetime import datetime; from zoneinfo import ZoneInfo; print(datetime(2026,11,20,18,0,tzinfo=ZoneInfo('Europe/Paris')).isoformat())"`
- The time must be in the future, or Inrō rejects it.
- If the date is vague ("Friday"), say which date you mean on the approval card.
- No time given and the brand file has posting windows: suggest the next window and say so.

## Step 6. Show the approval card and wait

Show this, filled in, and stop until the agency answers. A worked example is in `examples/approval-card.md`.

```
Client: @username (account id) | connected as @username
Action: Draft / Schedule for <day date time, client time zone> (<same moment in the agency's zone if different>) / Publish now
Type: Image / Carousel (n items, in this order) / Reel (Feed and Reels, or Reels only) / Story
Media: <file names>, checked: <format, size>
Caption (<n> of 2,200 characters, <n> hashtags):
<caption>
Alt text: <text>
Labels: AI-generated <yes/no> | Paid partnership <no / yes, with @brand> | Trial reel <no / yes>
Comment-to-DM: <none> or keyword <WORD> -> DM with a link card to <url>, created switched off
Note for the client's AI agent: <none> or <one line>
```

Then ask: "Approve as is, or tell me what to change." Edit and show the card again until it's a clear yes. If the brand file says the client signs off, the default is a **draft** the client can review in Inrō before it is scheduled.

## Step 7. Upload the media

Use `media_files_manage` with `action: create`. Pick the first method that works:

1. **The file has a link** (a direct download URL): pass `file_url`. Inrō downloads it. This is the most reliable.
2. **The file is on your machine and you have a shell with network access:** create with `media_type` and no `file_url`, then `PUT` the raw bytes to the returned `upload_url` with the file's `Content-Type`.
3. **Neither:** give the agency the returned `upload_page_url` and ask them to upload the file there.

Pass `purpose: publishing`. Then poll `media_files` `get` until `upload_status` is `ready` (or `failed`). If the link expired while still pending, use `refresh_upload` on the same id instead of creating a new file. For a carousel, upload every item and keep the ids in the approved order.

## Step 8. Create the post

- Feed post or reel: `medias_manage`, `action: create`, with `publish_media_type` (`IMAGE`, `REELS` or `CAROUSEL`), `media_file_id` (or `children` for a carousel), `caption`, `alt_text`, and either `scheduled_at` or `publish_now: true`. Leave both out for a draft.
- Story: `stories_manage`, `action: create`, with `media_file_id`, optional `user_tags`, and `scheduled_at` or `publish_now`.
- Labels that Instagram only accepts at creation go in now: `is_ai_generated`, `is_paid_partnership` with `branded_content_sponsors`, `trial_graduation_strategy` for a trial reel. They can't be added once the post is live.
- If the post is about an offer, price, date or stock, add `agent_context`: a short note the client's AI agent reads when someone asks about this post. It never shows on Instagram, and it can be changed later, even on a published post.

## Step 9. Pair it with a comment-to-DM automation (optional, recommended)

A post that asks people to comment a keyword should have the automation ready before it goes live. Two routes:

**Quick route, in the same call or right after.** Pass `comment_to_dm` on create, or call `medias_manage` `attach_comment_to_dm` with the post `id`:
- `comment_options`: `comment_type: comment_keywords` and `comment_keywords: ["KEYWORD"]` (matching ignores case and accents and works on whole words; a keyword of 4 or more letters also matches its plural, so RITUAL matches "rituals").
- `conversion_link`: the `url` to send, plus `title` and `button_title` if you want to set them. The DM sends it as a tappable link card.
- `question_type`: what the commenter does before getting the link (`button_template` a tap, `message` a reply, `ask_for_follow`, or `collect_property` their email).
- `active: false`. Always.

The public comment reply, the DM wording and the follow-up are copied from the client's most recent comment-to-DM automation, or from Inrō's defaults if there is none. So read it back before switching it on: `medias` `get` returns `comment_to_dm` with a `scenario_id`; open it with `show_scenario` and show the agency the reply and DM text. If the wording is wrong for this post, change it in Inrō (**Automation**, open the scenario) or with `dm-flow-builder`. The shortcut always adds a folder step and a Meta Pixel step under it; with no pixel set up, that step shows an issue ("No event selected"), which is harmless but worth mentioning. It also sets no run limit and leaves "stop when a person takes over" off, so add those with `dm-flow-builder` if the client needs them.

When the agency approves, switch it on: `attach_comment_to_dm` with the post `id` and `active: true`. It only targets this one post, from draft through publish.

**Full route.** For more than "comment, get a link" (email capture before the link, a booking, a hand-over to the AI agent, several steps), use the `dm-flow-builder` skill, or in Inrō **Automation > Scenarios > New scenario > Comment to DM link**. The post composer in Inrō also has a **Comment automation** step.

Grid posts made in the app can't carry a comment automation; add one to each tile after they're live.

## Step 10. Read back and report

- `publish_now` usually comes back `published` with a `permalink`: report the link and stop. Only `pending` (shown as "Processing" in the app) means Instagram is still working on a large video. Then poll `medias` `get` until `published`, or until `publish_status` is `ERROR`; on an error, report `login_error_data` in plain words.
- For a scheduled post, report the date and time in the client's zone, and that it stays editable until it goes out.
- For a draft, say where to find it: **Content > Posts & reels**, with a Draft badge. On a draft or scheduled post the text comes back in `publish_caption` and `publish_alt_text`; `caption` stays empty until the post is live.
- Say whether a comment-to-DM automation is attached, whether it is on, and its name in **Automation** (`comment_to_dm.title`, set by Inrō, for example "Specific post(s) - MENU").

## Changing what's already there

- **See the calendar:** `medias` `list` with `status: scheduled` (also `draft`, `pending`, `published`), and `stories` `list`. Show date, time in the client's zone, type and the caption's first line.
- **Edit a draft or scheduled post:** `medias_manage` `update` with the `id` and only the fields that change. Show the change first.
- **Reschedule:** `update` with a new future `scheduled_at`.
- **Back to draft:** `medias_manage` `update` with the `id` and `scheduled_at: ""`, then check that `status` is `draft`. In Inrō it's **Cancel scheduling** on the review step.
- **Publish a draft or scheduled post now:** `medias_manage` `publish` with the `id`, after the extra confirmation.
- **Published posts:** the content can't be edited. You can still change `agent_context` and the comment-to-DM automation, each in a call on its own.
- **Delete:** `medias_manage` or `stories_manage` `delete`, only on an explicit yes for that item, and warn first if it is published. Deleting a post doesn't delete its comment-to-DM automation or the link it created: delete the scenario too (`scenarios_manage` `delete` with `comment_to_dm.scenario_id`) and, if nothing else sends it, the link (`conversion_links_manage` `delete`).

## A week of posts for one client

Write every caption, then show one table (date and time, type, first line, keyword, action) plus the full captions below it. One yes covers the rows in that table only. Then upload and create one post at a time, reading each back, and report a final list with ids and statuses. If one fails, stop and report before doing the rest.

## What this skill doesn't do

- Cross-post to Facebook Pages or TikTok (not available in Inrō yet).
- Choose content strategy for the client. It writes for the post in front of it.
- Read post performance. Post insights are on the post's **Insights** tab in Inrō; a monthly view is the `monthly-client-report` skill's job.
