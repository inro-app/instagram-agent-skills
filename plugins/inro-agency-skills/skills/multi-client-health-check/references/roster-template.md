# Client roster template

Keep one roster file for the agency, default name `clients.md`, in the folder you run the check from. The check reads it at the start of every run and compares it with the accounts it can reach. It is the only way the check can tell that a client is missing.

Copy the table below and fill one line per client. Keep it short: the notes column is what makes the check smart about each client.

```markdown
# Clients

| Handle | Account id | Plan | Owner | Notes |
| --- | --- | --- | --- | --- |
| @client_handle | 12345 | Pro | Sam | AI agent answers all DMs. Comment-to-DM on every reel. We schedule posts. |
| @second_client | | Trial | Alex | Trial ends mid-month. No AI agent yet. Ice breakers live. |
| @third_client | | Pro | Sam | Campaigns every Friday. Paused on purpose until January. |
```

## Columns

| Column | What to put | How the check uses it |
| --- | --- | --- |
| Handle | The client's Instagram username, with or without @ | Matches the roster line to an account |
| Account id | The Inrō account id. Leave blank and the check fills it from `list_organizations` on the partner connector | Used in every call on the partner connector, since a username can match more than one account |
| Plan | Pro, Trial, or how you bill it ("partner plan") | A mismatch with what the account reports is a finding |
| Owner | Who on your team looks after this client | Shown next to each finding so the right person picks it up |
| Notes | What should be true on this account | Turns optional checks on and sets expectations, see below |

## Notes the check understands

Write them in plain words. The check looks for these ideas:

- **"AI agent answers all DMs" / "agent only in automations" / "no AI agent":** what the agent's mode should be. A different `trigger_mode` is a finding.
- **"We schedule posts" / "we publish for them":** turns on the publishing and scheduled-post checks.
- **"Ice breakers live":** turns on the ice breaker check.
- **"Campaigns every Friday" or similar:** a week with no campaign sent is worth a line.
- **"Paused on purpose until [date]":** silent or switched-off automations on this client are not reported until that date.
- **"Not live yet" / "onboarding":** an account with Instagram not connected is expected, not a finding.
- **Your own thresholds**, for example "flag failures above 5%": used instead of the defaults in `checks.md`.

## Keep it current

- When the check finds an account that is not on the roster, it says so. Add the line.
- When a client leaves, delete the line, or the check will report them missing every week.
- Do not put passwords, tokens, client contact details or anything private in this file. It holds handles, ids and notes only.
