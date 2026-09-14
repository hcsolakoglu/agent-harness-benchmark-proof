# Sanitization policy

The export is generated from a separate copy; original benchmark artifacts are not modified.

Removed or pseudonymized categories:

- local OS usernames and user-home paths
- personal/account identifiers known to be unrelated to benchmark semantics
- email addresses
- IPv4 addresses
- UUID/session identifiers (stable pseudonyms preserve trace linkage)
- common GitHub/OpenAI/Anthropic credential formats
- Bearer authorization values
- generic API key/token/secret/password assignments with secret-like values
- token/key/signature values in URL query strings

Excluded entirely:

- auth files and keyrings
- `.env` files
- harness runtime home directories
- SQLite/state databases and caches
- unrelated smoke/debug sessions
- repository `.git` directories from candidate workspaces

After generation the entire export must pass Gitleaks plus additional PII/secret pattern scans before publication.

Additional trace-only pseudonymization replaces opaque runtime/provider call IDs, generation IDs, trace IDs, and Hermes session IDs with stable placeholders. This preserves call/result linkage without publishing correlation identifiers.
