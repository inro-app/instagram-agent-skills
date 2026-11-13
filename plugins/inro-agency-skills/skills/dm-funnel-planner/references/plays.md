# Plays: what each needs, how to size it, what to start from

Check the "Only if" column against the account. If it is not true, the play is out of the quick wins, whatever the client's hopes. Template names are the in-app gallery names; links and setup notes are in `templates.md`. Check with `search_templates` before naming one, because the gallery changes. If search does not return a template, open its share page before you drop it: some valid templates are missing from search.

## Fix or restore (rank 1)

| Play | Only if | Size it with | Start from |
|---|---|---|---|
| Reconnect Instagram | `login_error` is true | How long it has been down, runs paused (`executions` health) | The client reconnects in Inrō. Nothing else runs until then. |
| Switch a working flow back on | An inactive scenario had real runs and clicks before | Its own past runs and clicks (`scenarios` performance, up to 90 days back) | The existing scenario: review its copy and link, then reactivate |
| Fix a failing flow | `executions` health shows one flow failing often | Its failed runs and the step they fail on | `dm-flow-builder`, section on fixing |
| Answer dead ice breakers or menu entries | An ice breaker or `postback` menu entry starts no automation | People who wrote for the first time in the window (`first_interaction`) | A small scenario per ice breaker, see "Ice breakers" below |
| Stop two flows colliding | Two active flows match the same comment or DM | Contacts who got both | A priority scenario folder, or narrower triggers |

## Catch volume that is arriving now (rank 2)

| Play | Only if | Size it with | Start from |
|---|---|---|---|
| Comment to DM with a link | Posts get comments that no active comment trigger covers | People who commented on uncovered posts in the window | The **Comment to DM link** wizard, or for one post the one-call shortcut in `dm-flow-builder`. Templates: Collect emails from audience, Grow followers with a freebie, Book calls from comments, Get event sign-ups, Build a launch waitlist |
| Comment to DM without a keyword (AI intent) | A keyword flow exists and people ask in their own words ("how do I get this?") | Comments that ask for the thing without the keyword, from a sample | Add a second comment trigger with an AI-detected intent to the existing flow. Pro and AI credits |
| Story replies to a link | People reply to stories (count repliers, not stories) | People who replied to a story in the window | Template: Story replies to link clicks |
| DM keyword answers | The same question arrives by DM again and again | People whose DMs contain that question in the window | A keyword DM flow (custom), or template: Qualify and book DM leads (AI) for booking-led clients |
| AI answers in DMs | Repeated questions in DMs or comments, and a website, price list or FAQ to train on | People who DM'd in the window, and the share asking the top questions | Template: Handle DMs with AI. Setup belongs to `instagram-ai-agent-setup`. Pro and AI credits |
| Ice breakers | People start new conversations with the account, and the same openers repeat in a sample | `first_interaction` in the window | Up to 4 ice breakers, each with a scenario behind it |
| Live comment links | The client goes live and sells or teaches on lives | Ask the client how often, and how many comment | Template: Send product links during lives. Pro |
| Ad replies | `referral_ad` contacts above zero | People who arrived from ads in the window | Template: Book calls from your ads (pick the ad in the trigger) |
| QR or link in the real world | The client has a shop, venue, packaging or events | Ask the client where the code would go | Template: Welcome customers from a QR code |
| Story mention thanks | People mention the client in their stories | `story_mention` in the window | Template: Like stories that mention you |

## Capture what already converts (rank 3)

| Play | Only if | Size it with | Start from |
|---|---|---|---|
| Ask for an email or phone | A flow sends a link, and few contacts have an email | Contacts with an email against total contacts; runs on the link flow | Add an **Ask for information** step (email) before the link, or template: Collect emails from audience |
| Tag who did what | Flows run but nothing is filed in a folder | Runs on those flows | Add a folder step on the clicked branch of the link |
| Segment by interest | The client sells more than one thing, and a flow already gets volume | Runs on that flow | One question with a button per interest, each answer to its own folder |

## New flow on existing traffic (rank 4)

| Play | Only if | Size it with | Start from |
|---|---|---|---|
| Follow before the freebie | A comment flow exists and the client wants followers | Commenters against followers among contacts (`is_follower`) | Template: Grow followers with a freebie |
| Tag-a-friend giveaway | The client runs or plans a giveaway | Ask for the giveaway post and dates | Template: Run a tag-a-friend giveaway |
| Thank kind comments | Comment volume is high and replies are few | People who commented in the window | Template: Thank positive comments |
| Like kind DMs | DM volume is high and many are praise | DMs in the window, a sample read | Template: Auto-like positive messages (AI credits) |
| Hide hateful comments | A sample shows abusive or spam comments | Share of the sample that is abusive | Template: Hide hateful comments, or the **Comment moderation** option in the New scenario window |

## Campaigns (sent by you, not triggered)

A campaign reaches only people who can receive a DM right now: active contacts who wrote to the account in the last 24 hours. A message to someone outside that window is held, retried, and dropped if they do not write again within a day. So:

| Play | Only if | Size it with | Start from |
|---|---|---|---|
| Launch announcement to a waitlist | A waitlist folder exists and people joined it recently | Folder members active in the last day | Campaign template: Do a launch announcement |
| Check-in with recent contacts | Many people wrote in the last day (after a viral post, a live, a giveaway) | `any_engagement` in the last 1 day | Campaign template: Re-engage recent contacts |
| Ask recent contacts to follow | Many recent contacts do not follow | Recent contacts with `is_follower` false | Campaign template: Ask contacts to follow you |
| Voice note | The client sells on trust and has recent conversations | Recent contacts | Campaign template: Send a voice note to contacts |
| Quick survey | The client wants feedback from recent contacts | Recent contacts | Campaign template: Get audience feedback |

"Win back a cold list" is not a DM campaign: people who have not written for weeks cannot be reached by DM. Move that idea to email, or to a new post or story that gives them a reason to write again.

For a message that repeats on a schedule for a filtered audience (a weekly check-in), a scenario with the recurring schedule trigger is the tool, not a campaign. Pro.

## Needs new content, ads or audience first (rank 5)

Keep these out of the quick wins. List them in the fuller funnel with what they need: "Comment to DM on the next reel: needs a reel that asks people to comment a word", "Ad replies: needs a click-to-message ad".

## What not to recommend

- Every feature. Ten plays reads as a brochure.
- The AI agent by default. It is only worth it when there are repeated questions and something to train it on.
- A play you cannot size in this account's own numbers.
- A play that contradicts the client's limits. A booking link flow next to a rule that the brand never pushes calls is a conflict to resolve first.
- Anything that asks health questions or other sensitive data without consent. If a flow must ask, ask permission first, offer buttons rather than free text, and store as little as possible.
