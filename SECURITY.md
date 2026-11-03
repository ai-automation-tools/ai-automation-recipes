# Security policy

## Reporting a vulnerability

Please report it privately, not in a public issue or pull request:

1. Open the repository's **Security** tab.
2. Choose **Report a vulnerability** and describe what you found, how to reproduce it, and which
   recipe, script or profile it touches.

If the **Report a vulnerability** button isn't there, open an issue titled "Security contact
request" with no details in it, and a maintainer will arrange a private channel.

You'll get an acknowledgement within a week. Fixes land on `main`; the Cronsole editions pick them up
through the pinned runtime bundle, so a fix ships with a `VERSION` bump.

## What counts

- A recipe, profile or script that reads or writes outside its staging and output folders
- A secret, token or home path that reaches a commit, a log or a delivered artifact
- A template parameter that can carry an API key, or a profile that widens an agent's permissions
  without saying so
- Prompt content that makes a scheduled agent act on text it fetched from the web

Bugs in how Cronsole imports or schedules a template belong in the
[Cronsole repository](https://github.com/ai-automation-tools/cronsole/issues).

## Supported versions

Only the latest release and `main`.
