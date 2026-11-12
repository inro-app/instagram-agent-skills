# Example output

A filled example with made-up clients, to show the format. Your file is saved as `health-checks/<YYYY-MM-DD>-health-check.md`.

---

# Health check, 10 to 17 Nov 2026

Scheduled run, Monday 17 Nov, 09:00. 5 of 5 clients on the roster reached, through the partner connector. **2 need action today:** @client_a lost its Instagram connection on Saturday and every automation on it has been paused since.

## Fix today

1. **@client_a: Instagram disconnected since 15 Nov.** Every automation on this account is paused, including [the flow that DMs the price list to people who comment PRICE](https://app.inro.social/automation/scenarios/0). Instagram reports the session as expired. 64 runs are paused and waiting. Next step: the account owner reconnects Instagram in Inrō (Reconnect on the partner dashboard card), then use **Run paused executions** on the dashboard card, window **Last 7 days**. Owner: Sam.
2. **@client_b: activation limit reached on the Trial plan.** 1,000 of 1,000 activated contacts used this period, so automations no longer message new people. 23 runs are held back. Next step: move the account to Pro or wait for the period to reset, then re-run the held runs. Owner: Alex.

## This week

3. **@client_c: link step failing in the welcome flow.** [The flow that answers a first DM and sends the booking link](https://app.inro.social/automation/scenarios/0) failed 41 of 60 runs this week, all at step 3, the link card, mostly `action_error`. It was fine last week. Next step: open a failed run in the scenario's History tab to read Instagram's error before changing anything; then **Retry all failed** on that step. Owner: Sam.
4. **@client_d: AI agent switched off.** The agent is set to Disable all replies, but the roster says it should answer all DMs. Two active automations hand conversations to the agent, and those steps are being skipped. Next step: check with the client whether this was on purpose, then set the mode back. Owner: Alex.
5. **@client_e: campaign sends failed.** [The Friday offer broadcast](https://app.inro.social/campaigns/0) failed 12 of 480 sends. Next step: open the campaign's failed sends to see the reason. Owner: Sam.

## Keep an eye on

6. **@client_c: runs down by more than half.** 140 runs this week against 310 last week, beyond the failures above. Two fewer reels went out, which may be the whole story. Check next week.
7. **@client_e: many DMs held by Instagram.** 30 runs held because the person had not messaged in the last 24 hours (`dm_held_window`). That is an Instagram rule, retried on its own, not a fault.

Good news: @client_b's story-reply flow converted 18 people this week, up from 5.

## All clients at a glance

| Client | Connection | Automations on | Runs (7 days) | Failure rate | Paused runs | Plan, renews |
| --- | --- | --- | --- | --- | --- | --- |
| @client_a | Disconnected since 15 Nov | 6 of 6 | 210 | 0% | 64 | Pro, 2 Dec |
| @client_b | Connected | 4 of 4 | 380 | 1% | 23 | Trial, 28 Nov |
| @client_c | Connected | 5 of 6 | 140 | 29% | 0 | Pro, 9 Dec |
| @client_d | Connected | 3 of 3 | 95 | 0% | 0 | Pro, 21 Nov |
| @client_e | Connected | 7 of 7 | 520 | 2% | 0 | Pro, 30 Nov |

## Snapshot for next week

```json
{
  "window": { "since": "2026-11-10T09:00:00Z", "until": "2026-11-17T09:00:00Z" },
  "connector": "partner",
  "clients": [
    {
      "username": "client_a",
      "account_id": 0,
      "connection": "disconnected",
      "connection_since": "2026-11-15",
      "instagram_linked_at": "2026-03-02",
      "subscription_tier": "pro",
      "billing_period_end": "2026-12-02",
      "active_automations": 6,
      "total_automations": 6,
      "runs": 210,
      "failed": 0,
      "partially_completed": 0,
      "paused": { "limited": 0, "disconnected": 64, "restricted": 0 },
      "failure_rate": 0.0,
      "activations_used": 812,
      "activations_limit": null,
      "agent_trigger_mode": "all_messages",
      "converting_automations": [ { "id": 0, "converted": 22 } ],
      "ran_this_week": [0]
    }
  ]
}
```
