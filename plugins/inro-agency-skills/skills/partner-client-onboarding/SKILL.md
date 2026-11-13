---
name: partner-client-onboarding
description: "Onboard a new client under your Inrō agency partner account. Covers the partner dashboard side (create the client account or a managed link, the optional automation template, your logo on the connect page), getting the client to connect their Instagram, confirming the connection, then the first steps through the partner connector: a read-only baseline and the first automations, created switched off. Use when you say: onboard a new client, add a client to my partner account, create a client account, set up a managed link, send the client the Instagram connect link, the client has connected, new client on Inrō, what do I do after the client connects."
license: MIT
---

# Partner client onboarding

Bring a new client into your partner account, get their Instagram connected, and leave the account with a baseline and its first automations ready to switch on.

**Requirements.** The partner dashboard at **app.inro.social/partners**, with an active partner plan, and a payment method on file unless your plan is a lifetime agency plan (for example from AppSumo). No partner dashboard yet? It comes with the Inrō Agency Partner Program or a lifetime agency plan: see [The Inrō Agency Partner Program](https://help.inro.social/en/articles/15632327). Steps 3c and 5 to 8 also use the Inrō partner connector: `https://api.inro.social/partner/mcp`, your partner API token in an `Authorization: Bearer` header, Authentication set to "None", and every call names the client by account id or Instagram username. Accounts you create under your partner plan are served by it: on a subscription they count as Pro, and on a lifetime agency plan they show its tier (for example `appsumo_4`). **Without the partner connector:** Steps 1 to 4 work in the dashboard alone, and you can do Steps 5 to 8 with the single-account Inrō connector on that client's account (`https://api.inro.social/mcp`, OAuth, one account per connection).

Help center: [The Partner Dashboard](https://help.inro.social/en/articles/17027622), [Partner API & MCP](https://help.inro.social/en/articles/17027623), [The Inrō Agency Partner Program](https://help.inro.social/en/articles/15632327), [How to Connect Your Instagram Account](https://help.inro.social/en/articles/9424565).

## Keep the partner token safe

The partner token reaches every client account you manage. Never paste it into a chat, a document, a file or a message to a client. It belongs only in the connector's header. Regenerate it in the dashboard (**API & MCP**, **Regenerate**) when someone leaves your team or it may have leaked; the old one stops working at once, and removing someone from the team does not cancel a token they copied.

## Rules for this skill

1. **Never open a managed link yourself to check it.** Every visit creates a new client account under your partner account.
2. **A template on a managed link goes live.** The automation template you set on a managed link, or pass when creating an account through the connector, is copied into the new account and switched on: the dashboard says it is "activated as soon as Instagram is connected". So it runs on the client's real followers from the first minute. This skill's default is **no template**: take the baseline, then add automations switched off.
3. **Accounts you create are billed to your agency, not the client.** Get the user's OK before you create one, through any route.
4. **Confirm the account before any change.** `get_organization_info` with the client's account id, and check the username.
5. **Read first, plan, get an OK, then write.** New automations are created with `active: false` and switched on only on approval.
6. **Never message a real contact as a test.**
7. **On the partner connector, every call names the client.** Use the account id from `list_organizations`. There is no default account.

## Step 1. Check your partner account is ready (dashboard)

- **Plan.** Without an active partner plan you see "Start your partner plan" and cannot manage accounts. **Billing** shows your plan and when it renews, or on a lifetime plan how many of its accounts are in use.
- **Payment method.** Without one, a "No payment method" notice sits in the sidebar with **Add a payment method**. On a subscription you need it to create accounts and managed links. A lifetime agency plan needs no card; it has a fixed number of accounts instead, shown in **Billing**. Accounts you already have keep running.
- **Logo.** In **Settings**, your logo replaces the Inrō logo on the signup and onboarding pages opened from your partner links. Set it before the first client sees the connect page.
- **Team** (optional). Invite colleagues by email so they work in the partner workspace without sharing your login.

On the connector there is no call that reads your plan. `create_organization` refuses with a plain message if there is no active plan, no payment method, or, on a plan that covers a fixed number of accounts, no free account left. Fix the first two in **Billing** and try again. For the third, delete an account you no longer need, or upgrade the plan where you bought it.

## Step 2. Pick how the account is created

| Route | Where | Automation template | Link the client opens | If the client never connects |
|---|---|---|---|---|
| A. Create account | Dashboard | None | The **Connect** button on the new card | The empty account stays until it is deleted |
| B. Managed link | **Partner links**, **New link**, type **Managed** | Optional, switched on | The managed link itself | Removed automatically after about an hour; the client can open the link again |
| C. Partner connector | `create_organization` | Optional, switched on | `instagram_connect_url` in the response | The empty account stays until it is deleted |

- One client, now: **A**. Simplest, and nothing runs until you build it.
- A link you can put in a proposal or onboarding email, or one per offer: **B**. The **Partner links** list shows how many **Accounts** each link brought in and how many are **Paying**.
- From chat or a script: **C**.

**Referral links are not onboarding a managed client.** A referral link sends people to the normal signup page: the client creates their own account and pays for it, and it is not yours to manage, so the partner connector cannot reach it. **Trial days** and **Discount code** are settings of referral links only. A managed account is on your partner plan from the start, so it has no trial and no coupon.

## Step 3a. Create the account in the dashboard

1. On the **Dashboard**, click the **Create account** tile, type the **Account name** (the client's brand), and click **Create**. Once Instagram is connected, the Instagram profile name replaces it.
2. The new card reads **Not connected** and has a **Connect** button. It opens that account's connect page. Copy that page's address and send it to the client (Step 4).

## Step 3b. Create a managed link

1. Open **Partner links** and click **New link**. Choose **Managed**.
2. **Automation template:** leave it on **No template** (Rule 2). If you do pick one, it comes from the automations in your accounts, so build and check it there first, and agree with the client that it runs from day one.
3. **Hide the template notice:** the connect page tells the client which automation is being set up for them. Leave the notice on if you use a template.
4. Save, then copy the link with the copy icon in the **Partner links** list. Send it to the client (Step 4). Do not open it yourself.

A link's type cannot be changed after it is created. Make a new link for the other type.

## Step 3c. Create the account through the partner connector

1. `list_organizations`. Check the client is not already there (same name, or an earlier attempt that never connected). Reuse an unconnected one rather than creating a second.
2. Agree the name with the user and get their OK (Rule 3).
3. `create_organization` with `name` only. It also accepts `partner_link_code` (the code in a managed link's address, after `/p/`) to attribute the account to that link and copy its template, and `template_id` (an automation in one of your accounts) to copy it in. Both copies are switched on, so leave them out unless the user asked for them (Rule 2). A `template_id` that is not one of your accounts' automations is skipped without an error, and the connect page of this route does not tell the client about the template.
4. The response has the account `id`, `instagram_connected: false` and an `instagram_connect_url`. Write down the id: the account has no username until Instagram connects, so the id is the only way to name it. Its `subscription_tier` can read `free`; the account still works, reads and writes included. Send the URL to the client (Step 4).

## Step 4. The client connects Instagram

Send the client the link from Step 3 with the short checklist in `references/client-messages.md`. What they need to know:

- They need an Instagram **Business or Creator** account. A personal account cannot connect.
- Use a desktop browser. On the page, type their Instagram username and click **Find Instagram account**, then **Authenticate with Instagram** and approve every permission. If the page says the account is already connected to another Inrō account (their own, or a previous agency's), stop and sort that out first.
- Connecting does not give them access to your Inrō account.
- On a managed link, finish within about an hour, or open the link again.

Connecting is a sign-in only the account owner can do. You cannot finish it for them through the connector.

## Step 5. Confirm the connection

- **Dashboard:** the client's card reads **Connected**. **Limited** means some permissions are missing: send the link behind the card's **Reconnect** button and ask them to approve every permission. **Restricted** means Instagram restricts sending from the account. **Error**, **Disconnected** or **Not connected** mean nothing will run yet.
- **Connector:** `get_organization` with the account id, or `list_organizations` with `connected: true`. Wait for `instagram_connected: true` and a `username`. Check when the client says they are done, then every few minutes. Do not poll in a tight loop.

Then call `get_organization_info` with `organization: <id>` and say back:

- the username, and confirm with the user it is the client's real handle;
- `subscription_tier` (on a subscription `pro`, on a lifetime plan its tier, for example `appsumo_4`; a brand-new account can still read `free` while it works);
- the connection state: `login_error_data` empty, any `instagram_restrictions`;
- `can_publish` and `missing_publish_scopes`, only if you will publish posts for them.

If the username is not the client's, stop. Nothing else happens on that account until it is sorted out.

## Step 6. Baseline (read only)

On the confirmed account, read and save what is already there. Every call carries `organization: <id>`:

- `scenarios` `list` (a template copy shows up here, switched on), `campaigns` `list`
- `icebreakers` `list` and `persistent_menu` `get`
- `settings` `get_optout`
- `agent` `get`
- `contact_properties` `list` and `folders` `list`

Write a short baseline note with the format in `references/client-messages.md`. For a full read of an account that already has a history on Instagram, run `instagram-account-audit`.

If a template was copied in and is on, show it with `show_scenario`, tell the user it is live, and offer to switch it off (`scenarios_manage` `update`, `active: false`) until it is reviewed.

## Step 7. First automations, switched off

1. Agree two or three starting automations with the user. `dm-funnel-planner` helps pick them; `inbound-dm-playbook` covers the inbound basics.
2. Build each one switched off: from a gallery template (`search_templates`, then `scenarios_manage` `create` with `template_id` and a title; the copy starts off) or with `dm-flow-builder`. Replace every example link and name in a template with the client's own. A template copy can also add the contact folders its steps use, and can show an `issue` warning (such as an empty alert email) until the client's values are in. If search does not return a template you expect, open its share page: if it shows the flow, the id copies normally.
3. Show each with `show_scenario`. Switch one on (`scenarios_manage` `update`, `active: true`) only when the user says so for that automation.
4. AI agent: `instagram-ai-agent-setup`. The full first-week setup checklist: `client-account-setup`.

## Step 8. Hand-off

- Record for the user: account id, username, route used (A, B or C), the managed link code if any, date connected, and what is on. No token.
- Add the client to the weekly check with `multi-client-health-check`.
- Tell the client what is live on their account and what is waiting for their OK.

## Cleaning up

- **An account with no Instagram connected** can be deleted with `delete_organization` and the account id, after the user's OK. It works only on an account that never connected Instagram (`can_be_deleted: true` in `list_organizations`), deletes everything in the account, and cannot be undone. The partner dashboard has no delete button for accounts.
- **A connected account** cannot be deleted through the partner connector. It is a live client account.
- **Managed link visits** that never connected are removed automatically.

## Check in the partner dashboard or the app

- Whether your client can also log in to their own account, and who can invite them (**Profile**, **Team members** inside that account): check in the app.
