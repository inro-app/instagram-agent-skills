# Writing the backup and the audit

Three outputs, three readers:

| File | Reader | Tone |
|---|---|---|
| `<handle>-backup-<date>.md` | whoever restores the account | complete, raw, technical |
| `<handle>-audit-<date>.md` | the client, or the agency lead who presents it | plain, specific, in the client's language |
| `<handle>-notes-<date>.md` | your own team only | blunt: doubts, hypotheses, checks still to do |

Nothing from the notes file ever goes into the audit.

## The backup

Write it before anything changes. Sections, in order:

1. **Header.** Account username and name, connector used, the date and time of every read, and this warning: "A snapshot. Re-read the account before relying on it."
2. **Account.** `get_organization_info` as returned, and `settings` → `get_optout` in full.
3. **Entry points.** Every icebreaker (question, payload, linked automations) and every persistent menu entry (type, title, payload or URL), verbatim.
4. **AI agent.** A table of every field from `agent` → `get`, with a column "restorable through the connector": yes for the fields `agent_manage` → `update` accepts, no for `model`, `reasoning` and anything else it does not take. If `context_migrated` is false, include the older fields (`description`, `goals`, `chat_instructions`, `style_rules`, `role`, `account_type`, `audience_type`) in full.
5. **Restore payload.** One JSON block that puts every editable agent field back in a single `agent_manage` → `update` call (shape below).
6. **Knowledge.** Every item verbatim in a fenced block, with `item_type`, `source_url`, whether it pulls in other pages of the site, `retrieval`, and `status`.
7. **Agent actions** (trigger, target type, target id and the target's name) and **tracked properties**.
8. **Contact properties**: title, slug, type, choices, `agent_active`, `auto_detect`.
9. **Folders** with their counts, **segments** with their filters, **conversion links** (title, URL, button).
10. **Scenario folders** (type and order), then **every scenario**: title, id, active, folder and priority, settings (excluded folders, frequency limit, interrupt settings), triggers with options, and the full action tree as returned by `scenarios` → `get`.
11. **Campaigns**: status, schedule, audience rules, actions.
12. **Restore limits** (below).

### Restore payload shape

Fill it from `agent` → `get`; every value below is a placeholder. Leave out any field that was empty, and leave out the ids inside `rules` so the list is recreated exactly as saved.

```json
{
  "action": "update",
  "action_params": {
    "about": "...",
    "goal": "...",
    "rules": [
      { "kind": "voice", "text": "..." },
      { "kind": "instruction", "text": "..." }
    ],
    "message_length": 25,
    "message_examples": ["..."],
    "auto_like": true,
    "trigger_mode": "specific_messages",
    "trigger_intents": { "intents": ["..."] },
    "folder_rules": { "folder_rule_type": "exclude", "folder_ids": [1234] },
    "no_reply_active": true,
    "no_reply_scenario_id": "5678",
    "request_human_scenario_id": "9012",
    "human_takeover_active": true,
    "human_takeover_pause": 12,
    "built_in_property_access": ["email"],
    "common_intents": ["..."]
  }
}
```

Knowledge items, actions and tracked properties go back one by one: `agent_manage` → `create_item` (`item_type` text with `text`, or url with `source_url`, plus `retrieval` and `crawl_source_url`), `create_action` (`trigger`, `target_type`, `target_id`) and `create_contact_property` (`field_name` or `contact_property_id`).

### Restore limits to record

- Uploaded documents ("Text document", `item_type: file`) cannot be recreated through the connector. Keep the text and re-upload the file in the app.
- `model` and `reasoning` are not editable through the connector.
- Updating a scenario's actions replaces the complete list: steps left out are deleted. Replacing a scenario's triggers gives every trigger a new id, and a webhook trigger gets a new URL that anything outside Inrō must be told about.
- Ids change on recreate. Agent actions, intent targets and campaign rules that point at a recreated scenario, folder or link must be re-pointed.
- App-only settings (the account-wide exclusion filter, integrations, team access) are not in this file. Note what you saw in the app, if anything.
- Contacts, conversations and past runs are not backed up here and do not need to be: they are not changed by a configuration rebuild.

## The audit

```markdown
# Instagram DM audit: @handle

Read from Inrō on <date>. Covers <window, e.g. the last 30 days>.

## The account at a glance
| | |
|---|---|
| Instagram connection | Connected / Disconnected since <date> |
| Plan | <plan>, period ends <date> |
| Contacts | <total>, <n> active in the last 30 days |
| Live automations | <n> active of <n> |
| AI agent | <mode in plain words> |

## What is live and working
<facts and numbers, one claim per line>

## What is broken or stale
<each item: the finding in bold, one line of evidence>

## What is risky
<anything where a change would hit live conversations straight away>

## What is missing for this kind of business
<only gaps with an entry point on this account>

## The three quickest wins
<three blocks, in order; format in choosing-quick-wins.md>

## The full setup (optional)
<Foundations / Automations and campaigns / AI agent, one line per row>

## Decisions needed
<numbered questions, each with a recommendation>

## What this did not cover
<what could not be seen and why: app-only settings, a short story history, a recent reconnection>
```

## Writing rules

- **Never invent or estimate a number.** No figure without a read behind it.
- **A number handed to you is not a source.** Re-read every figure that arrives with the request (from a brief, a teammate, an earlier report) before it goes in.
- **A number with no comparison is not an insight.** Compare it with the account's own history, with its other flows, or label it as a total.
- **No outcome promises.** No guaranteed followers, leads or revenue.
- **Their language, not the tool's.** "People who tapped through to your booking page", not "conversion link 1234". "Conversations the AI agent answered", not "agent_reply executions". No ids, field names, statuses or settings values in the audit.
- **Say what is missing.** If story history is short because the account was connected last week, write that. A gap you name reads as care; a gap you hide reads as sloppy when the client notices.
- **One claim per observation.** Bold claim, one line of evidence, move on.
- **People's names, not pronouns.** Write about the account owner by name or as "they", unless their profile states otherwise. The audit itself says "you".

### A zero is a claim about Inrō, not about them

Inrō records what Inrō did. It cannot see another tool, a reply typed in the Instagram app, or an email list kept somewhere else. Scope every zero to what Inrō can observe:

| Never write | Write instead |
|---|---|
| No automation has ever run on this account | No automation is running through Inrō |
| You have never sent a campaign | No campaign has been sent from Inrō |
| Not one of your comments gets a reply | No reply to these was sent through Inrō |
| You capture no email addresses | No email address is stored on a contact here |
| Nobody answers your story replies | No flow in Inrō picks up a story reply today |
| Every reply is typed by hand | None of these replies was sent by a flow or the agent |

Inrō's own comment flows post public replies too, so split the account's replies by who sent them before calling any of them manual.

Where the zero is the finding, it still leads, scoped: "312 people commented on these reels, and no flow in Inrō answered them." The force is in the volume and the gap, not in the absolute.

Never name or guess another tool in the audit, including link-in-bio services, booking tools or community platforms. Write "your first link", "your booking page", "the community's own page".

### Findings, not process

The audit describes what was measured, not how. Use "analysed", "measured", "recorded", never "read", "went through", "looked at".

| Never write | Write instead |
|---|---|
| We read 40 of your DMs | Of 40 recent conversations analysed, ... |
| We went through your comments and found ... | Comments on the last 10 reels show ... |
| We have left story automation out on purpose | Story automation is not recommended here |
| What we looked at | What this covers |

Sample sizes stay; they are what keeps a percentage honest. No meta-commentary about your own effort or judgement ("that's not a criticism"), and nothing about how the audit was made.

### Messages and comments

- Stock phrases are fine to quote, because they are button taps or common requests: "send me the link", "price?", "yes please".
- An individual's words are not, however typical they feel. Generalize them: a sharp question about whether the offer is real becomes "questions about whether the offer is legitimate"; "I never got it" becomes "the guide never arrived".
- No usernames of people who wrote in.

### The internal notes

Everything meant for your team: hypotheses to test on the call, a figure you left out and why, a doubt about a number, a tool you suspect they use, app checks still to do, what the next audit should look at. Blunt is fine here. Before you share the audit, reread every sentence and ask: is this about their account, or about how we made this? Only the first kind stays.

## The quality gate, in detail

Run it on the finished audit, with the client's live Instagram profile open next to it.

1. **Right account.** Is this the account the business runs its offer from? Look for a separate brand, product or topic account, an old account, or a personal one. If the handle came from a list or an email signature, treat it as a guess and confirm it with the client.
2. **On-topic evidence.** Every post, reel or story the audit relies on is about the offer it recommends for. A reel about something else is not evidence for this funnel, however many comments it has.
3. **The premise survives its own data.** No finding contradicts the recommendation. If the audit says "none of the comments mention the course" and then proposes a course funnel off those comments, one of them has to go.
4. **Every number traces to a read**, with a window and a date, and the arithmetic adds up.
5. **Nothing generic.** Swap in another account's name: if a sentence still fits, rewrite it or cut it.

Checking the numbers against your own notes is not enough; that check misses all of the above. Do not send on a fail.
