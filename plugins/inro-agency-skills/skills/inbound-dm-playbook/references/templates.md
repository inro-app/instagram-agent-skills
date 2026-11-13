# Templates for inbound DMs

Every template here imports as an **inactive** copy. Connector: `scenarios_manage` `create` with `template_id: <id>` and, optionally, a `title`. This works for every id below, including the newest ones (36428 to 36438), which aren't in the template library yet, so `search_templates` doesn't return them. Share page: `https://app.inro.social/public/scenarios/<id>` (works logged out, with a **Use this automation** button), also for every id below. If a name has changed, the id still works.

What happens on import:
- Links are copied into the client's account as their own link records. Replace each URL.
- Folders are matched by exact name in the client's account and created when missing. Use the folder names from `client-account-setup` (baseline B1) so they line up.
- Alert emails arrive with no recipient. That shows as the issue "Email address is empty" until you add the client's address. Send the step's whole `options` with the address in it: options are replaced, not merged, so a partial update wipes the subject and body.
- Ice breaker triggers point at ice breakers on the template's own profile, and show the issue "The ice breaker this trigger answers is no longer on your Instagram profile." Create the client's ice breakers and point each trigger at the new payload.
- A trigger on the next post watches the first post published after the import, not after go-live. Import it close to that post, or switch the trigger to chosen posts.
- Run limits and "Interrupt when you reply manually" come with the template (listed below). Excluded folders don't: set them after import with `scenarios_manage` `update` and `excluded_folder_ids`, or in the app (`SKILL.md`, section 8, step 5).

## The core inbound set

### 36429 · Catch collab requests in DMs
- **Starts from:** Someone sends you a DM, AI-detected intent: "A brand, agency or creator offers a collaboration, sponsorship, partnership, UGC deal or paid promotion. Not a customer question, an order, a compliment or a button reply."
- **Steps:** add to "Collabs: requested" → alert email (subject "Collab request: @username") → wait 5 seconds → "Thanks for reaching out! It's with the team now, and you'll hear back here if it's a fit."
- **Defaults:** once every 7 days per contact; interrupt on manual reply on.
- **Set after import:** alert address; holding reply in the client's voice; add the Collab window (7d) steps if other flows could misfire on follow-ups.
- **Needs:** AI credits.

### 6085 · Handle DMs with AI
- **Starts from:** Someone sends you a DM, AI-detected intent: "Asks a question or for help in their own words about products, services, prices, hours, bookings or orders. Not a button reply, a collab pitch, a compliment or spam."
- **Steps:** hand over to the AI agent (24 hours) with the task: answer from the knowledge base in one or two short messages, one question back at most; done only when they have their answer or link; if the answer isn't there, or they ask for a person, say the team will reply here (which doesn't complete the task). Task completed → "Front desk: resolved". Handover expired → alert email with the first and latest message → "Needs a human".
- **Defaults:** once a day per contact; interrupt on manual reply on.
- **Set after import:** alert address. The agent's knowledge, voice and rules (`instagram-ai-agent-setup`). Narrow the intent if the client has dedicated flows for prices or bookings.
- **Needs:** Pro and AI credits. The agent's activation rules must not be **Disable all replies**.

### 36437 · Get bookings from DMs
- **Starts from:** Someone sends you a DM with the keyword RESERVE.
- **Steps:** "You can pick a time and book here." → booking link card (waits 2 hours) → clicked: "Bookings: clicked"; not clicked: "Have you checked the link yet?"
- **Defaults:** once an hour per contact; interrupt on manual reply on.
- **Set after import:** the booking URL; the keyword, or switch to an AI-detected booking intent (`intent-library.md`); add an ice breaker or menu trigger for "Book".
- **Needs:** nothing extra.

### 6021 · Qualify and book DM leads (AI)
- **Starts from:** Someone sends you a DM with a keyword (default COACHME).
- **Steps:** "Thanks for your message! What would you like help with?" → wait for reply (20 hours) → AI condition (wants to start soon, asks about price, availability or a call, or describes a problem the offer solves) → true: hot-lead folder, alert email, booking link with one reminder; false: cold-lead folder and a free resource link.
- **Defaults:** once every 7 days per contact; interrupt on manual reply on.
- **Set after import:** the keyword or an AI intent; the fit description in the AI condition; both links; alert address; rename the two folders to the client's offer.
- **Needs:** Pro and AI credits.

### 36432 · Shop link to ready buyers (AI)
- **Starts from:** Someone sends you a DM, AI-detected intent: "Wants to buy, or asks where to buy, if it is in stock or how to order, in their own words. Not a button reply, a complaint, a return or a collab pitch."
- **Steps:** "Here's where you can order. Any questions about sizes or delivery, just reply here." → shop link card (2 hours) → clicked: "Shop: clicked"; not clicked: "No rush, the link is just above."
- **Defaults:** once a day per contact; interrupt on manual reply on.
- **Set after import:** the shop URL; product words in the intent.
- **Needs:** AI credits.

### 36433 · Help people choose a product
- **Starts from:** an ice breaker, "Which plan is right for me?"
- **Steps:** "Happy to help. Which sounds most like you?" with three options (waits 20 hours; a typed reply that matches no option gets "Just tap one of the options below.") → each option sends its own link card → clicked: "Plans: clicked".
- **Defaults:** no run limit; interrupt on manual reply on.
- **Set after import:** the client's ice breaker (and a menu entry reusing its payload); the option labels and a link per option; the link behind the third option, "Not sure yet" (it ships with a call link).
- **Needs:** nothing extra.

### 36436 · Answer price questions in DMs
- **Starts from:** comments with the keyword PRICE on the next post.
- **Steps:** public reply under the comment ("Details are in your DMs" and variants) → DM with the price and two buttons, "Send the link" and "Chat on WhatsApp" (waits 6 hours) → each sends its link card → clicked: "Prices: clicked"; one reminder on the first link.
- **Defaults:** once per contact; interrupt on manual reply on.
- **Set after import:** the price line (the template's example price is a placeholder), both URLs, which posts to watch.
- **For DM price questions:** import a second copy, delete the public reply step ("Delete only this action" in the app), and give the copy a DM trigger with the price intent. Through the connector: `scenarios_manage` `update` with the full actions list minus the reply step and `parent_id: null` on the DM step that followed it, and a triggers list with no ids holding the one DM trigger (that replaces the comment trigger).
- **Needs:** nothing extra.

### 36428 · FAQ buttons in your DMs
- **Starts from:** three ice breakers ("Tell me more about your pricing", "What's your availability this week?", "Can I talk to a person?").
- **Steps:** condition on the tapped text: contains "pricing" → the price answer, "FAQ: asked about prices"; contains "availability" → the availability answer and a booking link card, clicked: "FAQ: opened booking link"; anything else → "Of course. Someone from the team will reply here soon." → alert email → "Needs a human".
- **Defaults:** no run limit; interrupt on manual reply on.
- **Set after import:** the client's ice breakers and payloads; **the condition values, so they match words in the client's questions**; the answers (the template's prices are placeholders); booking URL; alert address.
- **Needs:** nothing extra.

### 6223 · Auto-like positive messages (Helpers)
- **Starts from:** Someone sends you a DM, AI-detected intent: "A kind message in their own words, such as thanks, a compliment or support, with no question or request. Not a button reply, a question, an order or a complaint."
- **Steps:** wait 1 minute → like the message → "Thanks: praised us".
- **Defaults:** once a day per contact; interrupt on manual reply off (turn it on).
- **Set after import:** move to Helpers; exclude Human only and Team hold (24h).
- **Needs:** AI credits.

### 6086 · Like stories that mention you (Helpers)
- **Starts from:** Someone mentions you in a story (any story).
- **Steps:** wait 1 minute → like → "Thanks: mentioned us".
- **Defaults:** once a day per contact; interrupt on manual reply off (turn it on).
- **Set after import:** move to Helpers; exclude Human only and Team hold (24h); consider a longer wait so the like doesn't look instant.
- **Needs:** nothing extra.

## Templates that feed the inbox (plan them with `dm-funnel-planner`)

| Id | Name | Starts from | What it does |
|---|---|---|---|
| 6023 | Story replies to link clicks | Replies to a story | DMs the link, one reminder |
| 6022 | Collect emails from audience | Comments with a keyword | Asks for an email, then sends the freebie |
| 36430 | Detect intent & send links (AI) | Comments asking for the link, no keyword | AI spots them and DMs the link |
| 36438 | Recommend products with a quiz | Comments with a keyword | Two questions, then the matching product link |
| 36434 | Segment audience by interest | Comments with a keyword | One question, a folder per answer |
| 6025 | Book calls from comments | Comments with a keyword | One question, then the booking link |
| 6222 | Book calls from your ads | Click-to-message ads | Qualifies, then sends the booking link |
| 6019 | Welcome customers from a QR code | A scan of the client's QR code | DMs a welcome offer and files the person |
| 36431 | Handle comments with AI | Comments on the next post | AI likes and replies publicly |

Help: templates https://help.inro.social/en/articles/11968052 · triggers https://help.inro.social/en/articles/10267476 · AI intent filters https://help.inro.social/en/articles/15632169
