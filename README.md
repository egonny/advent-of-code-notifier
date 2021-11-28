# Advent Of Code Notifier

A script that sends a message on Slack and/or Discord whenever a leaderboard on [Advent Of Code](https://adventofcode.com/) changes.

* On the first run, the script reads the current leaderboard and writes it to a new file called `old_leaderboard.json` in the current directory.
* On subsequent runs, the script reads the previous leaderboard from this file and compares it with the current leaderboard.
  It then sends a message summarizing the leaderboard changes to the configured Slack app and/or Discord server, and updates the file's contents.

## Setup

```bash
pip install -r requirements.txt
```

## Running

The CLI accepts input as environment variables:
* `AOC_SESSION`: The `session` cookie for authenticating with the AoC API.
* `AOC_BOARD`: The ID of the private leaderboard to monitor.
* `AOC_SLACK_HOOK`: The [Webhook URL](https://api.slack.com/messaging/webhooks) for your Slack app. (Optional)
* `AOC_DISCORD_HOOK`: The [Webhook URL](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks) for your Discord server. (Optional)

Example usage:
```bash
AOC_SESSION=my_cookie AOC_BOARD=123456 AOC_SLACK_HOOK=my_slack_url python aoc-notifier
```
