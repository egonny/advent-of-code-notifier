import json

import requests

from .formatter import *


def send_message(webhook, challenge_changes, leaderboard_changes, board_id):
    blocks = []
    for challenge_change in challenge_changes:
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": format_complete_chal_message(challenge_change)
            }
        })

    if leaderboard_changes:
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": format_leaderboard_changes(leaderboard_changes)
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
                "text": f"AoC 2020 Leaderboard | <https://adventofcode.com/2020/leaderboard/private/view/{board_id}|view>"
            }
        ]
    })

    print(json.dumps({"blocks": blocks}))
    response = requests.post(
        webhook,
        data=json.dumps({"blocks": blocks}),
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        raise ValueError(
            f"Request to Slack returned an error {response.status_code}, the response is:\n{response.text}"
        )
