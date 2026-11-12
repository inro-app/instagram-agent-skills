# Choosing the three quickest wins

Read this before picking anything. The audit is only as good as what you leave out.

## The rule

**A play with no live entry point on this account is not a recommendation.**

An entry point is traffic that already exists: posts that get comments, stories that get replies, DMs arriving, a list already captured, ads already running. A play that needs the client to post more, run ads or build an audience first is a strategy conversation, not a quick win. It can go in the full setup, never in the top three.

Anyone can recommend icebreakers. Recommending them to an account that gets four DMs a week is how you lose the client's trust.

## The order

Work down this list and stop at three.

1. **Something they already own that is broken, switched off or unused.** A flow that converted and is off. An agent that answers nobody because its activation rules are wrong. An Instagram connection that dropped two weeks ago. A link nothing points at. These cost little to restore, the client can check them, and they prove you looked.
2. **Volume arriving now that nothing catches.** Comments on posts no flow covers. Story replies with no flow behind them. DMs with no answer. Size it: "312 people commented on your last 10 reels in 30 days, and no flow in Inrō answered them" is the argument.
3. **A capture gap on traffic that already converts.** The flow works, but it keeps only the Instagram handle: no email, no phone, no folder. The list is real but cannot be segmented or reached anywhere else. A small build on a flow that already works.
4. **A new flow on existing traffic.** A second keyword, an AI-detected intent next to a keyword, a follow step on a giveaway, a reply to story mentions.
5. **Anything that needs new content, new traffic or new spend.** Mention it in the full setup if it matters. Never a quick win.

## What each play needs before you can recommend it

If the condition is not true on this account, the play is not on the table.

| Play | Only if | Size it with |
|---|---|---|
| Reconnect Instagram | `login_error` is true or `instagram_connected` is false | how long it has been down, paused runs |
| Fix a broken flow | an active flow with issues, a trigger that cannot fire, or a step where most runs stop | its runs and failures in the window |
| Restore a switched-off flow | an inactive scenario with real past volume and conversions at or above the live ones | its own past runs and conversions |
| Fix the agent's activation | the agent is meant to reply and its mode or intents stop it | DMs received in the window with no reply |
| Comment-to-DM on uncovered posts | recent posts drawing comments that no active comment flow covers | commenters on those posts in 30 days |
| AI-detected intent next to a keyword | a keyword flow works and comments ask for the same thing in other words | how many such comments in what you read |
| Story replies | stories posted regularly **and** replies actually arriving | the reply count, never the story count |
| Story mentions | mentions arriving with no flow | mentions in 30 days |
| Icebreakers or an FAQ menu | DMs arrive and the same opening questions repeat | share of the conversation sample |
| AI agent on common questions | repeated questions in comments or DMs, and a website or price list to train it on | share of questions in the sample |
| Email or phone capture | contacts exist and almost none has an email or phone | contacts, and the share with email |
| Folders and segments | a few hundred contacts or more and most in no folder | that share |
| Follow step on a freebie or giveaway | a comment flow exists without one and growth is a stated goal | followers against contacts captured |
| Campaign to recent contacts | contacts active in the last few days and no recent campaign from Inrō | contacts active recently, not the total |
| Ads click-to-DM | contacts already arrive from ads, or the client says they run ads | contacts from ads in 30 days |

**A campaign only reaches people inside Instagram's messaging window.** Inrō's campaign templates describe it as people who messaged the account in the last 24 hours. A big list that has been quiet for months is not a campaign opportunity. Reopen those conversations through comments, stories or ads instead, and size any campaign on people active recently.

**A flow's later steps are not limited the same way.** A delay step can wait days, so a follow-up a week later is a real build. It reaches the people who are still in the conversation, and email carries it to the rest. Write "reaches people still active in the conversation", never "cannot be sent".

**For links, Inrō records taps, not page visits.** Write "did not tap the link", never "did not visit the page".

**Tags and exclusions can come from outside Inrō.** A webhook trigger or an integration can set a property or a folder, so customers or members can be kept out of every invitation automatically. Do not write that Inrō cannot see something until you have checked the triggers and integrations.

**A limit Instagram sets on reach is not a missing feature.** Before you write that Inrō cannot do something, check `get_trigger_types`, `get_action_types` and the help center.

## Sizing without promising

Anchor on their volume and their own rate, and say what it is:

> Your comment flow on the spring reels reached 1,240 people in the last 30 days and 380 of them tapped through, 31%. The version you switched off in August reached 900 people with 410 taps, 46%. On the volume you run now, that difference is roughly 185 more taps a month.

That is arithmetic on their numbers, labelled as arithmetic. It is not a forecast, and it survives someone checking it. Never write "this will double your leads". Do not quote industry or platform averages unless you have a current, citable source for them.

## Before you call something unused

A play chosen because "they have never done this" rests on a zero, and a zero only means Inrō has no record. Confirm the absence is real:

- a very fast first reply on most conversations (seconds), which means something automatic is answering;
- the same reply wording repeating across many conversations, typed outside Inrō (`sent_from: instagram`);
- public comment replies that no Inrō flow sent;
- bio links or captions that point to another DM or booking tool.

If something else is running, the play does not disappear, it changes shape. "Build this" becomes "move this where you can see it, segment it and follow it up", which is an easier conversation with a client who has already shown they want it. Note what you found in the internal notes, and never name or guess the other tool in the client document.

## What not to do

- Do not recommend every feature. Ten plays read as a brochure.
- Do not recommend the AI agent by default. It needs knowledge written before it is worth anything, and on an account with no repeated questions it solves nothing.
- Do not say who the commenters are or what they want without reading their comments. Launch-post comments are often congratulations from friends and family, not demand.
- Do not treat a burst of spam, an angry wave or the same handful of people commenting on everything as demand. Say the numbers neutrally and build nothing on them.
- Do not lead with what is broken. Lead with what is working, then the gaps.
- Do not put a play in the top three whose size you cannot state in their own numbers.
- Do not date a quick win "this week" if the account is not fully connected. "First" and "then" are enough.
- **Sensitive audiences** (health, mental health, finances, anything personal): do not segment people on a symptom or a hardship without their consent. Ask permission first, offer buttons taken from the client's own programmes, store no free text, and make sure the agent hands off to a person, with emergency contacts where they apply, before any other rule.

## The two tiers

### Quick wins: three, in order

"If we were setting up your account tomorrow, this is the order we would do it in." Chosen by the order above. Each one needs a number from the account.

One block per win:

```markdown
### 1. Answer the people commenting on your reels

**What we saw** 312 people commented on your last 10 reels (12 Oct to 11 Nov). No flow in Inrō covers those reels.
**What to do** One comment-to-DM flow on reels whose caption includes GUIDE: it asks for an email, then sends the guide. Built switched off; you switch it on.
**Effort** Small: one flow, one link.
**Template** Collect emails from audience, https://app.inro.social/public/scenarios/6022
**Next** dm-flow-builder
```

### The full setup: 10 to 15 rows, three groups

"If we were building the complete account, these are the systems we would put in." Each row is one line: the idea, what it does, and the benefit. No build detail.

- **Foundations.** Set up once, works for everything after: icebreakers, folders and segments, data capture (email, phone, and the two or three custom properties that matter for this business), the persistent menu, opt-out keywords, the account-wide exclusion filter, frequency limits.
- **Automations and campaigns.** The flows that carry volume: comment-to-DM with keyword and AI-detected intent, story replies, story mentions, lives if they go live, campaigns to recent contacts, launch or waitlist flows, booking flows, ad flows if they run ads, the hand-off flow behind the agent.
- **AI agent.** Always four rows: what it is trained on, which conversations it handles, what it captures, and when it hands off to a person. Each row names something from their account: their offer, their recurring questions, their qualifying details.

Every quick win also appears in the full setup. A row nobody could act on, or one the account has no traffic for, is filler and the reader can tell.

## Templates for common gaps

Find templates with `search_templates`, then open the share page before you suggest one. Use results that have a full description with "What it does", "What to set up" and a "Plan" line; skip entries with no description, which are older templates. "Add to My Inrō" on a share page imports an inactive, editable copy. Replace the template's link and any example values before switching it on.

Starting list (checked November 2026; names and the library change, so confirm with `search_templates`):

| Gap | Template | Share page |
|---|---|---|
| Commenters get nothing, and an email list is the goal | Collect emails from audience | https://app.inro.social/public/scenarios/6022 |
| Freebie or giveaway with no follow step | Grow followers with a freebie | https://app.inro.social/public/scenarios/6028 |
| Story replies with no flow | Story replies to link clicks | https://app.inro.social/public/scenarios/6023 |
| Story mentions with no flow | Like stories that mention you | https://app.inro.social/public/scenarios/6086 |
| Busy inbox, no agent | Handle DMs with AI | https://app.inro.social/public/scenarios/6085 |
| Leads to qualify and book | Qualify and book DM leads (AI) | https://app.inro.social/public/scenarios/6021 |
| Comments asking about calls or consultations | Book calls from comments | https://app.inro.social/public/scenarios/6025 |
| Ads already running | Book calls from your ads | https://app.inro.social/public/scenarios/6222 |
| A launch coming up | Build a launch waitlist | https://app.inro.social/public/scenarios/6081 |
| Hateful or spam comments | Hide hateful comments | https://app.inro.social/public/scenarios/6111 |
| Selling on lives | Send product links during lives | https://app.inro.social/public/scenarios/4393 |
| Offline customers (tables, flyers, packaging) | Welcome customers from a QR code | https://app.inro.social/public/scenarios/6019 |
| Recent contacts with no follow-up | Re-engage recent contacts (campaign) | https://app.inro.social/public/campaigns/21974 |
| Feedback wanted | Get audience feedback (campaign) | https://app.inro.social/public/campaigns/21978 |

The ad template needs an ad picked after import, and templates with an alert email step need an address. Suggest one template per gap at most.
