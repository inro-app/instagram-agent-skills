---
name: dm-flow-builder
description: Build, check and test Instagram DM automations in Inrō for a client, safely. Covers comment-to-DM, DM keyword replies, story replies, follow-ups, welcome flows and ice breakers, the persistent menu, and DM campaigns. Starts from an Inrō template where one fits, otherwise builds the scenario from explicit triggers and actions. Creates everything switched off, checks it with show_scenario and the builder warnings, tests it without messaging real contacts, and switches it on only with the user's approval. Use when someone asks to build or set up an automation, a comment to DM flow, a keyword auto-reply, a story reply flow, a follow-up, ice breakers, a DM menu or a campaign, to import a template, to fix a scenario that is not firing, or to build the items of a DM funnel plan.
license: MIT
---

# DM flow builder

Build the automations from a plan, one at a time, on one client's account. Everything is created switched off, checked, tested on your own account, and switched on only when the user says so.

**Requirements.** The Inrō connector (`https://api.inro.social/mcp`, sign in with OAuth), connected to the client's account. The account must be on Pro (monthly or annual), a free trial, or a lifetime plan (free accounts are refused), and one connection reaches one account. If you manage many clients, use the Inrō partner connector (`https://api.inro.social/partner/mcp`, your partner token in an `Authorization: Bearer` header); every request then names the client, preferably by the account id from `list_organizations` (a username that matches several accounts is refused), and each client still needs one of those plans. Without a connector, this skill can still write the build spec and the click-by-click steps for someone to follow in the Inrō app.

If there is no plan yet, run `dm-funnel-planner` first, or at least agree the goal, the entry point and the destination of the one flow you are building.

## Safety rules

These hold for every build, on every account.

1. **Confirm the account before anything.** `get_organization_info`, then say back the username, name and plan, and get a yes. If several Inrō connectors are loaded, check each and agree which one is this client. Never mix them in one task.
2. **Read before you write.** Section 2 is a read-only pass. Do it every time.
3. **Show the plan and get an OK before any write.** Say exactly what will be created or changed, in plain words.
4. **Create switched off.** Pass `active: false` on every create. The one-call comment shortcut (`attach_comment_to_dm`) switches on by default, so always pass `active: false` to it.
5. **Never message real contacts as a test.** Test only on your own Instagram account or a team member's (section 9). Never use `scenarios_manage` `trigger`, `campaigns_manage` `send` or `resend` to test: those reach real people.
6. **Switch on only with approval**, after the test, and name the scenario being switched on.
7. **Never delete without explicit approval** of that item. Prefer switching off. Deleting a scenario removes its triggers and steps for good.
8. **One client at a time**, unless the user asked for a bulk change. For the same flow across many clients, use `partner-bulk-rollout`.
9. **On the partner connector, name the client in every call.** Nothing is remembered between calls.

## 0. Know your tools

Read and write tools are separate. Reads: `scenarios` (list, get, performance), `show_scenario`, `medias`, `stories`, `folders`, `scenario_folders`, `conversion_links`, `icebreakers`, `persistent_menu`, `campaigns`, `show_campaign`, `executions`, `contacts`, `agent`, `settings`, `search_templates`, `get_trigger_types`, `get_action_types`. Writes: the matching `_manage` tools.

**Call `get_trigger_types` and `get_action_types` before building any triggers or actions, every time.** They return the current options and branch labels. The summary in `references/triggers-and-actions.md` was checked on 12 November 2026, and the live response wins if they differ.

Some settings exist only in the app (for example the account-wide **Exclude specific contacts** card, a scenario's test code, and **Catch up**). When the connector cannot do a step, say so and give the user the click path.

## 1. Get the brief

For the one flow you are building, you need:

- **Goal** in one line, and what happens to the person at the end.
- **Entry point**: which posts, stories, DM words, ad, QR code, ice breaker or menu entry.
- **Destination**: the link, file, booking page, folder, or a person on the team.
- **Copy**: the client's wording, or your draft for their approval.
- **What is captured**: email, phone, a property, a folder.
- **Guardrails**: who must not get it (customers, team), what the brand never says.

## 2. Read before you write

1. `scenarios` list. For each active scenario that could fire on the same comment, story reply or DM, `get` it. Overlap means the person gets two replies, or one flow blocks the other.
2. `scenario_folders` list. A **priority** folder runs only its highest-priority matching scenario per person; a **normal** folder runs all of them. To see the order inside a folder, `scenarios` list with `scenario_folder_id` (the folder id as a string), `order_column: "scenario_folder_priority"`, `order_direction: "asc"`. `scenario_folders` get shows only how many scenarios the folder holds.
3. `folders` list and `conversion_links` list. Reuse the client's folders and links where they fit.
4. For a comment flow: `medias` list or get for the target posts. `comment_to_dm` on a post shows only a wizard or shortcut automation attached to it. Custom scenarios that watch all posts, chosen posts or a caption word don't show there, so also read the comment triggers of the scenarios from step 1.
5. For ice breakers or menu flows: `icebreakers` list and `persistent_menu` get.
6. If the flow uses an AI step: `agent` get. Every AI step uses the account's global AI agent settings, so if the agent knows nothing about this topic, the step will improvise. Fix the agent first with `instagram-ai-agent-setup`.
7. `settings` get_optout: opt-out on, and its keywords.

## 3. Pick the build path

| You want | Use |
|---|---|
| A flow a template already does | `search_templates`, or an id from `references/templates.md` (the newest ones import by id but aren't in search yet), then `scenarios_manage` create with `template_id` and a `title` (arrives switched off), then edit |
| People who comment on **one** post get a DM and a link | `medias_manage` `attach_comment_to_dm` on that post, with `active: false`. It targets the post, creates the link and fills in every step |
| A new post and its comment automation together | `medias_manage` create with `comment_to_dm` (set `active: false` inside it). See `client-post-scheduler` for the post itself |
| Comment to DM on all posts, the next post, or posts with a caption word | `scenarios_manage` create with triggers and actions (a custom scenario), or the **Comment to DM link** wizard in the app |
| Anything else: DM keywords, story replies, welcome, ice breakers, menu, folder or schedule triggers, several entry points | `scenarios_manage` create with explicit triggers and actions |
| A one-off message to a chosen group | `campaigns_manage` create (a draft), see `references/recipes.md` |

Build modes on `scenarios_manage` create are exclusive: `template_id`, `prompt`, or `triggers`/`actions`. Use explicit triggers and actions by default. `prompt` generation is a drafting aid: it builds in the background, may decline or ask for clarification instead of building, uses a limited set of steps, and leaves out variables. Read its result in full before treating it as a draft.

Recipes with JSON for each flow type are in `references/recipes.md`.

## 4. Show the plan, get the OK

Before the first write, show the user:

- the scenario name (name it for the client report: "Comments: TRIAL to intro offer", not "comment flow v2"),
- the trigger in plain words,
- each step, with the exact message text,
- the link, folders and settings (run once, interrupt on manual reply),
- that it will be created switched off.

Wait for a clear yes.

## 5. Build rules

- **`active: false` on create.** Always.
- **The actions array is a flat list.** Each step has an `action_key`; a child names its parent with `parent_key` (new parent in the same payload) or `parent_id` (existing parent), and the branch with `parent_branch`. A step under a non-branching step has no `parent_branch`.
- **One step per branch.** If two steps hang off the same branch, only the first runs. Chain them one after the other.
- **One root.** Only one step can start the flow.
- **Unique `action_key`s.** Duplicates break updates.
- **Updates replace the whole actions list.** Send every step you want to keep (`{"id": 123}` keeps one unchanged). Anything left out is deleted. A step's `options` is also replaced as a whole, not merged: to change one option, send the step's full `options` from `get` with your change in it, or the other options are wiped (an alert email loses its subject and body). Triggers work differently: a list with no ids replaces all triggers (a webhook trigger then gets a new URL); once any trigger in the list has an `id`, listed ones are updated, new ones added, and unlisted ones kept. Always `get` first and build the update from what came back.
- **Put deletable steps last** in their branch (an alert email, a pixel event), so removing them later orphans nothing.
- **One scenario per intent.** Several triggers can share one flow when they lead to the same place.
- **Follow the account's existing shape** unless there is a reason not to.
- **Group it.** Put the scenario in a scenario folder (`scenario_folder_id`); use a priority folder when two flows could match the same person.
- **Read the response warnings.** Create and update return each step's `warnings`. Severity `issue` means the flow will not run as written; fix and resubmit. `suggestion` means it may misfire.

## 6. Comment to DM rules

Instagram rules, they apply to every tool:

- **One DM per comment until the person responds.** The first DM is a private reply. Anything after it waits until they reply, tap a button or open a link card. Inrō holds a second message, retries it, and drops it if they never respond.
- **7 days.** A comment can only be answered by DM within 7 days. Comments on a Live: 24 hours.
- **So the first DM must ask for a tap or reply**: a button (`button_template`), a question (`ask_question`), a follow request (`ask_for_follow`) or an email request (`collect_property`). If the first DM is plain text, follow it with `wait_for_reply` before anything else. The link comes after.
- **No raw URL in the first message.** Meta may block DMs with plain links when an account sends many. Send links as a link card (`conversion_link`).
- **Reply publicly too** with a `comment` step, with two or three variants. Public replies are only possible on top-level comments.
- **Choose the keyword with care.** Keywords match whole words, ignoring case and accents; a keyword of 4+ letters also matches its plural. Check the word against the client's captions and recent comments so it does not fire on ordinary comments.
- **One post choice and one comment filter per trigger.** For keyword plus AI intent, add two comment triggers to the same scenario: one `comment_keywords`, one `ai_detected` with a short intent ("asks how to get the free guide"). An AI intent needs AI features and uses credits.
- **Next post** watches only the first post published after the trigger is created. For "this post and every future one", use a caption keyword the client puts in each caption.
- **Exclude hateful and negative comments** is off by default. Turn it on for lead flows (it is an AI check).
- **Past comments.** **Catch up** runs the flow on matching comments from the last 7 days that never got it, one message per person, with a count first. It is in the app only: offered when a comment flow is switched on in the app, and on the scenario's results. Switching on through the connector doesn't catch up. It messages real people, so it needs the user's explicit OK on the number.

More detail and examples: `references/recipes.md`.

## 7. Links, buttons and files

- **Link card** (`conversion_link`): tracks clicks. Branches `option_clicked` and `option_expired`. Create it inline (`title`, `url`, `button_title`) or reference an existing one by `id`. A shared link referenced by id is the same link in every flow that sends it, so editing it changes all of them.
- **Button message** (`button_template`): one branch per postback button (`option_0`, `option_1`, ...) plus `option_expired`. A `web_url` button opens a page but does not branch and is not tracked as a click. Keep to one clear button where you can.
- **File** (`send_file`): a downloadable file with a button (button label up to 20 characters).
- **Message text**: up to 1,000 characters. Identical consecutive messages may not be sent.
- **Variables**: `{{contact.name}}`, `{{contact.username}}`, `{{trigger.comment}}`, `{{trigger.message}}` and more. Insert them where they read naturally.

## 8. Hygiene on every flow

- **Run once per person** for lead flows: `rate_limit_enabled: true`, `rate_limit_unit: "once"`. Or once every N hours or days.
- **Stop when a person takes over**: `interrupt_on_message: true` (a team member replying by hand stops pending runs). `interrupt_on_reply: true` stops pending runs when the contact writes, except at a step waiting for that reply.
- **Keep customers and the team out**: per-scenario excluded folders. `scenarios_manage` update with `id` and the full `excluded_folder_ids` list, in a call of its own, then read it back with `scenarios` get (details in `references/triggers-and-actions.md`). Or **Exclude specific folders** in the app. Keep the account-wide **Exclude specific contacts** card for spam only: it applies to every automation, including the helpers that step back while the team is replying (see `client-account-setup`).
- **Priority folders** when two flows can match the same comment or DM.
- **Opt-out on** (`settings`). Opted-out contacts are skipped by every automation.
- **Follow-up timing**: Instagram only lets you message people who wrote in the last 24 hours. Set link and question timeouts in hours, not days, so the follow-up still arrives.

## 9. Check, then test without messaging real contacts

**Check.** Call `show_scenario` (or `show_campaign`) so the user sees the flow drawn as it is in Inrō, with its warnings. Then `scenarios` get and confirm: trigger options as intended, every step in the right branch, link URL correct, folders are the client's own, settings set, `active` false. The full checklist is in `references/checks-and-testing.md`.

**Test on your own account only.** Two safe ways:

- **Test code.** Every scenario has a test code, shown in the app under **Test scenario**. From your own or a team member's Instagram account, send the code to the client's account as a DM, or as a comment on one of its posts for a comment flow. The flow runs as a test for you, even while switched off. A comment test posts a public reply under your comment, so use an older post and delete the comment afterwards.
- **Test on a chosen contact.** `scenarios_manage` `test` with `contact` set to your own account's contact (it must have messaged the client account in the last 24 hours, or the DM is held). It really sends the messages to that contact. Never pick a customer.

Test runs are kept out of the results, and they skip the run-once limit, excluded folders and the account exclusion filter, noting on the run which rule they skipped. So a test that works does not prove those rules; check them in the settings. Read the run with `executions` list (`scenario_id`, `include_test: true`) then `get`.

Campaigns: `campaigns_manage` `test` with your own contact, never `send`.

## 10. Switch on with approval

Show the test result and ask: "Switch on <scenario name> now?" Only on a yes, `scenarios_manage` update with `id` and `active: true`. For a comment flow, tell the user about **Catch up** (in the app; the connector can't run it). It messages the number of people it shows, so running it is their separate decision.

In the first 24 hours, read `scenarios` performance and the first real runs in `executions`. If people stop at a step, read a few of those runs before changing anything.

## 11. Fixing a flow that does not fire

Work in this order: `executions` health (a broken Instagram connection or a used-up contact limit stops everything), then `scenarios` performance on the flow (which step breaks), then `executions` list and get on failing runs. Common causes are in `references/checks-and-testing.md`: inactive, wrong post, keyword never used, run-once already used, excluded folder, a priority folder sibling winning, the 7-day comment window, the 24-hour DM window, another tool holding the conversation.

Edit with a full `get` first and a full actions list. If an update keeps failing on a scenario, build a fixed copy as a new scenario (switched off), test it, switch the old one off on approval, and ask before deleting anything.

## 12. Related skills

- `dm-funnel-planner`: decides what to build and in what order.
- `instagram-ai-agent-setup`: the AI agent that every AI step inherits, and the flows it escalates to.
- `client-post-scheduler`: the post that a comment flow watches, published with its automation.
- `instagram-account-audit`: a full read of what is set up before changing a busy account.
- `inbound-dm-playbook`: how the team handles the conversations these flows hand over.
- `monthly-client-report`: reporting each flow's numbers.
- `partner-bulk-rollout`: the same flow on many client accounts.
