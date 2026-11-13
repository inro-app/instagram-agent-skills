---
name: partner-bulk-rollout
description: "Roll one change out across many client Instagram accounts through the Inrō partner connector, safely and one client at a time. Covers an automation from a template or copied from one client, a fix to an existing automation, the same ice breakers or persistent menu entry, a contact property, opt-out keywords, a contact or automation folder, and a draft campaign. Reads every target account first, shows a per-client plan with duplicates and conflicts for your approval, applies it client by client with new automations switched off, and ends with a results table and a rollback list. Use when you say: roll this out to all my clients, copy this automation to every account, add these ice breakers to these clients, push this fix everywhere, same change across my accounts, bulk update client accounts, apply this to the clients on my list."
license: MIT
---

# Partner bulk rollout

One change, many client accounts, no surprises. There is no call that changes several accounts at once. You loop over the clients yourself, one at a time, and every call names the client it is for.

**Requirements.** The Inrō partner connector: `https://api.inro.social/partner/mcp`, with your partner API token in an `Authorization: Bearer` header and the connector's Authentication set to "None". Every call names the client account by its account id or Instagram username. Each client account must be on Pro (monthly or annual), a free trial, or a lifetime plan; accounts you created under your partner plan are covered by it. Free accounts, and accounts whose plan lapsed after a failed payment, are refused. **Without it:** you can run the same steps with one Inrō connector per client (`https://api.inro.social/mcp`, OAuth, one account per connection, client on one of those plans). Your Claude app allows one connector per URL, so give each one a unique dummy query string, for example `https://api.inro.social/mcp?client=acme`. It is slower, and Step 0 becomes "confirm which account each connector is on with `get_organization_info`".

Help center: [Partner API & MCP](https://help.inro.social/en/articles/17027623), [The Partner Dashboard](https://help.inro.social/en/articles/17027622).

## Keep the partner token safe

- The partner token reaches every client account in your partner workspace. Whoever holds it can read and change all of them.
- Never paste it into a chat, a prompt, a document, a sheet or a file. It belongs only in the connector's header setting.
- If the token shows up in a conversation, stop and tell the user to regenerate it before doing anything else.
- Regenerate it in the partner dashboard (**API & MCP**, **Regenerate**) when someone leaves your team or the token may have leaked. The old token stops working at once, and every connector and script using it needs the new one. Removing someone from the team does not cancel a token they already copied.

## Rules that never bend

1. **Every call names the client** in the `organization` argument. Use the account id from `list_organizations`, not the username: a username can match more than one account (the call is then refused), and an account that has not connected Instagram yet has no username at all. Never rely on a default or on "the client from the last call". There is no default.
2. **Read before you write.** Every client gets a dry run before anything changes.
3. **The user approves the per-client plan**, and the approval names the clients ("all 8 in the table" or a list). An OK for three clients is not an OK for ten.
4. **New automations are created switched off** (`active: false`). They go live only when the user says so, per client.
5. **Some changes are live the moment you make them.** Ice breakers, the persistent menu, opt-out settings and edits to an automation that is already on have no "off" state. Mark them "Live on approval" in the plan.
6. **Never message a real contact as a check.** No `send_message`, no campaign `send` or `test`, no scenario `test` or `trigger`. Read the record back instead.
7. **Never delete without explicit approval** for that record on that client. Rollback starts with switching off, not deleting.
8. **One client at a time.** Write, read back and log client A before you touch client B.
9. **Stop on the first unexpected error for a client.** Report what was already done there. Continue with the other clients only if the user agrees.

## Step 0. Confirm the connector and the client list

1. Call `list_organizations`. If that tool does not exist, you are on a single-account connector, not the partner one. Say so and stop, or switch to the per-client route above.
2. Show the user a table: account id, username, name, `instagram_connected`, `subscription_tier`.
3. Ask which clients are in scope: all of them, a list, or a filter ("the gyms", "everyone except X"). Resolve every name to an id from this table. Ask about any name that matches no row or more than one row.
4. Put aside, and list separately, every account where `instagram_connected` is false (nothing can run there yet). Do not set an account aside for its `subscription_tier` alone: the tier can lag the real plan, and a new partner account can read `free` and work normally. An account whose calls are refused ("... is not on a Pro or Trial subscription, so it cannot be managed through the API") goes aside when the Step 2 reads show it.

## Step 1. Write the change down once

Agree a change spec before you read any client. Use the template in `references/tables.md`.

- **What:** one of the change types below.
- **Source:** a gallery template (its id from `search_templates`), an automation in one client account (account id and scenario id, read with `scenarios` `get`), or a written definition.
- **Exact content:** titles, message text, buttons, keywords, menu labels, property type and choices.
- **Per-client values:** anything that differs by client (a link, a booking page, a product name, a language). Get them from the user as a table up front. Never guess a client's link.
- **Duplicate rule:** what counts as "already there" (same title, same keyword, same ice breaker question, same property title).
- **End state:** switched off (the default), or switched on after a separate approval.

| Change | Read | Write | Live when written? |
|---|---|---|---|
| Automation from a gallery template | `search_templates`, `scenarios` list | `scenarios_manage` create with `template_id` | No, the copy starts off |
| Automation copied from one client | `scenarios` get on the source | `scenarios_manage` create with `triggers` and `actions`, `active: false` | No |
| Fix to an existing automation | `scenarios` get | `scenarios_manage` update | Yes, if that automation is on |
| Ice breakers | `icebreakers` list | `icebreakers_manage` create or update | Yes |
| Persistent menu entry | `persistent_menu` get | `persistent_menu_manage` add or update | Yes |
| Contact property | `contact_properties` list | `contact_properties_manage` create | Exists at once, sends nothing |
| Opt-out keywords or messages | `settings` get_optout | `settings_manage` update_optout | Yes |
| Contact folder or automation folder | `folders` list, `scenario_folders` list | `folders_manage` or `scenario_folders_manage` create | Exists at once, sends nothing |
| Draft campaign | `campaigns` list | `campaigns_manage` create | No, it stays a draft until someone sends it |

The resource tools take `action` and `action_params`, plus `organization` on the partner connector. The checks, write calls, read-backs and rollback for each type are in `references/change-types.md`. Read the section for your type before Step 2.

Before you build automation steps or triggers, call `get_action_types` and `get_trigger_types` (on the partner connector they also take `organization`; use the first client in scope). The live answer beats anything written here.

**Not covered here.** AI agent instructions are different for every client: change them client by client with the `instagram-ai-agent-setup` skill. Sending a campaign is a separate decision for each client and is never part of a rollout.

## Step 2. Dry run, client by client (read only)

For each client in scope, in order:

1. Call `get_organization_info` with `organization: <id>`. Check the username is the one in your table and the connection is healthy (`login_error_data`, `instagram_restrictions`). If anything does not match, stop and ask. If the call is refused for the plan, the client is **Blocked**.
2. Read what the change touches, as listed for its type in `references/change-types.md`.
3. Put the client in one bucket:
   - **New:** nothing like it exists. Ready to create.
   - **Duplicate:** it is already there by the duplicate rule. Skip.
   - **Conflict:** something close but different exists. Examples: another active automation already triggers on the same keyword or ice breaker, the client already has 4 ice breakers, the menu already has 5 entries, a property with the same title has a different type.
   - **Blocked:** not connected, refused for its plan, or a per-client value is missing.
4. Write down exactly what you would create or change, with the title it would carry and what it would replace.

Write nothing in this step. Ten clients means ten sets of reads. That is the point.

## Step 3. The per-client plan

Show one table, one row per client (format in `references/tables.md`): account, bucket, the exact action, live or off after the write, and the per-client values you will use.

- Every **Conflict** needs the user's decision for that client: skip, rename, or replace. Never pick for them.
- Flag every row where the change is live the moment it is written.
- Ask for approval in a way that names the clients: "Approve these 7 clients? Tell me any to drop." Proceed only on a clear yes for that list.
- Save the plan as a file the user keeps (for example `rollout-YYYY-MM-DD-plan.md`). Never put the token in it.

## Step 4. Apply, one client at a time

For each approved client, in the order of the plan:

1. Call `get_organization_info` with the id again. Same username as in the plan? Go on. If not, stop.
2. Make the write with `organization: <id>`. For automations, set `active: false` and the agreed title.
3. Read it back (`scenarios` get, `show_scenario`, `icebreakers` list, `persistent_menu` get, and so on) and check it matches the plan. For a new automation, check the `warnings` in the create response: a warning with severity `issue` means the steps will not run as written. Warnings the plan listed as expected (for example "Email address is empty" on a template's alert step, until the client's address is in) are not a stop. Any other `issue` is.
4. Log the row: client, what was done, the new record's id, and the read-back result.
5. **If anything unexpected happens** (a refusal, a validation error, a read-back that differs from the plan), stop for this client. Do not retry with changed input. Record what was already written on this client. Ask the user: fix and retry this client, skip it, or stop the whole rollout. Continue with the next client only on their answer.

If a call fails with a timeout or a "too many requests" error, read first to see whether the write landed before you try again. Never repeat a create blindly: you would make a duplicate.

## Step 5. Results and rollback list

When the last client is done, or the user stops the rollout, show:

- **Results table:** every client in scope with its outcome (done, skipped as duplicate, skipped by decision, blocked, stopped on error) and the new record ids.
- **Rollback list:** for each record created or changed, how to undo it. Switch off a new automation. Delete an ice breaker by its payload. Put back the previous menu, opt-out keywords or automation steps from the values you saved in the dry run. A deleted property loses all its values, so deleting one is never automatic. List anything a template copy created besides the automation (contact folders, links, files, surveys): deleting the automation does not remove them.
- **What is still open:** clients blocked or stopped, conflicts left for later, anything that needs the app.

Save both tables next to the plan. Formats are in `references/tables.md`.

## Step 6. Switching on (separate approval)

Only when the user asks, and per client:

1. Check again for other active automations on the same keyword, ice breaker or menu entry on that client.
2. Call `scenarios_manage` update with `id` and `active: true`, then read it back.
3. Suggest switching on one client first, checking it for a day with `scenarios` `performance` or `executions`, then doing the rest.

## Use another skill when

- One client only: `dm-flow-builder` or `client-account-setup`.
- A weekly check across all clients: `multi-client-health-check`.
- A new client account: `partner-client-onboarding`.
- Deciding what a client should get in the first place: `dm-funnel-planner` or `instagram-account-audit`.

## References

- `references/change-types.md`: per change type, what to read, how to spot duplicates and conflicts, the write, the read-back and the rollback.
- `references/tables.md`: the change spec, the per-client plan, the results table and the rollback list.
