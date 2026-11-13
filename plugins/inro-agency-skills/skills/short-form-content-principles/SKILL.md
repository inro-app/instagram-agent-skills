---
name: short-form-content-principles
description: "How a short video holds a viewer, written for agencies scripting Instagram Reels for clients. Use it to plan, write, review or tighten a reel script, a hook, on-screen text or a caption, and to build a 'comment a keyword to get something' call to action that pairs with a comment-to-DM automation. Use when someone says 'write a reel script for my client', 'fix this hook', 'give me hook options', 'why does this reel lose people', 'turn this idea into a reel', 'tighten this script', 'add a comment to DM call to action' or 'review my client's reel before it goes out'. Works with nothing connected; pair it with client-post-scheduler or dm-flow-builder to put the post and its DM flow live."
license: MIT
---

# Short-form content principles

What goes on in a viewer's head while a reel plays, and how to write for it when the reel belongs to a client and should end in a DM conversation.

## Requirements

Nothing needs to be connected. This skill thinks and writes.

To put the result live: `client-post-scheduler` publishes or schedules the reel and can attach a simple comment-to-DM automation; `dm-flow-builder` builds a longer DM flow. Both need the Inrō connector (`https://api.inro.social/mcp`, one client on Pro (monthly or annual), a free trial, or a lifetime plan (free accounts are refused)) or the Inrō partner connector (`https://api.inro.social/partner/mcp`, partner token, client named on every call).

## How to work

- **Think about this reel, for this viewer.** These notes are things to reason with, not a fill-in template. A script that could be reused for a competitor by changing the logo is a sign you wrote from a pattern. Go back to the viewer.
- **The client sees the script, not the theory.** Don't name techniques in the deliverable or annotate lines with them.
- **Start from the client's brand-voice file** if the agency has one (the template ships with `client-post-scheduler`). Without it, ask four things before writing: who watches, what the client sells, the one thing this reel should get the viewer to do, and what the DM gives away.
- **Hand over scripts as beats:** the spoken line, the on-screen text, what we see, and a rough length in seconds so the editor has a target. Then the caption, the comment keyword and what the DM sends. `examples/reel-script-rewrite.md` shows a full before and after.

## Before writing: the viewer and the idea

**Write to a person you can describe.** "Women 30 to 55 interested in wellness" can't be written to. "A nurse coming off a night shift who wants to sleep but can't switch off" can. Decide who that one person is for this reel and write lines you'd say to her face.

**Let the details carry the targeting.** Rather than calling the viewer out ("Hey, night-shift nurses!"), show her world: the scrubs on the chair, the blackout blind at 9 a.m. People recognise themselves in a scene faster than in a label, and a label quietly tells everyone else to scroll on.

**Get the idea down to one plain sentence.** "Three things to stop doing before bed after a night shift." If the idea needs a paragraph, it's two reels or no reel yet.

**Know the payoff before the first line.** What does the viewer leave with, and what does the DM give them? A reel written backwards from its ending holds together; a reel written forwards from a topic drifts.

## The first seconds

**The viewer is doing a quick sum.** On first sight they guess how much this will give them and how long it will take, and they stay only if the answer looks like a good deal. Your opening should make the gain obvious and the time look short.

Ways to do that:
- Open on the result: the finished kitchen, the full appointment book, the plated dish, the before next to the after.
- Give the promise edges: "two changes", "one setting on your phone", "in the time it takes the kettle to boil".
- Begin at the moment of tension, not at the beginning of the story. If the reel is about a renovation disaster, open on the water on the floor.

**Hand over something real quickly.** The opening can promise, but a first piece of genuine value should land within the first few seconds: the tip, the surprising number, the reveal. A reel that spends its first five seconds on context has spent them.

There is a platform reason for this too. Instagram shows a new reel to a small group first and widens the audience if they keep watching and react to it. Instagram's head has named watch time, likes and sends (people sharing a reel by DM) among the strongest signals for reels. A weak start rarely gets a second audience.

**Testing openings for a client?** Publish one version as a trial reel: Instagram shows trial reels to non-followers first, so the client's followers don't see two near-identical posts. `client-post-scheduler` can set this when it schedules.

**Never let the opening write a cheque the reel can't cash.** Overpromise once and the viewer discounts every later opening from that account, and on a reel with a DM offer they stop commenting.

## The middle

**The viewer re-decides at every line.** An old copywriting rule says a first sentence exists to get the second one read. In a reel that decision repeats every couple of seconds. Read the script out loud, line by line, as a viewer who'd rather be elsewhere, and mark the first line where you'd swipe. Fix that line before touching anything after it; nothing past it will be heard.

**Make them wonder before you tell them.** Attention lasts while something is unresolved. Plant the question ("there's one setting almost every salon gets wrong") before giving the answer. When an answer lands, the next unanswered thing should already be in play, so the viewer never reaches a natural stopping point before your call to action.

- The wondering must happen in the viewer's head. A host reacting with surprise on screen doesn't make the viewer curious.
- Pay off what you set up. A tease that leads nowhere costs more than the views it bought.

**Swap summaries for things you can see.** Go through the script and circle every general word: "great", "fresh", "a lot", "recently", "many clients". Replace each with a number, a time, a name, a place or an object.

| Summary | Something you can see |
|---|---|
| "Our bread is baked fresh" | "This loaf was still dough at 4 a.m." |
| "A quick skincare routine" | "The two-minute routine I do in the car before school drop-off" |
| "Clients see great results" | "Week three is when Dana stopped needing the handrail" |
| "We help small businesses" | "A dental practice with one receptionist and a phone that never stops" |
| "Avoid costly renovation mistakes" | "The €400 tile mistake in every second bathroom we open up" |

Every concrete claim must be true and the client's to make: real figures, and customers who agreed to be named.

**Write for the ear, once.** Nobody scrubs back to decode a sentence. Short spoken sentences, everyday words, one idea per line. If the client's field has a term the viewer wouldn't use, either drop it or follow it straight away with plain words. Read the line to someone outside the industry; if they ask "meaning what?", rewrite it.

**Cut to the promise.** Ask of every line: does the viewer need this to get what the opening promised? A line that fails that test comes out, even the client's favourite. Usual suspects: "hi everyone, today I want to talk about", the brand intro, the origin story, the dead second while someone picks up a prop, the clever tangent. A reel is about one thing; everything else is drag.

**Answer the objection at the moment it forms.** Every reel prompts its own "yes, but". Work out which one this reel provokes and answer it in a short line right where it arises. In client work the usual ones are:

- "They're just selling to me." Start with the viewer's problem; let the business appear as the answer, later.
- "Fine for them, they have money and staff." Show the small, cheap version, or someone small doing it.
- "I'd never manage that." Show the first step only, done by someone like the viewer.
- "Heard it before." Say the specific thing this client does that others don't.
- "So what does it cost?" Say the price, or say exactly where to find it.

## Picture and sound

- **Script in beats so the edit has places to change.** Each new beat is a chance for a new angle, a close-up, a cutaway or a text card. A script that is one long paragraph produces one long shot.
- **Show what you're saying.** If the line is about a full appointment book, cut to the full appointment book. A face describing something the camera could show is the weakest choice.
- **Put the opening line on screen as text too.** Many people watch with sound off; the hook has to work silently.
- **Keep text away from the bottom and the right edge,** where Instagram lays the caption and the buttons.
- **Film it fresh for Instagram.** Instagram has said it favours original content in recommendations; a reel downloaded from another app with its watermark is a poor bet.
- Editing pace helps, but it can't rescue a script with nothing left to wonder about.

## The ending: a DM call to action

Most client reels should end in a conversation, not a like. "Comment a keyword to get something" turns a viewer into a DM thread the client's team or AI agent can work with. Patterns, example lines and pitfalls: `references/dm-call-to-action.md`.

- **One keyword per reel.** Short, easy to spell, tied to the payoff: MENU, PLAN, PRICES, QUOTE. Inrō's keyword matching ignores case and accents, so "menu" and "Menú" both count.
- **Say exactly what they get and where it arrives:** "Comment PLAN and I'll send you the four-week plan in your DMs."
- **Ask after the viewer has felt the value,** not in the opening line. Say it, show it on screen, and repeat it in the first line of the caption, before the "more" cut.
- **Promise what the DM really does.** If the DM first asks for a tap, a follow or an email, don't say "instantly".
- **Make it an offer, not a reach trick.** Instagram has said that using comments and DMs to talk to people and generate leads isn't engagement bait; asking for comments only to inflate numbers is.
- **Script and automation must match:** same keyword, same offer, same link, and the automation ready before the reel goes live. Hand the keyword and link to `client-post-scheduler` (comment, then a link card) or `dm-flow-builder` (email capture, booking, a hand-over to the AI agent).

## Writing for a client

- Their voice beats yours. Use their words from the brand-voice file.
- Every claim needs the client's OK and a fact behind it, more so in health, money, beauty and legal niches.
- Testimonials and named customers need consent.
- Paid partnerships carry Instagram's paid partnership label; photorealistic AI visuals carry the AI label. Both have to be set before publishing.
- Write lines the client can say naturally. A perfect line they stumble over on camera is a bad line.

## Reviewing a client's script

When the agency asks for a review rather than a rewrite:

1. Say the idea back in one sentence. If you can't, that is the first note.
2. Mark the first line where a viewer would leave, and why.
3. Circle the vague words and offer the concrete swap.
4. Check the payoff lands early and the call to action matches the DM.
5. Return the revised script, then at most five short notes on what changed and why. Keep the client's best lines.

## Keep it in proportion

None of this is law. If a reel ignores a point here and keeps people watching, it's right and the note is wrong. Judge on the client's numbers across several posts, not one. Platform details move often; the current ones, with sources, are in `references/instagram-reels-notes.md`.
