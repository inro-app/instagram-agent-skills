# Inrō templates to start from

The gallery changes, so treat this list as a map and confirm with `search_templates` (type `Scenario` or `Campaign`, with a plain query such as "story replies link" or "collect emails"). A result gives the template's `id`, title, description, setup notes and share link.

Every template has a public share page. Open it to see the flow, then **Use this automation** copies it into the account that is signed in, switched off. Through the connector, `scenarios_manage` create with `template_id` does the same for a scenario, and `campaigns_manage` create with `template_id` for a campaign. Both are writes, so show the plan and get the user's OK first (`SKILL.md`, sections 4 and 5), and follow recipe 1 in `recipes.md`.

Before any copy goes live: replace the link in its link step with the client's own, set the keyword and the posts it watches, point every folder step at one of the client's folders, fill any alert email, and read every message. Templates ship with example copy.

Plan notes: "Free" runs on any plan, "Pro" needs Pro or Trial, "AI credits" needs AI features on the account and uses credits.

## Automations (scenarios)

| Template | Starts from | What it does | Plan | Share page |
|---|---|---|---|---|
| Collect emails from audience | Comments with your keyword | Public reply, asks if they want the freebie, asks for their email, sends the link | Free | https://app.inro.social/public/scenarios/6022 |
| Grow followers with a freebie | Comments with your keyword | Followers get the link; others are asked to follow first | Free | https://app.inro.social/public/scenarios/6028 |
| Book calls from comments | Comments with your keyword | One question; ready people get the booking link and you get an alert, the rest a free resource | Free | https://app.inro.social/public/scenarios/6025 |
| Build a launch waitlist | Comments with your keyword | Adds them to a waitlist folder and asks for an email | Free | https://app.inro.social/public/scenarios/6081 |
| Run a tag-a-friend giveaway | Comments that tag someone | Asks for a follow, then an email, then confirms the entry | Free | https://app.inro.social/public/scenarios/6018 |
| Story replies to link clicks | Story replies with your keyword | Sends your link, one reminder if they do not open it | Free | https://app.inro.social/public/scenarios/6023 |
| Send product links during lives | Live comments with your keyword | DMs a button, then the product link | Pro | https://app.inro.social/public/scenarios/4393 |
| Book calls from your ads | Replies to a click-to-message ad | One question and an email, then the booking link or a lighter resource | Free | https://app.inro.social/public/scenarios/6222 |
| Welcome customers from a QR code | A scan of your QR code or ig.me link | Sends a welcome offer and code, files them in a folder | Free | https://app.inro.social/public/scenarios/6019 |
| Answer price questions in DMs | Comments asking about the price | Sends the price and the product link | Free | https://app.inro.social/public/scenarios/36436 |
| FAQ buttons in your DMs | People opening your DMs (ice breakers) | Answers common questions from buttons | Free | https://app.inro.social/public/scenarios/36428 |
| Recommend products with a quiz | Comments with your keyword | Asks two questions, then sends the right product | Free | https://app.inro.social/public/scenarios/36438 |
| Get bookings from DMs | DMs with your keyword | Sends your booking link | Free | https://app.inro.social/public/scenarios/36437 |
| Handle comments with AI | Comments on your posts | AI likes and replies to them | Pro and AI credits | https://app.inro.social/public/scenarios/36431 |
| Catch collab requests in DMs | Collab pitches in DMs | AI flags them and emails them to you | AI credits | https://app.inro.social/public/scenarios/36429 |
| Qualify and book DM leads (AI) | DMs with your keyword | AI judges the answer to one question; hot leads get the booking link and alert your team | Pro and AI credits | https://app.inro.social/public/scenarios/6021 |
| Handle DMs with AI | Questions in DMs or story replies | AI answers from the knowledge base; anything it cannot answer is filed for a person and emailed to your team | Pro and AI credits | https://app.inro.social/public/scenarios/6085 |
| Thank positive comments | Kind comments | Likes the comment and replies with a short thanks | Free | https://app.inro.social/public/scenarios/6082 |
| Auto-like positive messages | Kind DMs | AI spots them and likes them | AI credits | https://app.inro.social/public/scenarios/6223 |
| Like stories that mention you | Stories that mention the account | Likes the mention and files the person | Free | https://app.inro.social/public/scenarios/6086 |
| Hide hateful comments | Hateful comments | AI detects and hides them | Free | https://app.inro.social/public/scenarios/6111 |

Two built-in options sit in the **New scenario** window next to the templates: **Comment to DM link** (a step-by-step wizard for the most common flow: pick posts, filter comments, public reply, a question, the link, a follow-up) and **Comment moderation**. For a plain "comment a word, get the link" flow, the wizard is the starting point rather than a template.

## Campaigns

A campaign reaches people who wrote to the account in the last 24 hours. Pick the audience before sending.

| Template | What it does | Plan | Share page |
|---|---|---|---|
| Re-engage recent contacts | One short personal question to a group you pick; replies are liked and filed | Free | https://app.inro.social/public/campaigns/21974 |
| Ask contacts to follow you | A follow ask with a button to non-followers in a recent group | Free | https://app.inro.social/public/campaigns/21975 |
| Do a launch announcement | Launch message and link to your waitlist | Free | https://app.inro.social/public/campaigns/21976 |
| Send a voice note to contacts | Your own recorded voice note to people already chatting with you | Free | https://app.inro.social/public/campaigns/21977 |
| Get audience feedback | A two-question survey with one reminder | Free | https://app.inro.social/public/campaigns/21978 |

## Older templates

The gallery may still show a few older templates with Title Case names and a generic "Powered by Inrō" description. Prefer the ones above. If an older one is the only fit, read its whole flow before suggesting it.
