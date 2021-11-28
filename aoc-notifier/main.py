import datetime
import json
import os

import requests
import inflect

INFLECT = inflect.engine()
OLD_LEADERBOARD = 'old_leaderboard.json'


def format_leaderboard_changes(leaderboard_changes):
    result = ""
    for change in leaderboard_changes:
        result += f"{':arrow_up:' if change['positive'] else ':arrow_down:'} *{INFLECT.ordinal(change['position'])}* {change['username']} ({change['points']} points)\n"

    return result


def format_complete_chal_message(challenge):
    star = ":star2:" if challenge["part"] == 2 else ":star:"
    timestamp = datetime.datetime.fromtimestamp(challenge['timestamp'])

    return f"*{challenge['username']}* has completed {star} *Day {challenge['day']}* ({challenge['part']}) at {timestamp.strftime('%H:%M:%S')}!"


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


def get_leaderboard(id, session):
    response = requests.get(
        f"https://adventofcode.com/2020/leaderboard/private/view/{id}.json", headers={"cookie": f"session={session}"})
    if response.status_code != 200:
        raise ValueError(
            f"Request to AOC returned an error {response.status_code}, the response is:\n{response.text}"
        )
    return response.json()


def read_old_leaderboard(leaderboard_location):
    with open(leaderboard_location, 'r') as f:
        return json.load(f)


def write_old_leaderboard(leaderboard, location):
    with open(location, 'w+') as f:
        return json.dump(leaderboard, f)


def extract_changes(old_leaderboard, new_leaderboard):
    challenge_changes = collect_challenge_changes(
        old_leaderboard, new_leaderboard)
    leaderboard_changes = collect_leaderboard_changes(
        old_leaderboard, new_leaderboard)
    return (challenge_changes, leaderboard_changes)


def collect_challenge_changes(old_leaderboard, new_leaderboard):
    changes = []
    for (id, member) in new_leaderboard['members'].items():
        if id not in old_leaderboard['members']:
            continue
        old_member = old_leaderboard['members'][id]
        for (day, chal) in member['completion_day_level'].items():
            for (part, part_details) in chal.items():
                if day in old_member['completion_day_level'] and part in old_member['completion_day_level'][day]:
                    continue
                changes.append({
                    'username': member['name'],
                    'day': int(day),
                    'part': int(part),
                    'timestamp': int(part_details['get_star_ts'])
                })

    return sorted(changes, key=lambda x: x['timestamp'])


def collect_leaderboard_changes(old_leaderboard, new_leaderboard):
    changes = []
    old_positions = create_positions(old_leaderboard)
    new_positions = create_positions(new_leaderboard)
    for (id, new_info) in new_positions.items():
        if not id in old_positions:
            continue

        old_info = old_positions[id]
        if old_info['position'] == new_info['position']:
            continue

        changes.append({
            'username': new_info['username'],
            'position': new_info['position'],
            'points': new_info['points'],
            'positive': old_info['position'] > new_info['position']
        })
    return sorted(changes, key=lambda x: x['position'])


def create_positions(leaderboard):
    positions = {}
    position = 1
    for (id, member) in sorted(leaderboard['members'].items(), key=lambda x: (-x[1]['local_score'], int(x[1]['id']))):
        positions[id] = {
            'username': member['name'],
            'position': position,
            'points': member['local_score']
        }
        position += 1

    return positions


def run(board_id, session, slack_hook):
    new_leaderboard = get_leaderboard(board_id, session)
    try:
        old_leaderboard = read_old_leaderboard(OLD_LEADERBOARD)
    except:
        print("No old leaderboard found, saving new leaderboard and quitting.")
        write_old_leaderboard(new_leaderboard, OLD_LEADERBOARD)
        return
    write_old_leaderboard(new_leaderboard, OLD_LEADERBOARD)
    (challenge_changes, leaderboard_changes) = extract_changes(
        old_leaderboard, new_leaderboard)
    if challenge_changes:
        send_message(slack_hook, challenge_changes,
                     leaderboard_changes, board_id)


session = os.environ['AOC_SESSION']
aoc_board_id = os.environ['AOC_BOARD']
slack_webhook = os.environ['AOC_SLACK_HOOK']

run(aoc_board_id, session, slack_webhook)
