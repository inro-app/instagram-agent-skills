# The "comment a keyword" call to action

How to write the ask at the end of a client's reel so it starts a DM conversation, and how it has to line up with the comment-to-DM automation behind it.

## What happens after someone comments

These are Instagram's rules, as Inrō's help center describes them (https://help.inro.social/en/articles/10456326 and https://help.inro.social/en/articles/15632060):

- The automation can reply to the comment in public and send the commenter **one** DM, called a private reply.
- That first DM has to go out within **7 days** of the comment.
- Anything after the first DM needs the person to reply or tap first. A tap or a reply opens a 24-hour window in which the rest of the flow goes through.
- People who don't follow the account get the DM in their message requests, and show as **Requested** in Inrō until they accept or reply.
- A link sent as a tappable link card is the reliable way to deliver a link. Raw links typed into DM text may get throttled.
- On very busy posts, Inrō's comment reply limiting (an option on the public reply step) skips some public replies to keep the account safe. The DMs are what matter.

So the reel's promise and the first DM have to fit together: the first DM is a single message that should give, or unlock with one tap, what the reel promised.

## Choosing the keyword

- **One word, tied to the payoff.** MENU, PLAN, PRICES, QUOTE, GUIDE, SIZES. The word reminds the viewer what they asked for when the DM lands.
- **Easy to spell and to type on a phone.** Avoid words people misspell, and anything with hyphens or numbers.
- **Not a word people write anyway.** "Yes", "love", "wow" or the product's name will fire on ordinary comments.
- **One per reel.** Two keywords split the audience and confuse the automation setup.
- **Case and accents don't matter** in Inrō's keyword matching. A comment that contains the keyword among other words also matches ("menu please!").
- If people keep writing it differently, add the variant as a second keyword on the automation, or switch the automation to AI-detected intent ("asking for the menu") instead of a keyword.

## Writing the ask

The shape: **the keyword, what they get, where it arrives.** Then, if it helps, why it's worth it.

| Client goal | Line in the reel |
|---|---|
| Lead magnet | "Comment GUIDE and I'll send you the one-page checklist we use with every new client." |
| Price list | "Prices are in the DM. Comment PRICES and you'll have them in a minute." |
| Booking | "Comment BOOK and I'll send you the link with this week's free slots." |
| Product | "Want the exact shade? Comment SHADE and I'll DM you the link." |
| Local visit | "Comment MENU and we'll send this week's menu, so you know what's on before you come in." |
| Waitlist or drop | "Comment DROP and you'll be the first to get the link on Thursday." |
| Quote | "Send me QUOTE in the comments and I'll ask you three quick questions, then price it." |

Placement:
- **After the value, not before.** Asking in the first seconds reads as an ad and costs the opening. Ask once the viewer has had the tip, the reveal or the result.
- **Say it, show it, write it.** Spoken, as on-screen text, and near the top of the caption, where it shows before "more". You can also pin a comment with the keyword in the Instagram app.
- **Keep it a single ask.** "Comment, follow, share and save" asks for four things and gets none.

## Promise what the DM does

Match the line to how the automation opens (its `question_type` in Inrō):

| How the DM opens | What the reel can say | Avoid |
|---|---|---|
| A button to tap, then the link | "I'll DM you the link" | Nothing special |
| A question they reply to | "I'll DM you a quick question, then the link" | "Instantly" |
| Ask to follow first | "Follow and comment MENU, I'll send it over" | Implying it's free of conditions |
| Ask for their email | "Comment GUIDE and I'll send it to your inbox" | Hiding that you'll ask for an email |

If the payoff is a booking, a payment or an email capture, or the client wants their AI agent to take over the conversation, the automation needs more than one step. That is `dm-flow-builder`'s job.

## Make it an offer, not a reach trick

In 2024 Instagram clarified that engaging people in comments and DMs to build relationships or generate leads isn't engagement bait, and that the problem is content designed only to farm interactions for reach (reported by Social Media Today: https://www.socialmediatoday.com/news/instagram-clarifies-advice-on-single-word-ctas-and-longer-reels/718151/). In practice:

- The keyword must lead to something the viewer wants and gets.
- Don't ask for a comment with nothing behind it ("comment YES if you agree") on reels you want recommended.
- Answer real questions in the comments too, not only the keyword.

## Checklist before the reel goes live

1. The keyword in the script, on screen and in the caption is the same word as in the automation.
2. The automation exists, targets this post (or "Next post only" if built before publishing), and is switched on.
3. The link in the DM works, opens on a phone, and is the page the reel promised.
4. The DM wording sounds like the client, not like a template. The quick automation copies wording from the client's last comment-to-DM automation, so read it.
5. Someone on the agency side has commented the keyword from an account the team controls and received the DM. Never test on real followers.
6. If the reel is about an offer, the client's AI agent has a note on the post (price, dates, stock) so it can answer follow-up questions.
7. If the post was already live with comments before the automation was switched on, check whether you want to run it on those comments. Switching a comment scenario on in Inrō offers **Catch up** for comments from the last 7 days.

## Common misses

- The reel says MENU, the automation listens for LINK.
- The automation was built but left off.
- The ask comes in the first line and the reel loses people before the value.
- The DM sends a raw URL in text instead of a link card.
- The reel promises "free" and the DM asks for an email without saying so.
- A word so common that every "love this" comment triggers it.

## Reading the result

Compare three numbers on the post: comments, DMs sent by the automation, and link taps. Many comments but few DMs points at the automation (off, wrong keyword). Many DMs but few taps points at the DM or the offer. High reach with few comments points at the ask in the reel. Inrō shows the automation's numbers on the scenario, and the post's own numbers on its **Insights** tab where Instagram reports them for that account.
