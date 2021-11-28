import json

import requests

from .formatter import *


def send_slack_message(webhook: str, formatted_message: FormattedMessage):
    blocks = []
    for challenge_message in formatted_message.challenge_messages:
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": challenge_message
            }
        })

    for leaderboard_message in formatted_message.leaderboard_messages:
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": leaderboard_message
            }
        })

    blocks.append({
        "type": "context",
        "elements": [
            {
                "type": "image",
                "image_url": "https://adventofcode.com/favicon.png",
                "alt_text": "Advent of Code"
            },
            {
                "type": "mrkdwn",
                "text": f"AoC 2021 Leaderboard | <https://adventofcode.com/2021/leaderboard/private/view/{formatted_message.board_id}|view>"
            }
        ]
    })

    response = requests.post(
        webhook,
        data=json.dumps({"blocks": blocks}),
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        raise ValueError(
            f"Request to Slack returned an error {response.status_code}, the response is:\n{response.text}"
        )
    else:
        print("Slack notified!")


def send_discord_message(webhook: str, formatted_changes: FormattedMessage):
    pass
