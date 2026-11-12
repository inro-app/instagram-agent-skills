# Checks: what to read, what counts as a finding

On the partner connector, every call below also takes `organization`: the client's account id from `list_organizations`.

The thresholds below are defaults. If the agency wants a different bar, write it in the roster's notes and follow that.

## 1. Connection and plan: `get_organization_info`

| Field | What it tells you |
| --- | --- |
| `login_error_data.login_error` | `true`: Instagram reported a problem with the connection. |
| `login_error_data.login_error_message` | Meta's wording. Use it to tell an expired or revoked session from something else. |
| `login_error_data.login_error_flagged_at` | When the problem was first flagged. This is the "disconnected since" date. If absent, write "date unknown". |
| `instagram_restrictions` | Account-wide restrictions Meta applies now, oldest first. Each has `kind` (`sending_blocked`: every DM; `links_blocked`: DMs with a link; `rate_limited`: every DM, usually for minutes), `first_seen_at`, Meta's `error_message` and a `help_url`. Inrō pauses the affected messages and resumes them on its own once the restriction lifts. |
| `instagram_linked_at` | When Instagram was connected. A date later than last week's snapshot means someone reconnected during the week. |
| `can_publish`, `missing_publish_scopes` | Whether Instagram's publishing permission is granted. Matters only for clients whose posts you publish or schedule. |
| `subscription_tier` | `free`, `trial` or `pro`. The connector refuses free accounts. |
| `current_billing_period_end` | When the current period ends. On a Trial account, check in the app whether that is also the trial end. |
| `max_contact_activations` | The activation allowance on capped plans. |

**Matching the partner dashboard's words.** If you are a partner, the dashboard card for each client shows one connection status. The fields above map to it like this, so your report uses the same words:

| Dashboard status | From the connector |
| --- | --- |
| Disconnected | `executions` → `health` returns `account.instagram_connected: false`. Automations cannot run. |
| Error | `login_error_data.login_error` is `true` but `account.instagram_connected` is still `true`. |
| Restricted | `instagram_restrictions` is not empty. |
| Limited | Connected, but permissions are missing. The connector only shows the publishing ones (`missing_publish_scopes`); check the dashboard for others. |
| Not connected | `list_organizations` shows `instagram_connected: false` and no `username`. |
| Connected | None of the above. |

## 2. Runs: `executions` → `health`

Params: `since` (ISO 8601, default 7 days ago, at most 90 days back), `until` (default now).

| Field | Use |
| --- | --- |
| `executions` | Run counts by status, every status present (so a 0 is a real 0), plus `total`. Statuses: `pending`, `completed`, `failed`, `partially_completed`, `interrupted`, `limited`, `disconnected`, `restricted`. Test runs are excluded. |
| `failure_rate` | Share of runs that `failed` or `partially_completed`, from 0 to 1. |
| `account.instagram_connected` | `false` stops every automation at once. Editing a flow will not help. |
| `account.contact_activation_limit_reached` | `true` stops automations messaging new people until the period resets or the plan changes. |
| `account.contact_activations_used`, `account.contact_activations_limit` | Usage this billing period. No limit on Pro. |
| `top_failing` | Up to 5 automations ranked by failure rate, not volume: `type`, `id`, `title`, `executions`, `failed`, `failure_rate`, `top_reason_code`. |
| `top_reason_codes` | The most common reasons runs ended other than completing, as `reason_code` and `count`. |

Then, for each automation in `top_failing`: `scenarios` → `performance` (or `campaigns` → `performance`) with `id` and the same window. Each step has `position`, `action_type`, `reached`, `failed` and `top_reason_codes`. The step with the most failures is the one to name. To see one failing run in full: `executions` → `list` with `scenario_id` (or `campaign_id`) and `status: "failed"`, then `executions` → `get` with `type` and `id`. A run's `status_message` is the plain-language reason to quote.

## 3. Automations: `scenarios` → `list`

Paginate to the end (`per_page` up to 100).

| Field | Use |
| --- | --- |
| `active` | Whether it is switched on. Compare the count with last week. |
| `suspended` | `true`: suspended by the platform. It cannot run, be edited or be copied. |
| `last_executed_at` | When it last ran. The field to trust for "did it run". |
| `paused_executions` | `limited` and `disconnected`: runs held back and waiting to be re-run. Comment runs past Instagram's 7-day private-reply window are not included, because they can no longer be sent. |
| `metrics` | Cached totals (`executions.total`, `conversions.total`) and a cached 7-day figure. See the traps below. |
| `created_at` | To tell "new and not used yet" from "never used". |
| `full_url` | Link it in the report. |

To check AI steps on one automation, `scenarios` → `get` returns its actions, each with `warnings` (`message`, `severity` of `issue` or `suggestion`, optional `help_url`). Two warnings matter here: "AI features disabled" (AI is not available to the account, for example a Trial account out of AI credits) and "AI agent messages are disabled" (the agent is set to disable all replies). Read `get` only on active automations with AI steps, not on everything.

## 4. Campaigns: `campaigns` → `list`

`per_page: 10`, newest first. Fields: `title`, `status` (`draft`, `scheduled`, `running`, `completed`, `limited`, `canceled`), `sent_at`, `metrics` (`contacts`, `sent`, `opened`, `converted`, `failed`, `running`), `full_url`.

## 5. Background jobs: `batch_tasks` → `list`

`per_page: 10`. `status`, `task_type`, `error_message`. Empty is normal on accounts that do not run bulk updates or campaigns.

## 6. AI agent: `agent` → `get`

`trigger_mode`: `all_messages`, `specific_messages`, `automation_only` or `never_reply`. `never_reply` ("Disable all replies" in the app) silences the agent everywhere, including the AI steps inside automations. `setup_completed: false` means the agent was never set up.

The connector does not show the AI credit balance. Pro accounts are not metered. Trial and some other plans draw on a limited allowance, and when it runs out AI steps are skipped. If a Trial client's AI steps show the "AI features disabled" warning, check the credit gauge in the app.

## 7. Optional reads

- **Scheduled posts** (clients whose posts you schedule): `medias` → `list`, `status: "scheduled"`, and the most recent published ones. A `publish_status` of `ERROR` or `EXPIRED` means a publish failed; `login_error_data` on that post holds Instagram's error.
- **Ice breakers** (clients that use them): `icebreakers` → `list`. Each has `question` and `automations`. An empty `automations` array, or only inactive ones, means tapping that question starts nothing. This reads live from Instagram on every call.

## Conditions, by level

### Fix today

| Check | Condition |
| --- | --- |
| Reach | Client on the roster not reachable, or its calls refused |
| Connection | `account.instagram_connected: false`, or `login_error_data.login_error: true` |
| Restriction | `instagram_restrictions` has `sending_blocked` or `links_blocked` |
| Activation limit | `account.contact_activation_limit_reached: true` |
| Automation | Any `suspended: true` |
| Paused runs | `paused_executions.disconnected` or `.limited` above 0 on any automation, or `executions.disconnected` / `.limited` above 0 in health |

### This week

| Check | Condition |
| --- | --- |
| Failing automation | In `top_failing` with `failure_rate` 0.10 or more and at least 5 failed runs, or failing every run with at least 3 runs |
| Silent automation | `active: true`, `last_executed_at` null and `created_at` more than 7 days ago; or it ran last week (snapshot) and not this week |
| Switched off | Fewer active automations than last week's snapshot, and the agency did not say why |
| Campaign | `metrics.failed` above 0 on a campaign sent this week; `status: "limited"`; `metrics.running` above 0 more than 30 days after `sent_at` |
| Batch task | `status: "failed"` or an `error_message` |
| AI agent | `trigger_mode: "never_reply"` while the roster says the agent should answer; `setup_completed: false` on a client sold an AI agent; an "AI features disabled" warning on an active automation |
| Publishing | `can_publish: false` or `missing_publish_scopes` not empty, for a client whose posts you publish; a scheduled or recent post with `publish_status` `ERROR` or `EXPIRED` |
| Ice breakers | An ice breaker with no active automation |
| Plan | Trial with `current_billing_period_end` inside 7 days; `contact_activations_used` at 80% or more of a non-null `contact_activations_limit` |

### Keep an eye on

| Check | Condition |
| --- | --- |
| Volume | `executions.total` down by half or more against last week's snapshot, with at least 20 runs last week |
| Conversions | An automation that converted last week (`performance` steps' `converted`, or the snapshot) and converted 0 this week |
| Restriction | `rate_limited` in `instagram_restrictions` |
| Held DMs | `dm_held_window` or `dm_held_private_reply` among the top reason codes. These are Instagram rules, not faults: explain once, do not chase |

## Reason codes in plain words

Use these when a reason code helps. Codes not listed are rare; quote the run's `status_message` instead.

| Code | Plain words | A problem? |
| --- | --- | --- |
| `instagram_disconnected` | Paused: the Instagram connection is broken | Yes, account-wide |
| `plan_limit_reached` | Paused: the activation limit is reached | Yes, account-wide |
| `account_restricted` | Paused: Meta is restricting the account. Resumes on its own | Watch |
| `action_error` | A step failed with an error | Yes |
| `unexpected_error` | A step failed unexpectedly, after automatic retries | Yes |
| `action_skipped` | A step was skipped, for example an AI step while the agent is switched off. The step's error says why | Check the step |
| `scenario_suspended` | The automation is suspended | Yes |
| `scenario_not_active` | The automation was switched off when the run reached it | Only if it should be on |
| `dm_held_window` | Instagram held the DM: the person has not messaged in the last 24 hours. Retried automatically | No, platform rule |
| `dm_held_private_reply` | Instagram allows one DM in reply to a comment, and it was used | No, platform rule |
| `contact_replied`, `manual_reply`, `conversation_handled_by_human` | The person replied, or someone on your team took over | No |
| `contact_in_excluded_folder`, `contact_matches_exclusion_filter` | The person is excluded on purpose | Only if not intended |
| `execution_expired_stuck` | A run was stuck pending and was closed | Check if frequent |

## Data traps

- **Cached 7-day counter.** `metrics.executions.last_7_days` on a scenario is refreshed when the automation runs or is opened in the app, at most once a minute. On an automation that has gone quiet it keeps an old number. Never quote it when it disagrees with `last_executed_at`. Use `health` and `performance` for the week.
- **Three shapes of `metrics`:** `{}` when it never ran, partial with only `total`, or complete with `last_7_days`, `trend` and `total`.
- **Paused is not failed.** `failure_rate` excludes paused runs. Report paused runs separately, as waiting to be re-run.
- **Rolling window.** "Last 7 days" is counted back from the call, not Monday to Sunday.
- **Cached for a minute.** `health` and `performance` cache their result for about a minute, so a number read right after a retry can predate it.
- **90-day limit.** Run lists, health and funnels go back 90 days at most. A single run is readable by id at any age.
- **Logs are short-lived.** Platform logs in the app keep only a few days.
