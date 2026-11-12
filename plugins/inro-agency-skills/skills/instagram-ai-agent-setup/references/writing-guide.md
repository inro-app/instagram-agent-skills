# Writing guide: each field, the knowledge base, guardrails

How to write an agent that sounds like the client and stays inside the lines. Field names and limits are in `fields-and-connector.md`.

## About (500 characters)

The one description that is in every prompt. Accounts set up by hand often leave it thin while the same facts sit in a knowledge item that may never be retrieved. Fill it.

- Write in the client's own voice ("We make...", "I coach..."): what they are, what they offer, who they serve, where.
- Add the one or two facts that change most answers: online or local, booking needed, ships where.
- No rules here, and no sales lines. Rules go in Instructions.

Example: "We're a two-chair barbershop in Leeds city centre. Cuts, fades and beard trims for men and boys, walk-ins welcome, bookings online. Most of our clients are regulars who work nearby."

## Goal (500 characters)

What a conversation the agent handles on its own should move toward. It is read on every such message, including "hi", so test every draft against three traps:

- **Platform features dressed as goals.** "Reply fast to every DM" is the automation firing, not something the agent can try harder at. Cut it.
- **Bans in the goal.** "Never quote a price" is a rule. Put it in Instructions.
- **Funnel goals that leak.** "Qualify leads for the mentoring program" makes the agent treat every greeting as a lead. Write the neutral version ("Find out what they need, answer it, and when it fits, offer to book a free call") and put funnel-specific moves in the task of the automation that runs that funnel.

Write it as something a person could actually do in a chat.

## Instructions (one sentence each, 300 characters, up to 50)

What the agent must or must not say or do. They apply to every reply, including automations and comment replies, and they outrank the knowledge base. This is where every hard rule lives.

Good contents:

- How to handle a bare greeting.
- What to find out, and how: one question at a time, never as a form.
- What to offer and how often (a link once, not every message).
- The banned moves: prices, quotes, discounts, delivery dates, guarantees, refunds, bookings it cannot make, anything about other customers.
- When to pass the conversation to a person.
- The honest answer to "are you a bot?".

Rules that make Instructions work:

- **Script first, ban second.** "If someone asks the price, say it depends on the project and offer the price guide" beats "Never quote a price". A list of twenty "never" lines produces stiff, clipped replies even when no rule is broken.
- **One rule per line, said once.** If a rule is also in a knowledge item, delete one of them.
- **No rules about tone here.** Those are Voice rules.
- **No references to things the agent cannot see.** "Use the usual script" means nothing unless the script is in the rule.

## Voice rules (one sentence each, 300 characters, up to 50)

How it writes, and nothing else. Derive them from the client's real messages, not from adjectives.

1. Gather 15 to 30 messages the client actually sent in DMs.
2. Count before you write: average length, how they open, how they sign off, punctuation, emoji (which ones, how often), exclamation marks, recurring words, formal or informal address.
3. Write rules that match the data: "Open with the person's first name when you know it", "At most one emoji, usually at the end", "No exclamation marks".

Two rules catch most mistakes:

- **Never define the voice by a reference the agent has never seen.** "Write like I text, not like I email" means nothing to it. Describe the output: "Short, casual, first person, the way people type DMs on a phone."
- **Write as the account, in the first person.** The agent speaks as the client. The only exception is escalation: the person it hands to is real ("I'll pass this to the team").

Usually worth having: one question at most per message, mirror their formality, match their language, never repeat a line word for word, a short list of filler phrases to avoid. Once the agent has voice rules or message examples, it is also told to avoid the most common AI-sounding words and dashes, so you don't need to list those.

## Message examples

Always in the prompt, which makes them the strongest single lever on voice.

- 10 to 20, one or two lines each, the way people type on Instagram.
- Spread across situations: an opener, a short acknowledgement, a casual personal answer, a real on-topic answer, the commercial line, a polite no, a handoff. Four examples that are all openers teach exactly one move.
- Take them word for word from the client's real messages where possible. Drop any that break the client's own rules, even if they wrote them.
- Paste only the message, not the conversation around it.
- Examples and Voice rules must agree. When they contradict, the agent leans unpredictably to one side.

## Message length (10, 25 or 50 words)

Count, don't guess. Take the client's approved answer to their most common question and count its words. Pick the setting it fits. If the client writes in short bursts, pick Short even if some answers run longer; the agent can split a reply into a few short messages. AI steps in automations set their own length.

## Knowledge base

### Split by what people ask, not by topic

"How much is it" and "can we get on a call" are different questions that need different stock answers, even though both are commercial. A merged item comes back for both and dilutes each. One item per question family.

### Open every item with what it covers

```
PRICING

Covers: how much things cost, rates, quotes, budget questions, asking for a number.

<the content, written the way the client would say it>
```

The header is what lets the search land on the question's intent instead of a stray word. Use the same convention on every item of the account.

### Keep each item self-contained

- **No cross-references.** "See the shipping item" is useless when that item was not retrieved. Restate what is needed.
- **Local rules stay local.** A capability fact ("I can't open links") or a phrase list for one situation belongs in the one item it applies to.
- **No "hard rules" banner on every item.** A line like "this applies even if this note wasn't retrieved" can only be read when it was retrieved. Global rules go in Instructions.
- **As long as the content needs, and no longer.** An item running to several thousand characters is usually covering more than one kind of question. Split it.
- **Write it the way the client talks.** The agent mirrors the tone of what it reads. A conversational FAQ produces conversational replies.
- **One language is enough.** The agent reads knowledge in the language it is written in and replies in the contact's language.
- **Strip notes meant for the agency** before importing a client document.

### Choosing the source

- **Manual text** is the most reliable for anything the agent must get exactly right. Up to 5,000 characters per item in the app.
- **Website** is the fastest start for a good FAQ or services page. Turn on "Automatically find other pages on this website" only for a small, clean site; a big site pulls in pages you don't want.
- **Text document** (.txt, .pdf, .doc, .docx) is upload-only in the app. A scanned PDF with no real text fails; paste the text instead.
- **Post and story notes.** For a post people ask about (price, stock, sizes, dates), add notes in the post's **AI Agent** tab or through `agent_context`. They are used when the conversation started from that post or story, which beats a general knowledge item.

## Guardrails

### The layers, from strongest to weakest

1. **Instructions:** always present, outrank everything else.
2. **Limit to instructions:** the agent says it doesn't know rather than guessing, and the cannot-reply scenario runs.
3. **Intent actions to the escalation scenario:** the agent recognises the situation and starts a flow that tells the team.
4. **Human intervention:** a contact who asks the agent for a person is handed to the team.
5. **Folder exclusion:** once escalated, the agent stays out of that contact's DMs.
6. **Knowledge:** a second layer for detail, never the only place a rule lives.

### Sample instructions to adapt

Adjust the wording to the client's voice. Each is one rule.

- "If someone asks about price, say it depends on what they need and offer to send the price list."
- "Never confirm a delivery date or stock level. Say you'll check with the team and pass the conversation on."
- "Never promise a refund, exchange or discount. Say the team handles those and pass the conversation on."
- "If asked whether you are a person, say you are the account's automated assistant and offer to pass them to someone on the team."
- "Never give medical, legal or financial advice. Share general information from what you know and suggest they speak to a professional."
- "If someone describes an emergency or says they are in danger, tell them to contact local emergency services right away, then pass the conversation to the team."
- "Never ask for card numbers, passwords, ID documents or health details."
- "Never discuss other customers or share anyone's details."
- "Never compare the business with competitors or comment on them."
- "If someone is angry or reports a problem, apologise once, ask for the order or booking details, and pass the conversation to the team."

### Sensitive verticals

Health, beauty and wellness clinics, finance, legal, and anything for minors need a narrower agent:

- Use **Limit to instructions**.
- Prefer **Automation only** or **Specific intents only** with a few clear intents.
- Route symptoms, outcomes, complaints and anything personal to the team with an intent action.
- Don't collect sensitive data through User data collection.
- Have the client approve the Instructions list in writing before go-live.

### Contact property descriptions for data collection

The agent fills a property only while it is empty, so the first value sticks. Write each custom property's description for precision:

- State what qualifies, in the contact's own words.
- State the near misses that don't qualify (someone else's company, a link to an article, a job title guessed from tone).
- End with: leave it empty rather than guess.

Never add a catch-all choice ("Other", "Unclear") to a choice property: it gets written on first contact and blocks the real value. Avoid two properties that could take the same answer (Company and Brand): the answer lands in whichever fires first.

## Failure modes to watch for

- A Goal written as conversion behaviour, leaking into neutral chats.
- The same rule in Instructions, Voice rules and a knowledge item, drifting apart.
- Instructions that mention material the agent has never seen.
- "The newsletter" in a rule when the newsletter item may not be retrieved. "My newsletter, which goes out every Sunday" works on its own.
- Escalation wording ("I'll pass this on") with no scenario connected behind it.
- A choice property with a placeholder option.
- An always-included knowledge item that duplicates the Instructions.
- The client editing the agent while you work. Re-read with `get` before every write.
