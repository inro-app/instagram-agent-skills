# Tables for a rollout

Keep all four in one file per rollout (for example `rollout-YYYY-MM-DD.md`). Never write the partner token in it.

## 1. Change spec (Step 1)

```
Change:          Automation copied from one client
Source:          account 12345, automation 678 "Price list on comment"
Content:         as in the source, title "Price list on comment"
Per-client:      price list link, keyword (see table below)
Duplicate rule:  an automation with the same title, or any automation triggered by the same keyword
End state:       switched off; switch on per client after a separate OK
Clients:         8 in scope, 1 set aside (not connected)
```

Per-client values, filled in by the user before the dry run:

| Account id | Username | Link | Keyword |
|---|---|---|---|
| 12345 | @client_one | https://... | PRICE |
| 23456 | @client_two | https://... | PRICES |

## 2. Per-client plan (Step 3)

| # | Account id | Username | Bucket | Action | After the write | Notes |
|---|---|---|---|---|---|---|
| 1 | 12345 | @client_one | Duplicate | Skip | - | "Price list on comment" already exists, off |
| 2 | 23456 | @client_two | New | Create automation | Off | |
| 3 | 34567 | @client_three | Conflict | Waiting on you | - | Active automation "Comment PRICE" uses the same keyword. Skip, rename the keyword, or switch the old one off? |
| 4 | 45678 | @client_four | New | Add ice breaker "What are your prices?" | **Live on approval** | Client has 2 ice breakers |
| 5 | 56789 | @client_five | Blocked | None | - | No link given yet |

Set aside before the dry run: @client_six (not connected), @client_seven (not on Pro or Trial).

Approval line to ask for: "Approve rows 2 and 4 now, and tell me what to do on row 3?"

## 3. Results (Step 5)

| Account id | Username | Outcome | New record | Read-back |
|---|---|---|---|---|
| 23456 | @client_two | Done | automation 9101, off | Matches plan, no warnings |
| 45678 | @client_four | Done | ice breaker payload `...` | Shows on the profile list |
| 34567 | @client_three | Skipped by decision | - | - |
| 12345 | @client_one | Skipped, duplicate | - | - |
| 56789 | @client_five | Blocked | - | Waiting on link |

Outcomes: Done, Skipped (duplicate), Skipped (decision), Blocked, Stopped on error (say what was already written on that client).

## 4. Rollback list (Step 5)

| Account id | Username | Record | How to undo | Saved before change |
|---|---|---|---|---|
| 23456 | @client_two | automation 9101 | `scenarios_manage` update `active: false`; delete only with OK | n/a, new |
| 45678 | @client_four | ice breaker payload `...` | `icebreakers_manage` delete with that payload, after OK | previous list of 2 ice breakers |

Anything changed in place (an automation's steps, the menu, opt-out keywords) lists the saved previous values here, so it can be put back exactly.
