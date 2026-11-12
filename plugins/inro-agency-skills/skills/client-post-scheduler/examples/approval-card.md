# Example: one reel, scheduled, with a comment-to-DM

A fictional client: a neighbourhood bakery, @example.bakery, brand-voice file says time zone Europe/Lisbon, voice "warm, early-morning, unfussy", client signs off on every post, keyword MENU sends this week's menu.

The agency wrote: "Schedule this reel for Friday 7:30am, it's the new pastry. Add the menu DM."

## What the skill shows before doing anything

```
Client: @example.bakery (account id, from get_organization_info) | connected as @example.bakery
Action: Draft for client sign-off, then schedule for Fri 20 Nov 2026, 07:30 Lisbon time (08:30 Paris, your zone)
Type: Reel (Feed and Reels), cover from frame at 2.0 s
Media: pastel-de-nata-v3.mp4, checked: vertical 9:16, 41 MB, MP4
Caption (325 of 2,200 characters, 4 hashtags):
The tray came out at 6:12 this morning. By 6:40 there were nine left.

Same custard recipe since we opened, new shell: thinner, darker, louder when you bite it.

Comment MENU and we'll send you this week's menu in your DMs, so you know what's on before you walk over.

#lisbonbakery #pasteldenata #alfamafood #breakfastlisbon
Alt text: Hands lifting a tray of dark-topped custard tarts out of a stone oven.
Labels: AI-generated no | Paid partnership no | Trial reel no
Comment-to-DM: keyword MENU -> DM with a link card "This week's menu" to https://example.com/menu, button "See the menu", created switched off
Note for the client's AI agent: Pastéis are €1.40 each, 6 for €7.50, Friday to Sunday until sold out.
```

Approve as is, or tell me what to change.

## After "approved"

1. Upload the reel with `file_url`, `purpose: publishing`, poll until `ready`.
2. `medias_manage` `create` as a **draft** (the brand file says the client signs off), with the caption, alt text, `share_to_feed: true`, `thumb_offset: 2000`, `agent_context`, and `comment_to_dm` with `active: false`.
3. `medias` `get` to read it back; `show_scenario` on `comment_to_dm.scenario_id` to show the reply and DM text that were copied from the last automation.
4. Report: "Draft saved in Content > Posts & reels. The comment automation is attached and off. When the client OKs it, I'll set Friday 07:30 Lisbon (`2026-11-20T07:30:00+00:00`) and switch the automation on."

## After the client signs off

1. `medias_manage` `update` with `scheduled_at: "2026-11-20T07:30:00+00:00"`.
2. `medias_manage` `attach_comment_to_dm` with the post `id` and `active: true`.
3. Report the scheduled time in Lisbon time and the agency's time, and that the automation is on and listening for MENU on this post only.
