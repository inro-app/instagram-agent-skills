# Client intake: what to ask before you build

Send the client the questions in part 1 (copy them into an email or a form). Part 2 says what each answer drives, so you know which gaps block the build and which can wait.

## Part 1. The questions (client-facing)

Keep the tone light. Most clients answer faster with examples than with a blank box.

**About your business**
1. In one or two sentences: what do you sell, and to whom?
2. What should Instagram DMs achieve for you in the next three months? Pick up to two: more bookings, more sales, fewer repeat questions for the team, more leads for later, faster answers to customers, sorting out collab requests.
3. Which offers or products should we point people to, and what is the link for each (shop, booking page, sign-up, WhatsApp)?
4. Which prices are you happy for us to state in DMs? Anything that should only ever be quoted by a person?
5. Any discount or promo codes we can give? Any we must never give? When does each one end?

**The questions you get**
6. What are the five to ten questions people ask most in your DMs? Paste your usual answer to each.
7. What do people ask that you'd rather a person always answers? (Refunds, complaints, medical or legal questions, custom quotes, anything about money, anything upsetting.)
8. Do you get collab or sponsorship requests in DMs? Who looks at them, and at which email address?

**Your team**
9. Who answers DMs today, on which days and hours? Do they reply from the Instagram app, the Inrō inbox, or both?
10. Which email address should get each kind of alert: support, sales or bookings, partnerships?
11. Are there people the automations should never message (partners, ambassadors, friends of the brand)? We'll put them in a "Human only" folder.
12. When you close (holidays, time off), what should people hear?

**How you sound**
13. Paste three to five real DM replies you sent and liked. We'll match that voice.
14. Emojis: yes, a few, or none? First name or no name? Which languages do your customers write in?

**Setup**
15. Is another DM automation tool connected to this Instagram account? It has to be switched off before we start, or conversations can lock.
16. Which tools do you use for bookings, payments or your shop (for example Calendly, Shopify, Stripe)?
17. Who signs off changes on your side, and do you want to see each message before it goes live?

## Part 2. What each answer drives

| Answer | Drives | Blocks the build? |
|---|---|---|
| 1, 2 Business and goals | Which automations from `inbound-dm-playbook`, in which priority order | Yes |
| 3 Links | Conversion links, the persistent menu, every "send the link" step | Yes, for any flow that sends a link |
| 4 Prices | Price replies, the agent's knowledge base | Yes, for price flows. Without it, price questions go to a person |
| 5 Codes | Promo lines; "never give" goes in the agent's rules | No. Leave codes out until confirmed |
| 6 Top questions | Ice breakers (top 4), FAQ answers, knowledge base items | Yes, for ice breakers and the AI front desk |
| 7 Human-only topics | The handover list (agent rules, knowledge base, alert email), AI intent "Not" lists, the complaint flow | Yes |
| 8 Collabs | The collab flow's alert address and holding reply | No. Default: file and alert the main address |
| 9 Team hours and tools | Team hold window, the agent's pause after a team reply, alert wording | No. Default: 24 hours |
| 10 Alert addresses | Every `send_email` step | Yes, for any flow that escalates |
| 11 Never-message list | Human only folder, filled by hand on day one | No |
| 12 Closures | Time-off message, the agent's knowledge base | No |
| 13, 14 Voice | Message text in every flow, the agent's voice rules (`instagram-ai-agent-setup`) | No, but every message needs a voice check before go-live |
| 15 Other tool | Thread ownership: two tools on one account lock conversations | Yes, until it is off |
| 16 Integrations | Booking and shop flows, payment steps | No |
| 17 Approvals | How you send the plan and the go-live request | No |

## Rules for using the answers

- Never fill a gap with a guess. A missing price means the flow sends people to a person, not that you write a likely number.
- Check product claims against a public source (the client's website, store listing or booking page) before writing them into a flow or the knowledge base. The automation repeats whatever you give it, confidently.
- When the client's latest message disagrees with an older document, use the latest message and say which you used.
- Keep the answers in your notes for this client, dated. Next month's report and any later change will need them.
