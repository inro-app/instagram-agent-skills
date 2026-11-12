# Change types: checks, writes, read-backs, rollback

Every call below runs on one client and carries `organization: <account id>`. The resource tools take `action` and `action_params`. If a live tool description disagrees with this file, the live description wins.

Before Step 2, save a copy of whatever you are about to change on each client (the current automation, ice breakers, menu, opt-out settings). That copy is your rollback.

## Automation from a gallery template

**Find the template.** `search_templates` with `type: "Scenario"` and a plain-words `query` ("collect emails from comments"). On the partner connector it also needs `organization`: use any client in scope, the gallery is the same for all. Show the user the matches and agree on one template id.

**Dry run per client.**
- `scenarios` `list` with `search` set to the template title. A match by the duplicate rule means **Duplicate**.
- Look at the client's active automations whose triggers could overlap (same keyword, same ice breaker, same post). Open them with `scenarios` `get`. Overlap means **Conflict**.

**Write.** `scenarios_manage` `create` with `template_id` and the agreed `title`. A copy made from a template starts switched off. It arrives outside any folder.

**After the write.** Templates carry example links, names and wording. Open the copy with `scenarios` `get` and `show_scenario`, then replace every example value with the client's own (`scenarios_manage` `update`, see "Fix to an existing automation" for the rules). Nobody switches it on until those values are in.

**Rollback.** `scenarios_manage` `update` with `active: false`. Deleting (`scenarios_manage` `delete`) is permanent and needs the user's explicit OK for that record.

## Automation copied from one client to others

Build and check it once, in your own agency account or in one client, then copy it. The help center calls this "duplicate or migrate between accounts": read the full definition, then create it again from JSON in each target ([Build and Update Automations via API & MCP](https://help.inro.social/en/articles/14963455)).

**Read the source.** `scenarios` `get` with the source account id and the scenario `id`. You get the full `triggers` and `actions`. Save it.

**Turn it into a create payload.**
- Drop the record ids. Keep each step's `action_key`, `parent_key` and `parent_branch`: they hold the tree. If a step has no `action_key`, give it a short unique one and set its children's `parent_key` to match.
- Call `get_action_types` and `get_trigger_types` if any step or trigger is unfamiliar.

**Replace what belongs to the source account.** These do not carry over and must be swapped for the target client's own:
- **Media in a message step:** pass it inline as `media_file` with a `file_url` the user gives you, or reference a file already in the target account by `id`.
- **Tracked links:** pass a `conversion_link` inline with the client's own URL, or reference one that exists in the target.
- **Contact folders, properties, segments and surveys:** find or create the same one in the target, then use its id or slug. Folders and surveys can be created inline inside a step, but reuse the target's existing one with the same name so you don't make duplicates.
- **Post-specific comment triggers:** a post belongs to one account. Pick the target client's own post with the user, or use a trigger option that is not tied to one post.
- **Text that names the source client:** brand names, prices, links, language.

**Dry run per client.** Same duplicate and overlap checks as for a template. Also mark **Blocked** if a per-client value (link, file, post) is missing.

**Write.** `scenarios_manage` `create` with `title`, `active: false`, `triggers` and `actions`, plus any scenario settings the source had and you agreed to copy (for example `scenario_type`, rate limit settings).

**Read-back.** Check the `warnings` on every action in the create response. A severity of `issue` means the tree will run differently from how it reads: fix and update before you go on. Then `show_scenario` so the user can see the flow.

**Rollback.** Switch off with `scenarios_manage` `update` and `active: false`. Delete only with explicit approval.

## Fix to an existing automation

**Find it on each client.** `scenarios` `list` with `search`. Titles can differ between clients, so confirm each match with the user. Then `scenarios` `get` and save the full definition: it is the rollback.

**Rules that bite.** ([Updating Scenario & Campaign Actions](https://help.inro.social/en/articles/15075798))
- `actions` on update is the complete list. Any existing step you leave out is deleted. Send every step, with the `id` of each step you keep.
- `triggers` on update: a list where no item has an `id` replaces every trigger. Replaced triggers get new ids and a webhook trigger loses its URL. Include the `id` of each trigger you keep.
- A change to an automation that is on is live at once. Mark the row "Live on approval".
- If the fix is only the title or the on/off state, send only that field.

**Write.** `scenarios_manage` `update` with `id` and the fields that change.

**Read-back.** `scenarios` `get`, compare with the plan, check `warnings`.

**Rollback.** `scenarios_manage` `update` with the saved definition.

## Ice breakers

The tappable questions on the client's Instagram profile. They live on Instagram, so every action reads them back from Instagram. Instagram allows up to 4. See [Ice Breakers & Persistent Menu](https://help.inro.social/en/articles/15631969).

**Dry run per client.** `icebreakers` `list`. Each entry has a `question`, a `payload` and the `automations` that fire when it is tapped.
- Same question (ignoring case and punctuation): **Duplicate**.
- Already 4: **Conflict** (which one goes, if any, is the user's call).
- Replacing or rewording one that has automations: **Conflict**. Rewording keeps the payload, but an automation matching on the old title stops firing.

**Write.** `icebreakers_manage` `create` with `question`. The response returns the new `payload`. An ice breaker answers nothing until an automation triggers on it, so pair it with an automation (an `icebreaker` trigger matching that payload), created switched off as usual. To reword, `icebreakers_manage` `update` with `payload` and `question`.

**Live.** It shows on the client's profile as soon as it is written.

**Rollback.** `icebreakers_manage` `delete` with the `payload`, after the user's OK, or `update` back to the saved question.

## Persistent menu entry

The menu inside the client's Instagram DM thread. It lives on Instagram. Keep it to 5 entries; titles are cut to 30 characters.

**Dry run per client.** `persistent_menu` `get`. Each entry has an `id`, `type`, `title`, `payload`, `url` and `source`.
- Same title or same URL: **Duplicate**.
- Already 5 entries: **Conflict**.
- Never touch the opt-out entry. It is kept in step with the opt-out setting, and deleting it turns opt-out off for that client.

**Write.** `persistent_menu_manage` `add` with `title` and `type`: `postback` (set `payload` to an existing ice breaker's payload, so that ice breaker's scenario answers it; a trigger on a menu-only payload shows an issue) or `web_url` (opens a link, starts no automation; needs `url`). To change an entry, `persistent_menu_manage` `update` with `id` and the new `title` or `url`.

**Live.** Visible in the client's DMs as soon as it is written.

**Rollback.** `persistent_menu_manage` `delete` with the entry's `id` after the user's OK, or `update` back to the saved values.

## Contact property

**Dry run per client.** `contact_properties` `list`.
- Same title: **Duplicate**.
- Same title but a different type or different choices: **Conflict**.

**Write.** `contact_properties_manage` `create` with `title` and, as agreed, `property_type` (the allowed values are in the tool's schema; the default is text), `choices`, `description`, `agent_active`, `auto_detect`.

Do not run `backfill` as part of a rollout unless the user asks for it by name. It works through existing contacts in the background and spends AI credits on accounts that have them.

**Rollback.** `contact_properties_manage` `delete` with the `slug` removes the property and every value stored in it, and cannot be undone. Only with explicit approval, and only if no values were collected yet.

## Opt-out keywords and messages

**Dry run per client.** `settings` `get_optout`. Save `active`, `keywords`, `menu_message`, `confirmation_message`, `ai_detection`.

**Write.** `settings_manage` `update_optout` with only the fields that change. `keywords` replaces the whole list, so send the client's current keywords plus the new ones, never the new ones alone. Turning `active` on adds the opt-out entry to the persistent menu; turning it off removes it.

**Live.** Applies at once.

**Rollback.** `settings_manage` `update_optout` with the saved values.

## Contact folder or automation folder

**Contact folders.** Dry run with `folders` `list` (same name is a **Duplicate**). Write with `folders_manage` `create`, `name` and an optional `color` from the allowed list. Deleting a folder never deletes its contacts.

**Automation folders.** Dry run with `scenario_folders` `list`. Write with `scenario_folders_manage` `create`, `name`, `description`, `folder_type`. The default type is `priority`, where only the highest-priority matching automation in the folder runs; a `normal` folder runs every match. Say which one you are creating and why, because it changes how automations moved into it behave.

**Rollback.** `folders_manage` `delete`, or `scenario_folders_manage` `delete` with `action_type: "ungroup"` so the automations stay. Both after the user's OK.

## Draft campaign

**Dry run per client.** `campaigns` `list` with `search` (same title is a **Duplicate**). Read the client's contact folders and segments (`folders` `list`, `segments` `list`) to find the audience by name: a campaign rule points at a folder or segment id, and ids differ on every client. No matching audience means **Blocked**.

**Write.** `campaigns_manage` `create` with `title` and either a `template_id` (from `search_templates` with `type: "Campaign"`) or `actions` and `campaign_rules`. Each rule has `list_type` (`folder` or `segment`), `rule_type` (`inclusion` or `exclusion`) and that client's own `destination_id`.

**Never in a rollout.** `campaigns_manage` `send` and `test` both message real people. A campaign stays a draft until someone sends it, and sending is a decision for each client on its own.

**Read-back.** `campaigns` `get`, then `show_campaign` so the user sees the flow, destinations and audience.

**Rollback.** The connector has no delete for campaigns. Leave the draft unsent and remove it in the app if it is not wanted (check in the app).
