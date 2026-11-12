# AI intent library

Paste-ready texts for the **AI-detected intent** filter on "Someone sends you a DM" and "Someone replies to your story" (`content_filter: "ai_detected"`, text in `ai_intent`). Use the same text on both triggers of a flow.

Shape: one sentence of what fires, then "Not ..." naming the neighbours. Adapt the nouns to the client ("a class", "an order", "a session"), keep the structure. Texts marked **template** are the ones Inrō's templates ship with.

Test every intent in the app before switching on: open the trigger, use **Test intent detection** with 5 to 10 real messages from the client's inbox, including near misses from the neighbouring rows. Each near miss should fail. If one passes, add it to the "Not" list in the client's words and test again.

## 1. Collab and brand pitches (template, 36429)

```
A brand, agency or creator offers a collaboration, sponsorship, partnership, UGC deal or paid promotion. Not a customer question, an order, a compliment or a button reply.
```
Near misses to test: "do you do discounts for students?", "love your stuff, where can I buy it?", a customer asking for a refund.

## 2. Complaints, refunds and order problems

```
Complains, or asks for a refund, a cancellation or a return, or reports a problem with an order, a delivery, a charge or a booking they already made. Not a question before buying, a price question, a discount request, a collab pitch or a button reply.
```
Near misses: "how much is delivery?", "can I change my booking to Friday?" (decide with the client whether rescheduling is a booking or a person), "is it refundable if I don't like it?" (a pre-sale question: belongs to the AI front desk).

## 3. Bookings and availability

```
Wants to book, or asks about availability, free slots or the next possible time, in their own words. Not a cancellation or a complaint about a booking they already made, a price-only question, a collab pitch or a button reply.
```
Near misses: "I need to cancel tomorrow", "how much is a session?", "are you open on Sundays?" (hours: AI front desk, unless the client wants it to send the booking link).

## 4. Ready to buy (template, 36432)

```
Wants to buy, or asks where to buy, if it is in stock or how to order, in their own words. Not a button reply, a complaint, a return or a collab pitch.
```
Near misses: "my order hasn't arrived", "do you ship to Canada?" (a question: AI front desk), a brand asking to stock the product (a collab).

## 5. Prices, plans and packages

```
Asks what something costs, or about prices, plans, packages or payment options, in their own words. Not a refund or charge problem, a request for a discount code, a collab pitch or a button reply.
```
Near misses: "I was charged twice", "any promo code?", "is the first class free?" (decide with the client: often a price answer).

## 6. Discount codes (only if the client gives codes)

```
Explicitly asks for a discount, promo code, coupon, voucher or deal. Not a question about the normal price or whether something is free, a code that isn't working, a refund, or an affiliate or collab pitch.
```
Near misses: "how much is it?", "my code doesn't work" (a person), "can I be an ambassador?" (a collab). Rules for the flow: one code, never conditional, never invented.

## 7. General questions: the AI front desk (template, 6085)

```
Asks a question or for help in their own words about products, services, prices, hours, bookings or orders. Not a button reply, a collab pitch, a compliment or spam.
```
This one is wide on purpose. It sits low in the Inbound DMs folder so the specific flows above win. If the client has dedicated price or booking flows, they still win, because they are higher.

## 8. Kind messages (template, 6223, Helpers)

```
A kind message in their own words, such as thanks, a compliment or support, with no question or request. Not a button reply, a question, an order or a complaint.
```
Near misses: "love it! how much is it?" (has a question: should fail), "thanks, but it arrived broken" (a complaint).

## 9. Asks for a person (only for a scripted flow)

When the agent is talking, its own **Request a human** setting handles this. Use a flow only if the client wants a scripted answer outside agent conversations.

```
Asks to talk to a person, a human, the owner or someone from the team, in their own words. Not a question they want answered, a complaint about an order (that has its own flow), a collab pitch or a button reply.
```

## Writing new ones

- One intent per flow. If you need "and" twice, it is two flows.
- Name the neighbours in "Not", in the order of the Inbound DMs folder.
- "In their own words" plus "Not a button reply" keeps a flow from firing on ice breaker and menu taps that another flow answers.
- Broad intents like "asks a question" match nearly everything. Keep them for the last replying flow only.
- The agent's **Specific intents only** mode and its intent-based actions use the same kind of plain-language intent, but they are separate settings. Keep their wording consistent with the flows so the client's team sees one set of rules.
