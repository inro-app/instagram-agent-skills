# Inrō skills for agencies

Claude skills for agencies that run Instagram DM automation for their clients with [Inrō](https://inro.social/?utm_source=agency-kit&utm_medium=referral&utm_campaign=agency-skills-repo). They help you audit a client's account, plan and build the automations, set up the AI agent, report every month, and look after many clients at once.

Each skill is a set of instructions Claude follows step by step, with safety checks built in: it confirms which account it's working on, reads before it changes anything, shows you the plan, and waits for your OK before it writes.

Part of the Inrō Agency Automation Kit (templates, a free audit and the partner program).

## The skills

<!-- SKILLS:START -->
| Skill | What it does | Download for claude.ai |
|---|---|---|
| **Set up a client** | | |
| [`client-account-setup`](plugins/inro-agency-skills/skills/client-account-setup/SKILL.md) | Set up a client's Instagram DM automation in Inrō end to end, or take over an account someone else built. | [client-account-setup.zip](downloads/client-account-setup.zip) |
| [`partner-client-onboarding`](plugins/inro-agency-skills/skills/partner-client-onboarding/SKILL.md) | Onboard a new client under your Inrō agency partner account. | [partner-client-onboarding.zip](downloads/partner-client-onboarding.zip) |
| [`instagram-ai-agent-setup`](plugins/inro-agency-skills/skills/instagram-ai-agent-setup/SKILL.md) | Set up, rebuild, fix and test a client's Inrō AI agent, the assistant that answers Instagram DMs. | [instagram-ai-agent-setup.zip](downloads/instagram-ai-agent-setup.zip) |
| **Audit and plan** | | |
| [`instagram-account-audit`](plugins/inro-agency-skills/skills/instagram-account-audit/SKILL.md) | Audit a client's Instagram account in Inrō end to end without changing anything. | [instagram-account-audit.zip](downloads/instagram-account-audit.zip) |
| [`dm-funnel-planner`](plugins/inro-agency-skills/skills/dm-funnel-planner/SKILL.md) | Plan which Instagram DM automations to build for a client, and in what order, from what the account actually gets. | [dm-funnel-planner.zip](downloads/dm-funnel-planner.zip) |
| **Build** | | |
| [`dm-flow-builder`](plugins/inro-agency-skills/skills/dm-flow-builder/SKILL.md) | Build, check and test Instagram DM automations in Inrō for a client, safely. | [dm-flow-builder.zip](downloads/dm-flow-builder.zip) |
| [`inbound-dm-playbook`](plugins/inro-agency-skills/skills/inbound-dm-playbook/SKILL.md) | The standard way to handle inbound Instagram DMs on a client account in Inrō. | [inbound-dm-playbook.zip](downloads/inbound-dm-playbook.zip) |
| **Run and report** | | |
| [`monthly-client-report`](plugins/inro-agency-skills/skills/monthly-client-report/SKILL.md) | Writes the monthly performance report an agency sends to an Instagram client that runs on Inrō. | [monthly-client-report.zip](downloads/monthly-client-report.zip) |
| [`multi-client-health-check`](plugins/inro-agency-skills/skills/multi-client-health-check/SKILL.md) | Weekly health check across every Instagram client your agency runs on Inrō. | [multi-client-health-check.zip](downloads/multi-client-health-check.zip) |
| [`partner-bulk-rollout`](plugins/inro-agency-skills/skills/partner-bulk-rollout/SKILL.md) | Roll one change out across many client Instagram accounts through the Inrō partner connector, safely and one client at a time. | [partner-bulk-rollout.zip](downloads/partner-bulk-rollout.zip) |
| **Content** | | |
| [`client-post-scheduler`](plugins/inro-agency-skills/skills/client-post-scheduler/SKILL.md) | Writes an Instagram caption and hashtags in a client's brand voice for an image, carousel, reel or story, then saves it as a draft, schedules it or publishes it on the client's account through Inrō once you approve. | [client-post-scheduler.zip](downloads/client-post-scheduler.zip) |
| [`short-form-content-principles`](plugins/inro-agency-skills/skills/short-form-content-principles/SKILL.md) | How a short video holds a viewer, written for agencies scripting Instagram Reels for clients. | [short-form-content-principles.zip](downloads/short-form-content-principles.zip) |
<!-- SKILLS:END -->

## What you need

- **An Inrō account for each client**, on Pro, a trial or a lifetime plan (free accounts are refused). [Sign up](https://app.inro.social/users/sign_up?utm_source=agency-kit&utm_medium=referral&utm_campaign=agency-skills-repo) and connect the client's Instagram Business or Creator account.
- **Claude** on claude.ai, the desktop app or Claude Code, with the Inrō connector added (below).
- **For many clients at once** (the partner skills and the multi-client modes): an Inrō partner account and its partner token. See [the partner dashboard](https://help.inro.social/en/articles/17027622) and [the partner API and MCP](https://help.inro.social/en/articles/17027623).

`short-form-content-principles` works without any connector.

## Install on claude.ai or the desktop app

**1. Add the skills**
1. Download the zip of the skill you want from the table above.
2. In Claude, open **Customize > Skills**, click **+**, then **Create skill > Upload a skill**, and pick the zip. Upload one skill zip at a time. ([All skills in one zip](downloads/inro-agency-skills-all.zip) is there for copying into Claude Code.)
3. Code execution must be on. On Team and Enterprise plans, an owner enables skills in the **Plugins & skills** policy first, and can share them with the whole team.

**2. Add the Inrō connector** (one client account per connection)
1. Open **Customize > Connectors**, click **+ Add**, then **Add custom connector**. On Team and Enterprise plans, an owner adds it under **Organization settings > Connectors** and members click **Connect**.
2. URL: `https://api.inro.social/mcp`
3. Sign in with your Inrō account and pick the client's Instagram account. To switch to another client, connect again or add a second connector. [Help article](https://help.inro.social/en/articles/16004471)

**Or the partner connector** (every client from one connection)
1. Add a custom connector with the URL `https://api.inro.social/partner/mcp`.
2. Choose **No sign in**, then add the request header `Authorization` with the value `Bearer YOUR_PARTNER_TOKEN` (from **app.inro.social/partners > API & MCP**).
3. Name the client in every request ("on @clientaccount, ..."). A request that names no account is refused on purpose.
4. On Team and Enterprise plans everyone shares that one credential, so only add it where everyone should reach every client.

## Install in Claude Code

**Skills, as a plugin**
```
/plugin marketplace add inro-app/inro-agency-skills
/plugin install inro-agency-skills@inro-agency-kit
```
The skills then show up as `/inro-agency-skills:<skill-name>`, and Claude also picks them up on its own when your request fits. To update later: `claude plugin marketplace update inro-agency-kit`, then `claude plugin update inro-agency-skills@inro-agency-kit`.

Prefer plain folders? Copy the folders in `plugins/inro-agency-skills/skills/` into `~/.claude/skills/`. Use one way or the other, not both, or every skill shows up twice.

**The connector**
```
claude mcp add --transport http inro https://api.inro.social/mcp
```
Then run `/mcp` in Claude Code and sign in.

**The partner connector**, with the token kept out of your shell history:
```
export INRO_PARTNER_TOKEN="paste-it-here"
claude mcp add --transport http inro-partner https://api.inro.social/partner/mcp --header "Authorization: Bearer $INRO_PARTNER_TOKEN"
```

## Try it

- "Audit @clientaccount and tell me the three quickest wins."
- "Plan a DM funnel for @clientaccount from what their last month of posts actually got."
- "Set up the AI agent for @clientaccount from their website and FAQ."
- "Write this month's report for @clientaccount."
- "Run the weekly health check across all my clients."
- "Roll the 'Answer price questions in DMs' template out to my three e-commerce clients, inactive, and show me the plan first."

## Good to know

- New automations are created switched off. You switch them on after checking them.
- Skills never message real contacts as a test.
- Start any new connector with read-only questions across two or three clients before you let it change anything.
- Security notes: [SECURITY.md](SECURITY.md).

## Help and feedback

- Product help: [help.inro.social](https://help.inro.social) or support@inroapp.com
- Something wrong in a skill: [open an issue](https://github.com/inro-app/inro-agency-skills/issues) ([how](CONTRIBUTING.md))

## Licence

[MIT](LICENSE). Inrō is a trademark of its owner; the licence covers the skill files, not the Inrō name or product.
