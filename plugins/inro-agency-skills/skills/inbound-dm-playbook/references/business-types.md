# The playbook by business type

Same map as SKILL.md section 2, with the order, entry points and guardrails that usually fit. Treat each as a starting proposal for the client, not a rule: their intake answers win.

Positions are in the **Inbound DMs** priority folder (1 is highest). Helpers (team hold, window timers, Human handover, likes) are the same for everyone.

## Coach or course creator

| # | Flow | Start from |
|---|---|---|
| 1 | Collab pitches | 36429 |
| 2 | Refunds and programme problems | Build (SKILL.md 3.2) |
| 3 | Qualify, then book a discovery call | 6021, keyword switched to an AI booking intent if needed |
| 4 | Which programme is right for me? | 36433 on an ice breaker and a menu entry |
| 5 | Questions about the programme | 6085 |
| 6 | First message | Build (SKILL.md 3.7) |

- **Ice breakers:** "How does it work?", "How much is it?", "Can we have a quick call?", "Can I talk to [first name]?"
- **Menu:** Book a call (link), Programmes (postback, reuses the plan picker's ice breaker payload), Free resource (link), opt-out.
- **Always a person:** health or medical questions, guarantees of results, refunds, payment plans the client hasn't published.
- **Agent:** Limit to instructions. A coach's audience asks personal questions; the agent shouldn't improvise advice.

## Online shop

| # | Flow | Start from |
|---|---|---|
| 1 | Collab and UGC pitches | 36429 |
| 2 | Order problems, returns, refunds | Build (SKILL.md 3.2), with "where did you order?" buttons if they sell on several channels |
| 3 | Ready to buy | 36432 |
| 4 | Price questions in DMs | Copy of 36436 with a DM trigger (SKILL.md 3.5) |
| 5 | Questions (sizes, shipping, materials) | 6085 |
| 6 | First message | Build |

- **Also:** 36436 for PRICE comments, 36438 product quiz for a range of products, 6019 QR welcome for packaging inserts.
- **Ice breakers:** "Where's my order?", "Do you ship to me?", "Which size should I get?", "Can I talk to someone?"
- **Menu:** Shop (link), Track my order (link to the client's tracking page, if they have one), Sizes (postback), opt-out.
- **Always a person:** refunds, damaged or missing orders, delivery promises, codes that don't work.
- **Opt-out keywords:** consider dropping the bare "stop" ("stop my order" would opt the customer out).
- **Live order data:** a connected Shopify store gives order triggers and product links. Plan that separately.

## Local business (salon, clinic, studio, restaurant)

| # | Flow | Start from |
|---|---|---|
| 1 | Cancellations, complaints, problems with a booking | Build (SKILL.md 3.2) |
| 2 | Book or check availability | 36437, with an AI booking intent and a "Book" ice breaker |
| 3 | Prices | 36433, or answers in 36428 |
| 4 | Questions (hours, location, parking, what to bring) | 6085, or 36428 for the top three |
| 5 | First message | Build |
| 6 | Collab pitches (lower: rare and low stakes here) | 36429 |

- **Ice breakers:** "How much is it?", "Can I book this week?", "Where are you?", "Can I talk to someone?" (36428 covers three of these in one scenario).
- **Menu:** Book (link to the booking tool), Prices (postback), Find us (link to the map), opt-out.
- **Helpers:** 6086 story mention likes matter here: customers tag venues often.
- **Always a person:** medical questions (clinics), allergies and dietary questions (restaurants), anything that promises a slot the booking tool hasn't confirmed.
- **Closures:** Time-off with the reopening date. Opening hours go in the agent's knowledge base so the AI front desk answers them.

## Service firm or B2B (agency, consultant, studio)

| # | Flow | Start from |
|---|---|---|
| 1 | Complaints and client issues | Build (SKILL.md 3.2) |
| 2 | Qualify, then book a call | 6021 with the fit description rewritten for the client's ideal customer |
| 3 | Partnership and vendor pitches | 36429, intent extended with "a vendor or tool selling to the business" |
| 4 | Questions about services | 6085 |
| 5 | First message | Build |

- **Prices:** usually "it depends, here's a call", not a number. Put that answer in the knowledge base and leave out price flows.
- **Ice breakers:** "What do you do?", "How much does it cost?", "Can we book a call?", "Can I see your work?"
- **Menu:** Book a call (link), Case studies (link), opt-out.
- **Always a person:** quotes, contracts, timelines, anything about an existing client project.

## Creator or personal brand

| # | Flow | Start from |
|---|---|---|
| 1 | Brand and collab pitches | 36429, with the client's media kit or management email in the holding reply |
| 2 | Questions about the client's products or links | 6085 or link flows from `dm-funnel-planner` |
| 3 | First message | Build, short |

- **Helpers carry most of the load:** 6223 likes kind messages, 6086 likes story mentions.
- **Human only:** friends, family, other creators the client talks to directly. Fill it on day one.
- **Agent:** strict voice rules, Limit to instructions, and the shortest message length. A fan who gets an off-voice reply notices.
- **Ice breakers:** what fans really ask ("Where's your [product] from?", "How do I work with you?"), not a sales menu.
