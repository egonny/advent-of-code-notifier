import requests

from .formatter import *

DISCORD_SIDE_COLOR = 0x04450c


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
        json={"blocks": blocks},
    )
    if response.status_code != 200:
        raise ValueError(
            f"Request to Slack returned an error {response.status_code}, the response is:\n{response.text}"
        )
    else:
        print("Slack notified!")


def send_discord_message(webhook: str, formatted_message: FormattedMessage):
    fields = []

    if formatted_message.challenge_messages:
        fields.extend(create_discord_fields(
            ":tada: Challenge updates :tada:", formatted_message.challenge_messages))

    if formatted_message.leaderboard_messages:
        fields.extend(create_discord_fields(
            ":trophy: Leaderboard updates :trophy:", formatted_message.leaderboard_messages))

    embed = {
        "title": "<a:pepechristmashype:914628245046054934> Advent of Code update <a:pepechristmashype:914628245046054934>",
        "url": f"https://adventofcode.com/2021/leaderboard/private/view/{formatted_message.board_id}",
        "color": DISCORD_SIDE_COLOR,
        "footer": {
            "icon_url": "https://adventofcode.com/favicon.png",
            "text": "AoC 2021"
        },
        "fields": fields
    }

    response = requests.post(webhook, json={"embeds": [embed]})
    if response.status_code > 299:
        raise ValueError(
            f"Request to Discord returned an error {response.status_code}, the response is:\n{response.text}"
        )
    else:
        print("Discord notified!")


def create_discord_fields(title: str, value_parts: list[str]) -> list[dict[str, str]]:
    fixed_value_parts = [part.replace(
        "*", "**") + "\n" for part in value_parts]
    field = {"name": title, "value": ""}
    for part in fixed_value_parts:
        if len(field["value"]) + len(part) > 1024:
            yield field
            field = {"name": "\u200b", "value": part}
        else:
            field["value"] += part
    yield field
