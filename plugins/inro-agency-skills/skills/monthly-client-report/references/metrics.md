# Metrics: where each number comes from and how to label it

Every line in the report comes from one call below. If a number is not here, it is not in the report unless the agency supplied it, and then it is labelled as theirs.

On the partner connector, add `organization` (the client's account id) to every call shown here.

## The window

| What | Value |
| --- | --- |
| Runs and funnels (`executions`, `scenarios` / `campaigns` `performance`) | `since`: first day of the month, 00:00, client's time zone, ISO 8601. `until`: first day of the next month, 00:00. |
| Contact filters (`contacts` → `filter`) | `date_operator: "is_between"`, `date_mode: "exact_date"`, `date_value`: first day, `date_value_end`: last day. Both days are included. |
| Lookback | Run lists, health and funnels serve the last 90 days. A `since` older than that is refused. Run the report within a few weeks of month end, and the previous month can still be recomputed live. |

## Automation runs

| Report line | Call | What it counts | Label in the report |
| --- | --- | --- | --- |
| Automation runs | `executions` → `health`, `since`/`until` | `executions.total`: every scenario and campaign run started in the window, test runs excluded. `executions` also splits them by status. | "Times your automations ran in October" |
| Runs that did not finish | same call, `executions.failed` + `executions.partially_completed`, and `failure_rate` | Runs where a step failed. `partially_completed` means earlier steps had already run. | Usually an internal note, not a client line. Mention it only with its explanation and what was done about it. |
| Runs paused | same call, `limited`, `disconnected`, `restricted` | Runs held back by the activation limit, a broken Instagram connection, or a Meta restriction. They are paused, not lost, and can be re-run. | Only if it explains a dip: "Automations were paused for 3 days while Instagram was reconnected." |

`health` results are cached for about a minute. That does not matter for a past month.

## Per automation

`scenarios` → `list` (paginate to the end) gives `id`, `title`, `active`, `created_at`, `last_executed_at`, `full_url`, and a `metrics` object with all-time totals. Use the all-time totals only when labelled "since it was created".

For each automation with `last_executed_at` on or after the month's first day, call `scenarios` → `performance` with `id`, `since`, `until`. The response:

- `executions`: run counts for the window by status, with `total` and `failure_rate`.
- `steps`: one entry per step in flow order, each with `position`, `action_type`, `reached` (runs that got to the step), how they ended there (`completed`, `failed`, `pending`, `interrupted`, `cancelled`, `skipped`), `metrics` (`sent`, `read`, `clicked`, `replied`, `converted`) and `top_reason_codes`.

| Report line | From | Label |
| --- | --- | --- |
| Runs per automation | `performance.executions.total` | "The comment flow on your launch post ran 820 times in October" |
| Messages read | first message step: `metrics.read` against `metrics.sent` | "610 of 800 people opened the first message" |
| Link clicks per automation | conversion-link step: `metrics.clicked` | "190 people tapped the link to your booking page" |
| Where people stop | the step where `reached` drops most against the step before | A line in "what we are testing next" |

Campaigns: `campaigns` → `list` gives `title`, `status`, `sent_at`, `full_url` and `metrics` (`contacts`, `sent`, `opened`, `converted`, `failed`, `running`). A campaign is a one-off send, so its metrics belong to the month it was sent, unless it was still running at month end. `campaigns` → `performance` with `id`, `since`, `until` gives the step funnel.

## AI steps and the AI agent

| Report line | From | Label |
| --- | --- | --- |
| AI replies inside automations | `performance.steps` with `action_type` `agent_reply`, `agent_message` or `agent_comment`: `metrics.sent` | "Your AI assistant replied 430 times inside your automations" |
| Hand-offs to the AI agent | steps with `action_type` `agent_handover`: `reached` | "380 conversations were handed to your AI assistant" |
| Automations the agent started | `executions` → `list`, `execution_type: "agent"`, `since`/`until`, `per_page: 1`, read `pagination.total_count` | "Your AI assistant started 45 follow-up flows, for example sending the price list when asked" |
| The agent's own replies outside automations | not in the connector | In the app: AI Agent page, **Message history**. Ask the agency, or leave the line out. |

What changed on the agent this month: `agent` → `list_items` and `agent` → `list_actions` carry `created_at`.

## Contacts

Call `get_contact_filter_types` once per run and build filters from its answer. Count with `contacts` → `filter`, `filters: [ ... one filter ... ]`, `per_page: 1`, and read `pagination.total_count`. Use one filter per count, so each number means exactly one thing.

**Counts stop at 10,000.** Past that, `pagination.total_count` reads 10,000 and `pagination.total_count_capped` is `true`. The figure is then a floor: write "more than 10,000", do not compare or subtract it, and take an exact number from the app if the client needs one.

| Report line | Filter | What it counts | Label |
| --- | --- | --- | --- |
| New contacts | `first_interaction`, month range | Contacts whose very first message, comment or mention with the account falls in the month | "New people who reached out" |
| Engaged contacts | `any_engagement`, month range | Contacts with any message activity in the month | "People in a conversation with you" |
| People who went through an automation | `scenario`, month range (add `scenario_id` for one automation) | Contacts who went through any scenario in the month | "People your automations talked to" |
| People who received a campaign | `campaign`, month range (add `filtered_campaign_id` for one) | Contacts who received a campaign in the month | "People who received a broadcast" |
| Link clickers | `clicked_conversion_link`, month range (add `conversion_link_id` per destination) | Contacts who clicked a tracked link in the month. A person who clicked twice counts once. | "People who clicked through to your shop" |
| Survey answers | `survey`, month range, `options.survey_completion_status: "received_and_completed"` | Contacts who completed a survey | "People who answered your quiz" |
| Payments | `payment`, month range, `options.payment_status: "paid"` | Payments made through Inrō's Stripe step | Only if the client takes payments in DMs |
| Bookings | `appointment`, month range | Appointments created through Inrō's Calendly step | Only if the client books through the Calendly step |
| Total audience | `contacts` → `list`, `per_page: 1` | Every contact stored in the account, to date | "Your audience in Inrō, to date" |
| Emails stored | `email`, `operator: "is_present"` | Contacts with an email address, to date | Total to date; the month's change needs last month's snapshot |
| Phones stored | `phone`, `operator: "is_present"` | Same, phone numbers | Same |
| Custom data | `contact_property`, `operator: "is_present"`, `options.contact_property`: the property identifier | Contacts with a value for that property, to date | Same |

`conversion_links` → `list` gives each link's `title` and destination `url`, so a click count gets a plain-language name.

Activated contacts, the billing unit, are counted once per contact per billing period, when a scenario, campaign or the AI agent first messages them. `executions` → `health` returns `account.contact_activations_used` and `account.contact_activations_limit` for the **current billing period**, which starts on the billing date, not the 1st. For a calendar month, use the client's Dashboard (**Activated contacts**, with the month as the date range). The partner dashboard's Billing page shows usage by account for the billing period. If you report it, say where it came from and which period it covers.

## Posts and stories

`medias` → `list`, `status: "published"`, `per_page` up to 100, newest first. Stop paging once `posted_at` is before the month.

- `insights` is a hash keyed by metric name (reach, views, likes, saved, shares and others Instagram returns). It is present only when `insights_status` is `fresh`.
- `refreshing`: a refresh is running. Read again a minute later. Older posts start refreshing when they are read, so expect this on the first pass.
- `unavailable`: Instagram does not report on that post for this account. Leave it out of the totals and say "insights were not available for 2 of 14 posts".
- Report totals and averages, not a row per post. Summed reach counts the same person once per post, so call it "combined reach", never "people reached".

`stories` → `list` returns stories with an `insights` hash that Instagram fills by webhook. It is often empty. If so, tell the agency and let them check the story insights in the app. Story-reply automations report their own runs in `performance` either way.

## Things to leave out

- Follower growth: not in Inrō. Ask the agency or leave it out.
- Any platform-wide average or benchmark.
- Anything Inrō cannot see: sales on the client's website, emails sent from another tool, flows run by another automation tool.
