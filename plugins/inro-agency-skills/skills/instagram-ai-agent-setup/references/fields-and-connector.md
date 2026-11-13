# Fields, limits and connector calls

The current shape of the Inrō AI agent, field by field, and how to read and write it through the connector. If a live response disagrees with this file, the live response wins: tell the user this file needs updating.

## Tools

| Tool | Actions |
|---|---|
| `agent` (read only) | `get`, `list_items` (`page`, `per_page` up to 100), `list_actions`, `list_contact_properties` |
| `agent_manage` (writes) | `update`, `create_item`, `update_item`, `delete_item`, `create_action`, `update_action`, `delete_action`, `create_contact_property`, `delete_contact_property` |

Every call takes `action` plus an `action_params` object. On the partner connector, every call also names the client.

`get` returns the whole agent: settings, `rules`, `items`, `actions`, `contact_properties`, plus read-only `model`, `reasoning` and `context_migrated`.

`update` changes only the fields you send. Lists inside it (`rules`, `message_examples`, `trigger_intents.intents`, `folder_rules.folder_ids`, `built_in_property_access`) are replaced by what you send. Any `update` also sets `setup_completed: true` unless you send it yourself. The `update` response is the whole agent, the same as `get`, so it can serve as your read-back. Both include the full text of every knowledge item, so on an account with long items each read is large: don't add a `get` after every small write.

## Profile and rules (Voice and personality, Goal and instructions)

| App label | Field | Type and limit | Notes |
|---|---|---|---|
| Profile | `about` | text, 500 characters. This is the app's limit: the connector does not refuse longer text, so count before you send | Always in the prompt. Who the account is, what it offers, who it talks to. |
| Message length | `message_length` | `10`, `25` or `50` (Short, Normal, Long) | Words per message. The agent may send a reply as a few short messages. |
| Auto-like positive messages | `auto_like` | boolean | Hearts incoming messages that read as friendly. |
| Message examples | `message_examples` | list of text | Always in the prompt. No fixed cap in the app. |
| Voice rules | `rules` with `kind: "voice"` | each rule 300 characters, up to 50 | How it writes. |
| Goal | `goal` | text, 500 characters. The app's limit, not enforced by the connector | Used only when the agent handles a conversation on its own. Replaced by an automation's task; not used for comment replies. |
| Instructions | `rules` with `kind: "instruction"` | each rule 300 characters, up to 50 | Always applied, in DMs, automations and comment replies. Stated to the model as taking precedence over the knowledge. |

The two rule kinds are a split for the app and the prompt layout. Both apply on the same paths, so a rule filed under the wrong kind still applies, but keep them clean: content in Instructions, style in Voice rules.

### Writing rules through the connector

`rules` replaces the whole list. Each entry is `{ "kind": "voice" | "instruction", "text": "...", "id": <existing id, optional> }`. Keep an existing rule by sending its `id`; omit `id` to add a rule; leave a rule out to delete it. Order sets position within each kind. To change one rule, send the full list from `get` with that rule edited.

```json
{
  "action": "update",
  "action_params": {
    "about": "...",
    "goal": "...",
    "message_length": 25,
    "rules": [
      { "id": 101, "kind": "instruction", "text": "Never quote a price. Say prices depend on the project and offer to send the price guide." },
      { "kind": "instruction", "text": "If asked whether you are a person, say you are the account's automated assistant and offer to pass them to the team." },
      { "id": 102, "kind": "voice", "text": "Write in short sentences, the way people type DMs on a phone." }
    ]
  }
}
```

## Activation rules

| App label | Field | Values |
|---|---|---|
| All pending messages | `trigger_mode: "all_messages"` | Replies to every DM no automation answered. |
| Specific intents only | `trigger_mode: "specific_messages"` | Replies only when a DM matches an intent. New agents start here, with no intents, which means silent. |
| Automation only | `trigger_mode: "automation_only"` | Replies only through automations (for example during a Hand over to AI Agent step). |
| Disable all replies | `trigger_mode: "never_reply"` | Never sends anything, including AI steps in automations. |
| AI-detected intents | `trigger_intents: { "intents": [...] }` | Plain-language phrases. Matched by AI, so paraphrases count. Any one match is enough. |
| Limit replies based on contact folders | `folder_rules: { "folder_rule_type": "include" or "exclude", "folder_ids": [...] }` | Labels: Only reply to contacts in these folders / Never reply to contacts in these folders / Don't limit replies based on folders. Applies to the agent's own replies, not to AI steps in automations. With no limit set, `get` returns `{folder_ids: []}` without `folder_rule_type`; send `{folder_ids: []}` to remove a limit. |

Behaviour worth knowing:

- Automations come first. The agent does not reply if a scenario replied already, and does not interrupt a running scenario.
- After an intent match, the agent keeps that thread until 24 hours pass with no activity.
- The agent does not reply to messages with no text, or when a newer message already came in.
- The setup wizard offers only All pending messages and Specific intents only. The other two are on the Activation rules card.

## Knowledge (Knowledge access and behaviour, Training and knowledge)

| App label | Field | Notes |
|---|---|---|
| Always have an answer | `no_reply_active: false` | Also answers from the model's general knowledge. The app warns this can produce irrelevant or wrong replies. |
| Limit to instructions | `no_reply_active: true` | Answers only from instructions and knowledge; otherwise says it doesn't know. |
| If the agent cannot reply, trigger this automation | `no_reply_scenario_id` | Runs only with Limit to instructions. |

To clear `no_reply_scenario_id` or `request_human_scenario_id`, send `""`: the connector refuses `null`, and the field then reads back as `""`. A backup that shows `null` is restored the same way.

Knowledge items (`create_item`, `update_item`, `delete_item`):

| App source | Connector | Notes |
|---|---|---|
| Manual text | `item_type: "text"`, `text` | The app caps manual text at 5,000 characters. |
| Website | `item_type: "url"`, `source_url`, `crawl_source_url` | App toggle: "Automatically find other pages on this website". Off imports one page. |
| Text document | not available | Upload .txt, .pdf, .doc or .docx in the app. Shows as `item_type: "file"` on read. |
| Include this information in all Agent requests | `retrieval: false` | Always in the prompt instead of retrieved. In the app it needs the account's own OpenAI key, and it makes replies slower. Keep it to a short item, if any. |

Each item goes through `processing` to `ready`, or `failed` (unreadable file, a scan with no text, a page that could not be reached). Check status with `list_items` after creating.

## Actions and automations (intent actions)

`create_action` needs `trigger`, `target_type`, `target_id`. The connector does not check that the target exists: an action pointing at a wrong id is accepted without an error. Read each target first: a scenario with `scenarios` `get`, a folder with `folders` `list`, a link with `conversion_links` `get`. A survey's id is shown only on an existing scenario's survey step (`scenarios` `get`).

| App label | `target_type` | What happens |
|---|---|---|
| Send a conversion link | `ConversionLink` | The link goes out with the agent's reply. |
| Add to folder | `Folder` | The contact is added to the folder; the contact sees nothing. |
| Start an automation scenario | `Scenario` | Runs the scenario. If it sends messages itself, the agent steps back. |
| Send a survey | `Survey` | Sends the survey. |

`trigger` is the intent, written as the rest of "When contact wants to...", for example "book a discovery call". Several actions can fire on one message. Actions fire whenever the agent itself replies, on its own or during a handover.

## User data collection

`create_contact_property` takes exactly one of `field_name` (`email` or `phone`) or `contact_property_id` (a custom property). `delete_contact_property` stops detection; values already saved stay.

- The agent saves a value only while the property is empty for that contact. The first value sticks.
- On single or multiple choice properties, only one of the defined choices is saved.
- `built_in_property_access` (`["email"]`, `["phone"]`, both or none) lets the agent read those built-in fields when replying.
- A custom property's **Accessible by AI agent** switch (`agent_active` on `contact_properties_manage`) lets the agent read its value when replying. Its description guides detection. The connector does not return either, so check them in the app (Contacts, the property's settings).
- Properties also have **Detect automatically** (`auto_detect`), which fills empty values from profiles and conversations without the agent and uses AI credits on metered plans. That belongs to account setup; see `client-account-setup`.

## Human intervention

| App label | Field | Values |
|---|---|---|
| Pause the agent when a team member replies | `human_takeover_active` | default `true`. Replies from the Inrō inbox or the Instagram app both count. |
| Pause the agent for | `human_takeover_pause` | `1`, `4`, `12` or `24` hours, default 1 |
| If contact asks to speak to a human, trigger this automation | `request_human_scenario_id` | Optional. Detection itself is always on. |

When a contact asks for a person in a conversation the agent is replying to, the agent says it will connect them and stops. The conversation is marked as human requested and the agent stays out until a team member replies.

The agent starts a connected scenario (here, under cannot-reply, or from an intent action) whether or not it is switched on. A switched-off one stops before its first step, with run reason `scenario_not_active`: nothing is sent and nobody is told. The connector accepts a switched-off scenario in these settings without a warning, so check `active` on each one before go-live.

## Read only through the connector

| Field | Where to change it |
|---|---|
| `model` | App: **Billing & usage**, **OpenAI API Key** card. Options: Fast, Balanced, Smart. Only applies with the account's own OpenAI key. `null` means the plan default. |
| `reasoning` | Same card: Low, Medium, High. Higher is slower. `null` means the plan default. |
| `context_migrated` | Not editable. `false` means the agent still uses the legacy fields below. |

## Legacy fields

Agents set up before the current fields existed held these. They are used only while `context_migrated` is `false`, and they are converted automatically when the agent is opened in the app or when `about`, `goal` or `rules` are written through the connector.

| Legacy field (old app label) | Now |
|---|---|
| `role` (Role and behaviour) | Fold the stance into Profile and the Instructions |
| `account_type` (Account type) | Profile |
| `description` (Account description, 120 characters) | Profile |
| `audience_type` (Audience type, 80 characters) | Profile |
| `goals` (Goals and capabilities, 5 of 60 characters) | Goal (one field, 500 characters) |
| `chat_instructions` (Other instructions, 640 characters) | Instructions, one rule each |
| `style_rules` (Style rules, 640 characters) | Voice rules, one rule each |

The conversion can add one knowledge item that is always included (`retrieval: false`), holding text too long for a rule. After a conversion, read the new rules and that item, remove duplicates (with approval) and check nothing contradicts.

## AI steps in automations

These run on the agent's Profile, rules, examples and knowledge. Building them is covered by `dm-flow-builder`; this is only what they inherit.

| Step | Own settings | Uses Goal? |
|---|---|---|
| AI Agent auto-DM | Message length 10, 25, 50 or 100 words | Yes |
| AI Agent message | Instructions for this message (`agent_task`), message length 10, 25, 50 or 100 | Only without its own instructions |
| AI Agent auto-comment | Comment length 5, 10 or 25 words | No |
| Hand over to AI Agent | Task, follow-up, expiration; branches Task completed and Handover expired | Only when no task is set; a task replaces it |

All of them stop when the activation mode is Disable all replies, and use AI credits on metered plans.
