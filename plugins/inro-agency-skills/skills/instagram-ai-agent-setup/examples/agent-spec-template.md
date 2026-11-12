# AI agent spec: @client_username

Fill this in, show it to the user, and get an OK before any write. Put the character count after every text field. Keep the backup from Step 1 next to it.

## 0. Account and scope

- Account confirmed with `get_organization_info`: @username, plan ______, connection OK yes/no
- Job: new agent / rebuild / fix
- Current activation mode: ______ (from the backup)
- Automations on the account that use AI steps: ______ (they will change with this spec)
- Older agent still on legacy fields (`context_migrated: false`): yes/no

## 1. Conflicts and rulings

| Topic | Source A says | Source B says | Ruling (from the user) |
|---|---|---|---|
| | | | |

## 2. Voice and personality

**About** (__/500)

> 

**Message length:** 10 / 25 / 50. The client's approved answer to their most common question is __ words.

**Auto-like positive messages:** on / off

**Message examples** (10 to 20, real, varied)

| # | Situation | Example |
|---|---|---|
| 1 | Opener | |
| 2 | Short acknowledgement | |
| 3 | Casual personal answer | |
| 4 | On-topic answer | |
| 5 | Commercial line | |
| 6 | Polite no | |
| 7 | Handoff to the team | |

**Voice rules** (one sentence each, up to 300 characters)

| # | Rule | Chars | Keep id / new |
|---|---|---|---|
| V1 | | | |

## 3. Goal and instructions

**Goal** (__/500)

> 

**Instructions** (one sentence each, up to 300 characters)

| # | Rule | Chars | Keep id / new |
|---|---|---|---|
| I1 | Bare greeting: | | |
| I2 | Price: | | |
| I3 | Dates and availability: | | |
| I4 | Refunds and complaints: | | |
| I5 | Advice it must not give: | | |
| I6 | When to pass to the team: | | |
| I7 | "Are you a bot?": | | |

Rules to delete from the current config (each needs the user's OK):

| Current rule id | Text | Why |
|---|---|---|

## 4. Knowledge

**Knowledge access:** Limit to instructions / Always have an answer

**If the agent cannot reply, trigger:** scenario ______

| # | Header (what it covers) | Source (text / website / document) | Chars | New / replaces item |
|---|---|---|---|---|
| K1 | | | | |

Items to delete after the new ones are ready (each needs the user's OK):

| Item id | What it was | Why |
|---|---|---|

Post or story notes to add:

| Post or story | Notes |
|---|---|

## 5. Actions and data collection

| When contact wants to... | Do the following... | Target (name and id) |
|---|---|---|
| | Send a conversion link / Add to folder / Start an automation scenario / Send a survey | |

Properties to detect: Email / Phone / custom: ______ (description checked in the app: yes/no)

Built-in fields the agent may read: email / phone / none

## 6. Human intervention

- Pause the agent when a team member replies: on / off
- Pause for: 1 / 4 / 12 / 24 hours
- If contact asks to speak to a human, trigger: scenario ______
- Escalation scenario (built with `dm-flow-builder`): adds to folder ______, alerts ______

## 7. Activation (applied last, separate OK)

- Mode during build and tests: ______
- Go-live mode: Automation only / Specific intents only / All pending messages
- AI-detected intents (if Specific intents only): ______
- Folder limits: none / only these: ______ / never these: ______ (include the escalation folder)

## 8. Write plan

| Order | Call | What changes |
|---|---|---|
| 1 | `agent_manage` `update` | About, Goal, full rules list, examples, length, auto-like |
| 2 | `agent_manage` `create_item` (each) | New knowledge items |
| 3 | `agent_manage` `create_contact_property` | Detected properties |
| 4 | `agent_manage` `create_action` (each) | Intent actions |
| 5 | `agent_manage` `update` | Knowledge access, cannot-reply scenario, human intervention, folder limits |
| 6 | App, by the user | File uploads, model and reasoning, property descriptions check |
| 7 | `agent_manage` `update` | Activation mode, only after the test pass and the user's go |

## 9. Test results

| Case | Reply | Pass/fail | Fix |
|---|---|---|---|
