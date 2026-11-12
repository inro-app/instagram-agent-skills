# Publishing reference

Call shapes, fields, formats and limits for posting through the Inrō connector. Every write tool takes `action` plus an `action_params` object. On the partner connector, add `"organization": <account id or username>` at the top level of every call, next to `action`.

Help center articles behind this page:
- Your Instagram content in Inrō: https://help.inro.social/en/articles/15631977
- Manage media files via the API: https://help.inro.social/en/articles/15586658
- Access your media posts via the public API: https://help.inro.social/en/articles/14963447
- Comment-to-DM: https://help.inro.social/en/articles/15632060
- Partner API and MCP: https://help.inro.social/en/articles/17027623

## 1. Check the account

```json
get_organization_info {}
```

Fields that matter here: `username`, `subscription_tier` (free, trial or pro), `can_publish`, `missing_publish_scopes`, `publishing_reauth_url`, `login_error_data`, `instagram_restrictions`.

If `instagram_restrictions` is not empty or `login_error_data` shows an error, tell the agency before scheduling anything: a post can't go out from a broken connection.

## 2. Upload the media (`media_files_manage`)

**From a link (preferred):**
```json
{ "action": "create", "action_params": { "file_url": "https://example.com/files/reel-final.mp4", "purpose": "publishing" } }
```
`media_type` is detected from the file. If it comes back wrong, the link is probably not serving the right `Content-Type`.

**From a local file:**
```json
{ "action": "create", "action_params": { "media_type": "video", "purpose": "publishing" } }
```
The response holds a pending `media_file` with `upload_url`, `upload_page_url` and `expires_at`. Then:
```bash
curl -X PUT -H "Content-Type: video/mp4" --data-binary @reel-final.mp4 "<upload_url>"
```
No auth header is needed for the PUT. If you can't run it, give the agency the `upload_page_url`; uploads there resume if the connection drops.

**Wait for it:** `media_files` `{ "action": "get", "action_params": { "id": 123 } }` until `upload_status` is `ready` or `failed`. Back off between polls.

**Expired link:** `{ "action": "refresh_upload", "action_params": { "id": 123 } }` mints a new link and keeps what was already uploaded. Don't create a second media file.

`media_type` values: `image`, `audio`, `video`, `application`, `text`. `purpose: publishing` tells Inrō the file is for a post; the file is stored as uploaded either way.

**Size limits:** images, audio and documents up to 25 MB, video up to 250 MB. Larger files are refused.

**File types Inrō accepts:** JPEG, PNG, GIF, WebP and AVIF images; MP4, MOV and WebM video. Inrō converts them to what Instagram needs.

## 3. Create a post (`medias_manage`)

**Image, scheduled:**
```json
{
  "action": "create",
  "action_params": {
    "publish_media_type": "IMAGE",
    "media_file_id": 123,
    "caption": "First line that earns the tap.\n\nSecond paragraph.\n\n#tagone #tagtwo #tagthree",
    "alt_text": "A baker lifting a tray of sourdough loaves out of a stone oven",
    "scheduled_at": "2026-11-20T18:00:00+01:00"
  }
}
```

**Carousel:** `"publish_media_type": "CAROUSEL"` and `"children": [123, 124, 125]`, 2 to 10 items, in order. The first item is the one people see in the feed.

**Reel:** `"publish_media_type": "REELS"` and `"media_file_id"` of the video. Optional:
- `share_to_feed`: `true` shows it in Feed and Reels, `false` Reels only.
- `cover_media_id`: an uploaded image for the cover, or `thumb_offset`: the frame to use, in milliseconds.
- `audio_name`: renames the original audio.
- `trial_graduation_strategy`: publish as a trial reel, shown only to non-followers at first. `MANUAL` (you graduate it in the Instagram app) or `SS_PERFORMANCE` (Instagram graduates it if it performs well). Reels only.

**Draft:** leave out both `scheduled_at` and `publish_now`.

**Publish now:** `"publish_now": true`. The call waits for Instagram, so it normally returns `status: "published"` with a `permalink`. Report that and don't poll. Only `pending` needs polling.

**Other fields (create and update):**

| Field | What it does | Limit or note |
|---|---|---|
| `caption` | Post caption, with @mentions and #hashtags | 2,200 characters in the Inrō composer |
| `alt_text` | Accessibility text | |
| `location_id` | Instagram location (page) id | Only if you have the id |
| `user_tags` | People tagged on the image: `{ "username": "...", "x": 0.5, "y": 0.5 }` | x and y from 0 to 1 on feed images |
| `collaborators` | Collab post invites, by username | Up to 3 |
| `is_ai_generated` | Instagram's AI label | Set before publishing. It can't be added later |
| `is_paid_partnership` | Instagram's "Paid partnership" label | Posts and reels, not stories. Set before publishing |
| `branded_content_sponsors` | Brands credited on the paid partnership | Up to 2; each must be a public Business or Creator account |
| `agent_context` | Notes for the client's AI agent about this post | Never shown on Instagram; editable any time. The app's field takes up to 5,000 characters |
| `comment_to_dm` | Attach a comment-to-DM automation in the same call | See section 5 |

## 4. Stories (`stories_manage`)

```json
{ "action": "create", "action_params": { "media_file_id": 130, "scheduled_at": "2026-11-21T09:30:00+01:00" } }
```
Fields: `media_file_id` (image or video), `user_tags`, `scheduled_at` or `publish_now`, `is_ai_generated`, `agent_context`. No caption. Stories can't carry the paid partnership label.

## 5. Comment-to-DM on a post

On create or update, as `comment_to_dm`:
```json
"comment_to_dm": {
  "comment_options": { "comment_type": "comment_keywords", "comment_keywords": ["MENU"] },
  "conversion_link": { "url": "https://example.com/menu", "title": "This week's menu", "button_title": "See the menu" },
  "question_type": "button_template",
  "active": false
}
```

On an existing post (draft, scheduled or published):
```json
{ "action": "attach_comment_to_dm", "action_params": { "id": 222, "comment_options": { "comment_type": "comment_keywords", "comment_keywords": ["MENU"] }, "conversion_link": { "url": "https://example.com/menu" }, "active": false } }
```

Switch it on after approval:
```json
{ "action": "attach_comment_to_dm", "action_params": { "id": 222, "active": true } }
```

- `comment_type`: `all_comments`, `comment_keywords` (needs `comment_keywords`), `ai_detected` (needs `ai_intent`, a plain-language description like "asking for the price"), `tag_someone`, `hate_spam`.
- `allow_replies`: also trigger on replies to comments (off by default). `exclude_negative`: skip comments an AI check reads as negative.
- `conversion_link`: either `id` of an existing link, or `url` for a new one. Title, subtitle and image default to the page's preview tags.
- `question_type`: `button_template`, `message`, `ask_for_follow`, `collect_property`.
- `active` defaults to **true** when left out. Always send `false` on creation.
- The link is required the first time; later calls can change only the filter, the question or `active`.
- Calling it again for the same post updates that automation; it doesn't create a second one.
- The other steps (public reply, DM text, follow-up, folder) are copied from the client's most recent comment-to-DM automation, or from Inrō's defaults. Read them back: `medias` `get` returns `comment_to_dm.scenario_id`; `show_scenario` with that id shows the flow, and `scenarios` `get` returns the full definition.

Instagram rules that shape the DM (from the help center): one private reply per comment, sent within 7 days of the comment; the contact has to reply or tap before more messages go through; people who don't follow the account get the DM in message requests. A tappable link card is the reliable way to send a link.

## 6. Read, change, remove

| Need | Call |
|---|---|
| List posts | `medias` `list` with `status` (`published`, `scheduled`, `draft`, `pending`), `search`, `page`, `per_page` (up to 100) |
| One post, with its automation | `medias` `get` with `id` |
| Stories | `stories` `list` / `get` |
| Edit a draft or scheduled post | `medias_manage` `update` with `id` and changed fields |
| Reschedule | `update` with a new future `scheduled_at` |
| Publish now | `medias_manage` `publish` with `id` |
| Delete | `medias_manage` `delete` with `id`. Deleting a published post also removes it from Instagram |

A published post only accepts an `update` whose fields are `comment_to_dm` and/or `agent_context`. Anything else is refused.

## 7. Statuses and errors

| You see | Meaning | Do |
|---|---|---|
| `status: draft` | Saved, no time set | Nothing goes out |
| `status: scheduled` | Has a future `scheduled_at` | Goes out at that time; still editable |
| `status: pending` | Instagram is processing (app shows "Processing") | Poll `medias` `get` |
| `status: published` | Live; `permalink` and `instagram_id` set | Report the link |
| `publish_status: ERROR` | Instagram refused it | Read `login_error_data`, explain, fix, ask before retrying |
| "scheduled_at must be a valid future timestamp" | Past time or bad format | Recompute with the offset |
| Publishing permission error with a reauth link | `can_publish` is false | Send the client the link; save as draft meanwhile |
| "A published media cannot be edited" | Tried to change a live post | Only `agent_context` and `comment_to_dm` can change |

## 8. Instagram's own rules

- **Hashtags:** up to 5 per post or reel. Instagram moved to this limit from December 2025, rolled out gradually.
- **Feed image shape:** between 4:5 portrait and 1.91:1 landscape. Reels and stories are vertical, 9:16.
- **Carousel:** 2 to 10 images or videos.
- **Labels set at publish time only:** AI label, paid partnership, trial reel. Instagram gives no way to add them to a live post.
- **Publishing volume:** Instagram caps how many posts one account can publish through the API in 24 hours. A normal client calendar won't reach it.

## 9. In the Inrō app

- **Content** in the left sidebar, tabs **Posts & reels** and **Stories**. Status filter: All posts, Published, Scheduled, Draft, Processing.
- The New post composer runs **Select media > Caption & tags > Comment automation > Options > Review**, and the review step offers **Publish now** or **Schedule for later**. It offers Image, Reel, Carousel and Grid (a picture split into tiles, posted about 20 seconds apart). Grid is app only.
- The publishing tiles and filters only appear when the account can publish.
- A post's detail view has an **Automation** tab (attach or review a comment-to-DM) and an **AI Agent** tab (the `agent_context` note).
