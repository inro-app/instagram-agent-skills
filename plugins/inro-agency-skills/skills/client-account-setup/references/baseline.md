# Baseline: exact settings and build specs

Everything here was checked against the current product. Before you build, call `get_trigger_types` and `get_action_types` once: if a field below no longer matches, the live answer wins.

Placeholders in capitals (`TEAM_HOLD_ID`, `HELPERS_ID`) are ids you get back from earlier steps. Write every id in your notes for this client: every flow, exclusion and alert refers to them.

## B1. Contact folders

Create these on day one with exactly these names (`folders_manage` `create`, colour is free: yellow, red, green, blue, purple, pink or orange). Inrō's templates use the same names, and a template import reuses a folder whose name matches exactly instead of creating a duplicate.

| Folder | What it means | Added by | Removed by | Used as an exclusion? |
|---|---|---|---|---|
| Human only | The team always handles this person by hand (partners, VIPs, friends of the brand) | The team, by hand | The team | Yes: on every replying scenario, and in the agent's folder rule |
| Team hold (24h) | The team is talking to this person right now | Team hold: start | Team hold: timer, or the team | Yes: on every replying scenario, and in the agent's folder rule |
| Needs a human | The team has to act | Human handover, escalation steps, some templates | The team, once handled | Only in the agent's folder rule, so the AI stays out of escalated chats |
| Collabs: requested | A brand, creator or agency pitched a collaboration. A permanent tag | The collab flow | Never | **No.** A permanent tag as an exclusion blocks that person from every flow forever |
| Collab window (7d) | Temporary: keeps sales and support flows off a partner's follow-ups | The collab flow | Its window timer (B4) | Yes, on flows that could misfire on follow-ups |
| Complaint window (7d) | Temporary: someone complained, asked for a refund or had an order problem | The complaint flow | Its window timer (B4) | Yes, on price, buying and promo flows |
| Internal test | Your agency's own test accounts | You | Never | Optional: filter it out of reports |

Add lifecycle or interest folders only when a flow will use them (for example "Customer" or "Lead"). Templates also create their own click folders ("Bookings: clicked", "Shop: clicked" and similar): keep those, they make the monthly report easy.

## B2. Scenario folders

```
scenario_folders_manage create  {name: "Inbound DMs", folder_type: "priority",
                                 description: "Every automation that replies to a DM. One reply per message."}
scenario_folders_manage create  {name: "Helpers", folder_type: "normal",
                                 description: "Silent helpers: team hold, windows, handover, likes."}
```

- Put each new scenario in its folder with `scenario_folder_id` (and `scenario_folder_priority` for Inbound DMs, 1 is highest), then set the full order once with `scenario_folders_manage` `reorder` (first id gets priority 1). Read the folder back with `scenario_folders` `get`.
- In the app these show on the Scenarios page as a **Priority folder** ("Only one scenario can trigger at a time") and a **Normal folder** ("Scenarios are triggered independently"). The help center calls them scenario groups. Prefer the connector for the order: dragging rows works but is easy to get wrong.
- `scenario_folders_manage` `toggle_active` switches every scenario in a folder on or off at once. Don't use it at go-live: switch scenarios on one at a time.

## B3. Team hold (two scenarios)

Build the timer first, because the start needs its id. Both go in Helpers. Both are created inactive.

```
scenarios_manage create
{
  "title": "Team hold: timer",
  "active": false,
  "scenario_folder_id": HELPERS_ID,
  "interrupt_on_message": true,
  "interrupt_on_reply": false,
  "actions": [
    {"action_key": "wait", "action_type": "delay",
     "options": {"delay_duration": 24, "delay_unit": "hours"}},
    {"action_key": "release", "parent_key": "wait", "action_type": "folder",
     "options": {"folder_ids": [TEAM_HOLD_ID], "folder_action": "remove"}}
  ]
}

scenarios_manage create
{
  "title": "Team hold: start",
  "active": false,
  "scenario_folder_id": HELPERS_ID,
  "interrupt_on_message": false,
  "interrupt_on_reply": false,
  "triggers": [
    {"trigger_type": "outgoing_message",
     "options": {"content_filter": "any", "outgoing_message_sent_from": ["instagram", "inbox"]}}
  ],
  "actions": [
    {"action_key": "hold", "action_type": "folder",
     "options": {"folder_ids": [TEAM_HOLD_ID], "folder_action": "add"}},
    {"action_key": "pause", "parent_key": "hold", "action_type": "delay",
     "options": {"delay_duration": 20, "delay_unit": "seconds"}},
    {"action_key": "timer", "parent_key": "pause", "action_type": "trigger_scenario",
     "options": {"scenario_id": TIMER_ID}}
  ]
}
```

- No run limit and no excluded folders on either. An exclusion would stop the helper from releasing people.
- `outgoing_message_sent_from` must be Instagram and the inbox only. Left at its default it also counts AI agent messages.
- Switch both on together, after the replying flows exclude Team hold (24h). If you only switch on the start, nobody is ever released.
- Pick a shorter window (12 hours) if the client's team answers fast and wants automations back sooner. Then set the agent's pause to the same value and rename the folder.
- Replacing an older hold on a takeover: switch the old one off first, and neutralise its release step (its waiting runs keep going after it is off). People already in the folder then need a fresh timer. Firing the timer for them with `scenarios_manage` `trigger` is safe because the timer sends no messages, but it touches real contacts: get the user's OK and list who is in the folder first (`folders` `list_contacts`).

## B4. A window helper ("keep X for N days")

Use it for Collab window (7d), Complaint window (7d), or any temporary state. The main flow adds the folder and starts the timer; the timer removes it.

```
scenarios_manage create
{
  "title": "Collab window: timer",
  "active": false,
  "scenario_folder_id": HELPERS_ID,
  "interrupt_on_message": false,
  "interrupt_on_reply": false,
  "actions": [
    {"action_key": "wait", "action_type": "delay", "options": {"delay_duration": 7, "delay_unit": "days"}},
    {"action_key": "release", "parent_key": "wait", "action_type": "folder",
     "options": {"folder_ids": [COLLAB_WINDOW_ID], "folder_action": "remove"}}
  ]
}
```

In the collab flow, right after it adds "Collabs: requested", add two steps: add to folder "Collab window (7d)", then **Trigger a scenario** "Collab window: timer". The timer is its own scenario with no interrupts so that a team reply, which stops the collab flow, can't stop the removal.

## B5. Human handover (the agent's escalation target)

No triggers of its own, so it can never fire by accident. The agent runs it.

```
scenarios_manage create
{
  "title": "Human handover",
  "active": false,
  "scenario_folder_id": HELPERS_ID,
  "interrupt_on_message": false,
  "actions": [
    {"action_key": "tag", "action_type": "folder",
     "options": {"folder_ids": [NEEDS_HUMAN_ID], "folder_action": "add"}},
    {"action_key": "alert", "parent_key": "tag", "action_type": "send_email",
     "options": {
       "email_addresses": ["SUPPORT_EMAIL_FROM_INTAKE"],
       "email_subject": "Needs a person: @{{contact.username}}",
       "email_content": "@{{contact.username}} needs a person.\nTheir last message: \"{{conversation.last_message_received}}\"\n\nWe hand these to you: HANDOVER_LIST.\n\nReply in the Inrō inbox or on Instagram. Instagram only lets you reply within 24 hours of their last message. Once you reply, the automations stay out of this chat for 24 hours."}}
  ]
}
```

Then wire it (after the user's OK):

```
agent_manage update {request_human_scenario_id: "HANDOVER_ID"}
agent_manage update {no_reply_active: true, no_reply_scenario_id: "HANDOVER_ID"}   # only with Limit to instructions
```

In the app: **AI Agent → Human intervention → Request a human**, "If contact asks to speak to a human, trigger this automation", and **AI Agent → Knowledge access and behaviour → Limit to instructions**, "If the agent cannot reply, trigger this automation". The agent already sends a short acknowledgement when someone asks for a person, so the scenario doesn't need a message of its own. Exclude Human only on it (B12). Switch it on with the rest after QA.

`HANDOVER_LIST` is the same list as in the agent's rules and the knowledge base (SKILL.md section 7). If you want to tell "asked for a person" apart from "the AI didn't know", make a copy for the second case with a different subject.

## B6. Silent helpers worth adding

Both come as templates (see `inbound-dm-playbook`, `references/templates.md`). After importing, put them in Helpers and add the exclusions.

- **Like stories that mention you** (template 6086): likes each story mention and files the person. Add excluded folders Human only and Team hold (24h), and consider a longer wait than the template's one minute (30 minutes or more) so the like doesn't look instant. There is no reshare step: resharing stays with the client's team. Ask the client how they handle mentions today before adding any message.
- **Auto-like positive messages** (template 6223): AI spots kind messages with no question in them and likes them. Same exclusions.

## B7. Opt-out

Read the current settings with `settings` `get_optout`, then propose:

```
settings_manage update_optout {
  active: true,
  keywords: ["unsubscribe", "opt out", "optout", "opt-out", "stop"],   # plus the client's languages
  ai_detection: true,
  confirmation_message: "Done, you won't get any more automated messages from us. You can still write to us any time.",
  menu_message: "Opt out of messages"
}
```

- **Keywords match a whole word anywhere in the message**, ignoring case and accents, and words of 4 or more letters also match a plural or one extra letter. So "stop" opts out someone who writes "can you stop my order?" For a shop, a booking business or anything with orders or memberships, consider dropping the bare "stop" and keeping "unsubscribe" and "opt out". Show the user this trade-off.
- Keywords only catch text. AI detection works in conversations the agent replies to. The menu entry works for everyone.
- Turning opt-out on adds the `menu_message` entry to the persistent menu, and it counts toward the five entries. A blank `menu_message` removes the entry and keeps keywords and AI detection on. Deleting that entry from the menu instead (`persistent_menu_manage` `delete`) turns opt-out off.
- An opted-out contact is skipped by every automation and campaign, and the status sticks. The team can still reply by hand. Only put someone back (**Remove contact from opt-out list**) when they asked.

## B8. Ice breakers and the persistent menu

**Ice breakers** (up to 4, shown when someone opens a chat with the client for the first time):

- Use the questions the client gets most, in the client's words: "How much is it?", "Can I book this week?", "Do you ship to me?", "Can I talk to someone?".
- Create with `icebreakers_manage` `create`; the response gives each one a payload. Then give each one a scenario with an ice breaker trigger on that payload (`{"trigger_type": "icebreaker", "options": {"icebreaker_payload": "PAYLOAD"}}`). The question text is filled in on save.
- Check with `icebreakers` `list`: every entry should have a non-empty `automations` list (or be answered by the agent). In the app the **Manage ice breakers** card shows "Nothing answers this" when one has no answer.
- Rewording an ice breaker with `icebreakers_manage` `update` keeps its payload, so a trigger on the payload keeps working. A trigger matching on the question text stops working when the question changes.

**Persistent menu** (always available in the chat, 5 entries or fewer including the opt-out entry, titles cut at 30 characters):

- Links to off-Instagram places (shop, booking page) as `web_url` entries. They open the page and start no automation.
- Entries that should start an automation as `postback` entries that **reuse an ice breaker's payload** (`persistent_menu_manage` `add` with `payload` set to it). The same ice breaker trigger then answers both the ice breaker and the menu tap. A postback with a payload no ice breaker has makes its trigger show an "ice breaker not found" issue, so avoid menu-only payloads unless you have checked how the scenario shows in the app.
- Read the menu back with `persistent_menu` `get`. Menus and ice breakers live on Instagram, so the read shows what people actually see.

**Run limits on button entries:** with a run limit, a second tap on the same ice breaker or menu entry gets no answer from that flow. Leave flows that are only reached by buttons without a limit, unless the client is happy with that.

## B9. Conversion links

- One link record per destination (`conversion_links_manage` `create` with `title`, `url`, `button_title`), reused by every flow. Edit it once and every flow follows.
- Add tracking parameters to every URL, for example `utm_source=instagram&utm_medium=dm&utm_campaign=automation`, plus `utm_content` where the placement matters (menu, price reply).
- Never put a raw URL in message text: links in text can be dropped by Instagram, and the editor warns about them. Send a link card. Link cards also give a "clicked" branch for tagging. Help: https://help.inro.social/en/articles/15808092
- Templates arrive with their own placeholder links copied into the client's account. Replace each URL with the client's real one before switching the flow on.

## B10. Contact properties

- Email and phone are built in. Add one to three custom properties the flows will actually save (`contact_properties_manage` `create`, for example a single-choice "Interested in" with the client's two or three offers).
- Don't add an "Other" or "Not sure" option to a property the agent detects: it will pick it too often. Let `instagram-ai-agent-setup` decide which properties the agent tracks.

## B11. Waits that read as human

- No wait before the first reply. People expect an answer.
- 5 to 10 seconds after someone types an answer (an email, a free-text reply) before the next message, and between an AI reply and a scripted follow-up, so two messages don't land in the same second.
- After a button tap: no wait, or a few seconds before a long message.
- A contact writing during a wait doesn't stop the flow ("Interrupt when contact replies" is off). A manual team reply does.

## B12. In-app steps (what the connector can't set)

**Excluded folders on a scenario.** Open **Automation → Scenarios**, open the scenario. In the editor, the **Advanced options** panel (top left) has three sections: **Limit frequency per contact**, **Interrupt on message replies** and **Exclude specific folders**. Open **Exclude specific folders** ("This scenario will not run for contacts in the selected folders"), pick the folders, then **Save scenario**. Read it back with `scenarios` `get` (`excluded_folder_ids`). Always click **Save scenario** before you close the editor.

**Account-wide exclusion.** On the Scenarios page, the **Exclude specific contacts** card ("Contacts matching these filters will be excluded from all automations") opens a contact filter. It stops every automation for matching contacts, helpers included, at every step. Keep it to one filter at most (contact status is Spam), and read the filter back before you save: a wrong filter such as "not in a folder" would switch off automation for most of the account.

**Spam.** In the inbox, select conversations and **Move to spam**, or set their status to `spam` with `contacts_manage` `bulk_update`. Spam contacts leave the main inbox.

**Human intervention and knowledge access.** See B5.

**Time-off.** Inbox settings (gear next to FOLDERS) → **Time-off**: an auto-reply to the first message anyone sends while it is on, until the last day you pick. For closures and holidays. Check how it combines with the client's welcome flow on your test account before relying on it.

## B13. Making sure the team hears about things

- Alert emails (`send_email` step) to the address the client chose for each topic. Templates arrive with an empty recipient, which shows as an issue until you fill it in.
- Folder notifications as a lighter option: inbox gear → **Manage folder notifications**, set **Needs a human** to Real time. Each team member sets their own under **Profile → Notifications**.
- To send alerts from the client's own address, it has to be authorised first under **Profile → Domain & emails** (Pro), and the owner of the address must confirm it.
