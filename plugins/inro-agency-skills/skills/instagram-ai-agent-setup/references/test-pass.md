# Test pass and troubleshooting

## Where to test

- **Chat with Agent** (top right of the AI Agent page, and beside every settings panel). A private test chat: nothing is sent to contacts. It shows the reply, any link or survey it would send, any folder or scenario action it would trigger, any contact property it would detect, and "Human intervention requested" when it would hand off. It does not run those actions. Use **Reset chat** between cases. **Chat as** lets you pick one of the client's contacts to simulate; pick a team member's or test contact, not a customer.
- **Your own test account.** Post and story notes, and automations with AI steps, are not covered by the test chat. Test them by commenting or replying from an Instagram account you control, or with **Test scenario** in the automation (see `dm-flow-builder`). Test runs send real messages, so only ever to yourself.

Never DM a real follower to see what the agent does.

## The script

Run every case. Record the reply word for word, pass or fail, and the field you will change for each fail. Expect at least one failure on a first build.

| # | Send | Pass when |
|---|---|---|
| 1 | "hi" | Greets and asks what they need. No pitch, no assumed product. |
| 2 | The most common question, as a customer would type it | Correct facts from the knowledge; fits the message length; no invented numbers. |
| 3 | The most common commercial question ("how much?", "can I book?") | Follows the Instruction script; offers the right link if an action exists. |
| 4 | A question the knowledge does not cover | With Limit to instructions: says it doesn't know, no guess. |
| 5 | "can I talk to a real person?" | Short acknowledgement, then stops; test chat shows a human request. |
| 6 | Each banned move: a price, a date, a refund, a discount, advice | Follows the matching Instruction every time. |
| 7 | Each intent action's situation, phrased two ways | The right link, survey, folder or scenario shows in the test chat. |
| 8 | Something that should not trigger an action | No action fires. Overlapping intents show up here. |
| 9 | A complaint or an upset message | Apologises once, asks for details, routes to the team if that is the rule. |
| 10 | A distress or urgent message, if the vertical has them | Points to emergency help and routes to the team. |
| 11 | "are you a bot?" | The honest answer from the Instructions. |
| 12 | The same question as case 2, in different words | Same facts; doesn't repeat the earlier reply word for word. |
| 13 | A message in the client's second language | Replies in that language with the same facts. |
| 14 | A message that includes an email or phone number | The test chat shows the detected property, if collection is on. |
| 15 | A long, rambling message with two questions | Answers both, briefly, or answers one and asks about the other. |

After fixing, rerun the failed cases and cases 1, 2 and 6, since fixes in one place often break another.

## Reading a failure

| What you saw | Change |
|---|---|
| Sales pitch on "hi" | Goal (make it neutral) |
| Wrong fact | The knowledge item, then check no other item disagrees |
| Invented a number or date | Instructions (add the script); Knowledge access to Limit to instructions |
| Right content, wrong voice | Message examples first, then Voice rules |
| Too long, cut off, or split into fragments | Message length |
| Same rule obeyed sometimes | Move it into Instructions; remove duplicates |
| Action fires on the wrong message | Narrow that action's intent wording |
| Action never fires | Rephrase the intent the way a customer writes |

In the app, **Improve reply** (on agent messages in **Message history**, the inbox, and automation run history) turns a written correction into suggested edits to Profile (connector field `about`), Goal, rules and examples. Review each before and after, edit if needed, and apply. It does not edit knowledge items; fix those yourself.

## Agent not replying

Work through in order. Most cases are the first two.

1. **Activation mode.** The status chip on the AI Agent page names it. Disable all replies is a full stop, including AI steps in automations. Specific intents only with no intents replies to nothing. Automation only ignores normal DMs.
2. **AI credits.** On a Trial or another metered plan, every AI reply uses credits. With none left, AI replies and AI steps are skipped until credits are added or the account moves to Pro. The mode itself does not change.
3. **Folder limits.** Is the contact in a folder under Never reply to contacts in these folders, or outside the folders under Only reply to contacts in these folders?
4. **An automation got there first.** Automations take priority; the agent does not reply when a scenario already did or is running for that contact. Check the conversation's handling status in the inbox.
5. **A person is handling it.** After a team member replies (from the inbox or the Instagram app), the agent waits for the pause set under Human intervention. After a request for a human, it waits until a team member replies. Use **Hand back to AI Agent** in the inbox to return it early.
6. **The message.** No reply to a message with no text (a bare photo or mention), or when a newer message from the contact already arrived.
7. **The connection.** `get_organization_info` shows `login_error_data`. A broken Instagram connection stops all sending.
8. **The account's own OpenAI key.** If the account uses its own key and that key is out of credit or rate limited, replies stop until it is topped up on the OpenAI side.

An empty knowledge base does not stop replies: the agent still answers from its Profile, Goal and Instructions.

## First week after go-live

- Daily: read the agent's conversations (inbox filter **Currently handled by agents**, plus **Message history**). Note wrong answers, off-voice replies, and questions it should have answered.
- Check the escalation folder and the team alerts: did every handoff reach a person?
- Check which intent actions fired and which never did. Reword the silent ones.
- Check detected properties on a few contact profiles.
- Only after a clean week, consider widening the activation mode, with the user's OK.
