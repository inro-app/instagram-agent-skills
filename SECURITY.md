# Security

## Report a problem
If you find a security issue in these skills or in how they use the Inrō connector, email **support@inroapp.com** with "Security" in the subject. Please don't open a public issue for it.

## Keep your tokens safe
- The **partner token** reaches every client account in your workspace. Never paste it into a chat, a skill file, a shared document or a client-facing tool. If it is ever exposed, open the partner dashboard, go to **API & MCP** and click **Regenerate**.
- Regenerate it when someone leaves your team. Removing them from the workspace doesn't invalidate a token they already copied.
- Skills in this repo never ask you to paste a token into the conversation. Tokens go in the connector settings only.
- Template share pages show a flow's settings. Don't share a client's flow publicly if it holds an API key, a webhook URL with a key or a pixel token.
